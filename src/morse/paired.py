"""Paired-condition execution with shared task populations."""
from __future__ import annotations

from dataclasses import dataclass
from .harness import HarnessResult, run_harness


@dataclass(frozen=True)
class PairedResult:
    seed: int
    condition_a: str
    condition_b: str
    a: HarnessResult
    b: HarnessResult

    @property
    def success_delta(self) -> float:
        return self.b.success_rate - self.a.success_rate


def run_paired(seed: int, condition_a: str, strength_a: float, condition_b: str, strength_b: float, task_count: int = 100) -> PairedResult:
    return PairedResult(seed, condition_a, condition_b, run_harness(seed, condition_a, task_count, strength_a), run_harness(seed, condition_b, task_count, strength_b))
