"""Mechanism-level synthetic experiment harness.

The harness derives outcomes from actual scheduler activation events. It does
not assign regime-specific bonuses, and therefore cannot encode a preferred
ratio as an assumption.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Iterable

from .experiment import BINARY, MULTI_RATIO, PLATINUM_REGIME, UNIFORM, make_topology
from .phase import PhaseSchedule


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


def _activations(periods: tuple[int, ...], cycles: int) -> int:
    if cycles < 1:
        raise ValueError("cycles must be >= 1")
    # Integer baseline: exact periodic activation, inclusive of cycle zero.
    return sum((cycles - 1) // p + 1 for p in periods)


def _phase_activations(periods: tuple[int, ...], cycles: int) -> int:
    # Convert integer periods to frequencies for the mechanism path. The
    # phase API is exercised here so the experiment is coupled to scheduler
    # state rather than to a regime label.
    total = 0
    for period in periods:
        schedule = PhaseSchedule(1.0 / period)
        total += schedule.activation_count(cycles)
    return total


def run_condition(
    task: Task,
    leaf_count: int,
    regime: str,
    seed: int,
    cycles: int = 32,
) -> Observation:
    if regime not in (UNIFORM, BINARY, PLATINUM_REGIME, MULTI_RATIO):
        raise ValueError(f"unknown regime: {regime}")
    topology = make_topology(leaf_count, regime)
    periods = topology.periods
    activation_total = _phase_activations(periods, cycles)
    # The synthetic task requires signal contributions. Each activation is a
    # bounded contribution; hub events arise only when multiple leaves are
    # active on the same cycle. This is intentionally simple and inspectable.
    by_cycle = [0] * cycles
    for period in periods:
        for cycle in range(0, cycles, period):
            by_cycle[cycle] += 1
    hub_events = sum(v >= 2 for v in by_cycle)
    digest = hashlib.sha256(f"{seed}:{task.task_id}:{activation_total}:{hub_events}".encode()).digest()
    effective_signal = min(task.signal, activation_total) + hub_events
    recovery = 1 if digest[0] % 17 == 0 and hub_events else 0
    success = effective_signal + recovery >= task.difficulty + 2
    cost = activation_total + leaf_count * task.difficulty
    return Observation(
        task.task_id, 0, leaf_count, regime, seed, success, cost,
        activation_total, hub_events, recovery,
    )


def paired_matrix(task_seed: int, task_count: int = 100, repetitions: int = 50) -> list[Observation]:
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
                    row = run_condition(task, leaves, regime, seed)
                    rows.append(Observation(
                        task.task_id, rep, row.leaf_count, row.regime, row.seed,
                        row.success, row.cost, row.activations, row.hub_events,
                        row.recovery_events,
                    ))
    return rows


def jsonl(rows: Iterable[Observation]) -> str:
    return "".join(json.dumps(row.__dict__, sort_keys=True) + "\n" for row in rows)
