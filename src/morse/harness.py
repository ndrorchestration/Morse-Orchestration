"""Provider-neutral seeded task harness for MORSE experiments.

The harness deliberately contains no model/provider dependency. It supplies a
repeatable synthetic coordination workload so scheduler/topology effects can
be isolated before introducing an external AI system.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import random


@dataclass(frozen=True)
class Task:
    task_id: int
    difficulty: int
    answer: int


@dataclass(frozen=True)
class TaskOutcome:
    task_id: int
    success: bool
    attempts: int
    cost: int


@dataclass(frozen=True)
class HarnessResult:
    seed: int
    task_count: int
    successes: int
    total_cost: int
    outcomes: tuple[TaskOutcome, ...]

    @property
    def success_rate(self) -> float:
        return self.successes / self.task_count if self.task_count else 0.0


def derive_seed(master_seed: int, condition: str, task_id: int) -> int:
    """Derive an independent deterministic seed without shared RNG state."""
    material = f"{master_seed}:{condition}:{task_id}".encode()
    return int.from_bytes(hashlib.sha256(material).digest()[:8], "big")


def generate_tasks(seed: int, count: int) -> tuple[Task, ...]:
    if count < 0:
        raise ValueError("count must be non-negative")
    rng = random.Random(seed)
    tasks = []
    for task_id in range(count):
        difficulty = rng.randint(1, 10)
        answer = difficulty * 7 + (task_id % 5)
        tasks.append(Task(task_id, difficulty, answer))
    return tuple(tasks)


def solve_task(task: Task, coordination_strength: float, seed: int) -> TaskOutcome:
    """Simulate a bounded stochastic solver; seed is local to this task."""
    rng = random.Random(seed)
    probability = min(0.995, max(0.05, 0.48 + coordination_strength - task.difficulty * 0.035))
    success = rng.random() < probability
    attempts = 1 if success else 2
    return TaskOutcome(task.task_id, success, attempts, task.difficulty * attempts)


def run_harness(master_seed: int, condition: str, task_count: int, coordination_strength: float) -> HarnessResult:
    tasks = generate_tasks(master_seed, task_count)
    outcomes = tuple(
        solve_task(task, coordination_strength, derive_seed(master_seed, condition, task.task_id))
        for task in tasks
    )
    successes = sum(o.success for o in outcomes)
    return HarnessResult(master_seed, task_count, successes, sum(o.cost for o in outcomes), outcomes)
