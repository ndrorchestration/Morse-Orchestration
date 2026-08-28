"""Minimal deterministic paired-seed bootstrap analysis."""
from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Estimate:
    estimate: float
    ci_low: float
    ci_high: float
    alpha: float
    resamples: int
    seed: int

    @property
    def directional_support(self) -> bool:
        return self.estimate > 0 and self.ci_low > 0


def paired_bootstrap(deltas: list[float], resamples: int = 10_000, seed: int = 20260828, alpha: float = 0.05) -> Estimate:
    if not deltas:
        raise ValueError("deltas must not be empty")
    if resamples < 1 or not 0 < alpha < 1:
        raise ValueError("invalid bootstrap configuration")
    rng = random.Random(seed)
    n = len(deltas)
    estimate = sum(deltas) / n
    means = sorted(sum(deltas[rng.randrange(n)] for _ in range(n)) / n for _ in range(resamples))
    lo = int((alpha / 2) * resamples)
    hi = int((1 - alpha / 2) * resamples) - 1
    return Estimate(estimate, means[lo], means[hi], alpha, resamples, seed)
