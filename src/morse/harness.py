"""Provider-neutral seeded synthetic workload harness."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import random


@dataclass(frozen=True)
class Task:
    task_id: int
    difficulty: int


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
    material = f"{master_seed}:{condition}:{task_id}".encode()
    return int.from_bytes(hashlib.sha256(material).digest()[:8], "big")


def generate_tasks(seed: int, count: int) -> tuple[Task, ...]:
    if count < 0:
        raise ValueError("count must be non-negative")
    rng = random.Random(seed)
    return tuple(Task(i, rng.randint(1, 10)) for i in range(count))


def solve_task(task: Task, coordination_strength: float, seed: int) -> TaskOutcome:
    rng = random.Random(seed)
    probability = min(0.995, max(0.05, 0.48 + coordination_strength - task.difficulty * 0.035))
    success = rng.random() < probability
    attempts = 1 if success else 2
    return TaskOutcome(task.task_id, success, attempts, task.difficulty * attempts)


def run_harness(master_seed: int, condition: str, task_count: int, coordination_strength: float) -> HarnessResult:
    tasks = generate_tasks(master_seed, task_count)
    outcomes = tuple(solve_task(t, coordination_strength, derive_seed(master_seed, condition, t.task_id)) for t in tasks)
    return HarnessResult(master_seed, task_count, sum(o.success for o in outcomes), sum(o.cost for o in outcomes), outcomes)
