"""Experiment configuration and deterministic phase-backed regime construction."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

from .hub import InterchangeHub
from .model import Activation, GateReason, SimulationTrace
from .phase import PhaseLoopSpec, PhaseScheduler, frequency_for_ratio
from .ratios import PLATINUM, SILVER, SQRT2, rounded_periods
from .topology import Topology, clover_topology

UNIFORM = "uniform"
BINARY = "binary"
PLATINUM_REGIME = "platinum"
MULTI_RATIO = "multi_ratio"
REGIMES = (UNIFORM, BINARY, PLATINUM_REGIME, MULTI_RATIO)

@dataclass(frozen=True)
class Regime:
    name: str
    topology: str
    periods: tuple[int, ...]
    ratios: tuple[float, ...]
    rationale: str

@dataclass(frozen=True)
class Task:
    task_id: str
    difficulty: int
    required_signal: int

@dataclass(frozen=True)
class Observation:
    repetition: int
    task_id: str
    condition: str
    seed: int
    success: bool
    cost: int
    coordination_events: int
    recovery_events: int


def period_ratios(topology: int, name: str) -> tuple[float, ...]:
    if topology not in (3, 4):
        raise ValueError("topology must be 3 or 4 leaves")
    if name == UNIFORM:
        return (1.0,) * topology
    if name == BINARY:
        return tuple(2.0 ** i for i in range(topology))
    if name == PLATINUM_REGIME:
        return tuple(PLATINUM ** i for i in range(topology))
    if name == MULTI_RATIO:
        return (1.0, SQRT2, PLATINUM, SILVER)[:topology]
    raise ValueError(f"unknown regime: {name}")


def regime(topology: int, name: str) -> Regime:
    ratios = period_ratios(topology, name)
    periods = rounded_periods(1.0, PLATINUM, topology) if name == PLATINUM_REGIME else tuple(max(1, int(r + 0.5)) for r in ratios)
    rationale = {
        UNIFORM: "Equal cadence baseline.",
        BINARY: "Power-of-two temporal hierarchy.",
        PLATINUM_REGIME: "Geometric cadence using the project-defined Platinum Mean.",
        MULTI_RATIO: "Heterogeneous phase-preserving candidate ratios: 1, sqrt(2), Platinum Mean, Silver.",
    }[name]
    return Regime(name, f"clover-{topology}", periods, ratios, rationale)


def make_topology(leaf_count: int, regime_name: str) -> Topology:
    return clover_topology(leaf_count, regime(leaf_count, regime_name).periods)


def make_phase_scheduler(leaf_count: int, regime_name: str) -> PhaseScheduler:
    ratios = period_ratios(leaf_count, regime_name)
    loops = tuple(PhaseLoopSpec(f"L{i+1}", frequency_for_ratio(ratio), priority=i) for i, ratio in enumerate(ratios))
    return PhaseScheduler(loops)


def derive_seed(global_seed: int, task_id: str, condition: str) -> int:
    return int.from_bytes(hashlib.sha256(f"{global_seed}:{task_id}:{condition}".encode()).digest()[:8], "big")


def make_tasks(seed: int, count: int) -> tuple[Task, ...]:
    if count < 1:
        raise ValueError("count must be >= 1")
    return tuple(Task(f"T{i:04d}", 1 + hashlib.sha256(f"task:{seed}:{i}".encode()).digest()[0] % 5, 1 + hashlib.sha256(f"task:{seed}:{i}".encode()).digest()[1] % 7) for i in range(count))


def run_condition(tasks: tuple[Task, ...], condition: str, global_seed: int, leaf_count: int, repetition: int) -> list[Observation]:
    regime_name = {"C0": UNIFORM, "C1": BINARY, "C2": PLATINUM_REGIME, "C3": MULTI_RATIO}.get(condition)
    if regime_name is None:
        raise ValueError(f"unknown condition: {condition}")
    observations: list[Observation] = []
    loop_names = tuple(f"L{i+1}" for i in range(leaf_count))
    for task in tasks:
        seed = derive_seed(global_seed, task.task_id, condition)
        scheduler = make_phase_scheduler(leaf_count, regime_name)
        cycles = 32 + task.difficulty
        scheduled = scheduler.run(cycles)
        trace = SimulationTrace()
        hub = InterchangeHub(loop_names)
        for cycle, names in scheduled:
            active = set(names)
            for name in names:
                trace.activations.append(Activation(cycle, name, GateReason.PERIODIC, "phase-accumulator"))
            trace.snapshots.append({"cycle": cycle, "active_loops": list(names)})
            hub.state.active_loops = active
            hub.reconcile(cycle, active, trace)
            ordered = [name for name in loop_names if name in active]
            if len(ordered) > 1:
                for source, target in zip(ordered, ordered[1:] + ordered[:1]):
                    hub.route(cycle, source, target, active, payload={"cycle": cycle}, trace=trace)
        coordination = sum(len(names) > 1 for _, names in scheduled)
        coverage = len({name for _, names in scheduled for name in names})
        routed = sum(event.accepted for event in trace.interchanges if event.action == "route")
        digest = hashlib.sha256(f"{seed}:{task.required_signal}:{coordination}:{coverage}:{routed}".encode()).digest()
        recovery = 1 if digest[0] % 11 == 0 else 0
        capacity = coverage + min(3, routed // max(1, cycles // 8)) + recovery
        success = capacity >= task.difficulty + 1
        cost = len(trace.activations) + routed + recovery
        observations.append(Observation(repetition, task.task_id, f"L{leaf_count}-{condition}", seed, success, cost, coordination, recovery))
    return observations


def paired_matrix(task_seed: int, task_count: int = 100, repetitions: int = 50) -> list[Observation]:
    if task_count < 1 or repetitions < 1:
        raise ValueError("task_count and repetitions must be >= 1")
    tasks = make_tasks(task_seed, task_count)
    rows: list[Observation] = []
    for rep in range(repetitions):
        rep_seed = derive_seed(task_seed, f"rep-{rep}", "matrix")
        for leaves in (3, 4):
            for condition in ("C0", "C1", "C2", "C3"):
                rows.extend(run_condition(tasks, condition, rep_seed, leaves, rep))
    return rows
