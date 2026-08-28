"""Deterministic paired-seed analysis primitives.

This module intentionally implements the analysis plan without scipy/numpy so
it can run in the minimal CI environment. Bootstrap resampling is paired by
seed and uses a fixed analysis seed for reproducibility.
"""
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
    if resamples < 1:
        raise ValueError("resamples must be positive")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    rng = random.Random(seed)
    n = len(deltas)
    estimate = sum(deltas) / n
    means: list[float] = []
    for _ in range(resamples):
        sample = [deltas[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo_index = int((alpha / 2) * resamples)
    hi_index = int((1 - alpha / 2) * resamples) - 1
    return Estimate(estimate, means[lo_index], means[hi_index], alpha, resamples, seed)
