"""Paired-condition runner with deterministic seed assignment."""
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
    """Run two conditions on the same generated task population.

    Condition labels remain distinct in the solver RNG derivation, while the
    task seed is shared. This controls task difficulty across the pair.
    """
    a = run_harness(seed, condition_a, task_count, strength_a)
    b = run_harness(seed, condition_b, task_count, strength_b)
    return PairedResult(seed, condition_a, condition_b, a, b)


def run_seed_matrix(seeds: list[int], pairs: list[tuple[str, float, str, float]], task_count: int = 100) -> list[PairedResult]:
    return [run_paired(seed, a, sa, b, sb, task_count) for seed in seeds for a, sa, b, sb in pairs]
