"""Mechanism-level synthetic experiment harness.

Outcomes are derived from scheduler activations and hub coincidences. No
condition receives a regime-specific bonus, so the harness cannot encode a
preferred ratio as an assumption.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Iterable

from .phase import PhaseLoopSpec, PhaseScheduler, frequency_for_ratio
from .ratios import PLATINUM, SILVER, SQRT2
from .experiment import BINARY, MULTI_RATIO, PLATINUM_REGIME, UNIFORM


@dataclass(frozen=True)
class Task:
    task_id: str
    difficulty: int
    signal: int


@dataclass(frozen=True)
class Observation:
    task_id: str
    repetition: int
    leaf_count: int
    regime: str
    seed: int
    success: bool
    cost: int
    activations: int
    hub_events: int
    recovery_events: int


def derive_seed(global_seed: int, task_id: str, condition: str) -> int:
    material = f"{global_seed}:{task_id}:{condition}".encode()
    return int.from_bytes(hashlib.sha256(material).digest()[:8], "big")


def make_tasks(seed: int, count: int) -> tuple[Task, ...]:
    if count < 1:
        raise ValueError("count must be >= 1")
    result: list[Task] = []
    for i in range(count):
        digest = hashlib.sha256(f"task:{seed}:{i}".encode()).digest()
        result.append(Task(f"T{i:04d}", 1 + digest[0] % 5, 1 + digest[1] % 7))
    return tuple(result)


def period_ratios(leaf_count: int, regime: str) -> tuple[float, ...]:
    if leaf_count not in (3, 4):
        raise ValueError("leaf_count must be 3 or 4")
    if regime == UNIFORM:
        return (1.0,) * leaf_count
    if regime == BINARY:
        return tuple(float(2 ** i) for i in range(leaf_count))
    if regime == PLATINUM_REGIME:
        return tuple(PLATINUM ** i for i in range(leaf_count))
    if regime == MULTI_RATIO:
        return (1.0, SQRT2, PLATINUM, SILVER)[:leaf_count]
    raise ValueError(f"unknown regime: {regime}")


def schedule_trace(leaf_count: int, regime: str, cycles: int) -> list[tuple[int, list[str]]]:
    if cycles < 0:
        raise ValueError("cycles must be non-negative")
    loops = tuple(
        PhaseLoopSpec(f"L{i+1}", frequency_for_ratio(ratio), priority=i)
        for i, ratio in enumerate(period_ratios(leaf_count, regime))
    )
    return PhaseScheduler(loops).run(cycles)


def run_condition(task: Task, leaf_count: int, regime: str, seed: int,
                  cycles: int = 32, repetition: int = 0) -> Observation:
    trace = schedule_trace(leaf_count, regime, cycles)
    activation_total = sum(len(active) for _, active in trace)
    hub_events = sum(len(active) >= 2 for _, active in trace)
    digest = hashlib.sha256(
        f"{seed}:{task.task_id}:{activation_total}:{hub_events}".encode()
    ).digest()
    effective_signal = min(task.signal, activation_total) + hub_events
    recovery = 1 if digest[0] % 17 == 0 and hub_events else 0
    success = effective_signal + recovery >= task.difficulty + 2
    cost = activation_total + leaf_count * task.difficulty
    return Observation(task.task_id, repetition, leaf_count, regime, seed,
                       success, cost, activation_total, hub_events, recovery)


def paired_matrix(task_seed: int, task_count: int = 100,
                  repetitions: int = 50) -> list[Observation]:
    if repetitions < 1:
        raise ValueError("repetitions must be >= 1")
    tasks = make_tasks(task_seed, task_count)
    rows: list[Observation] = []
    for rep in range(repetitions):
        rep_seed = derive_seed(task_seed, f"rep-{rep}", "matrix")
        for leaves in (3, 4):
            for regime in (UNIFORM, BINARY, PLATINUM_REGIME, MULTI_RATIO):
                for task in tasks:
                    seed = derive_seed(rep_seed, task.task_id, f"L{leaves}-{regime}")
                    rows.append(run_condition(task, leaves, regime, seed,
                                               repetition=rep))
    return rows


def jsonl(rows: Iterable[Observation]) -> str:
    return "".join(json.dumps(row.__dict__, sort_keys=True) + "\n" for row in rows)
