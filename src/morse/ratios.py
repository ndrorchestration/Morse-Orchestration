"""Candidate temporal ratios used by MORSE.

Constants are scheduling hypotheses, not claims of mathematical or empirical
optimality.
"""
from __future__ import annotations

from math import pi, sin, sqrt

SQRT2 = sqrt(2.0)
GOLDEN = (1.0 + sqrt(5.0)) / 2.0
SILVER = 1.0 + sqrt(2.0)
# Project-defined Platinum Mean: circumradius of a regular hendecagon with unit side.
PLATINUM = 1.0 / (2.0 * sin(pi / 11.0))

CANDIDATES: dict[str, float] = {
    "sqrt2": SQRT2,
    "golden": GOLDEN,
    "platinum": PLATINUM,
    "silver": SILVER,
    "binary": 2.0,
}


def geometric_scales(base: float, ratio: float, count: int) -> tuple[float, ...]:
    """Return deterministic geometric time scales without claiming optimality."""
    if base <= 0:
        raise ValueError("base must be > 0")
    if ratio <= 1:
        raise ValueError("ratio must be > 1")
    if count < 1:
        raise ValueError("count must be >= 1")
    return tuple(base * (ratio ** i) for i in range(count))


def rounded_periods(base: float, ratio: float, count: int) -> tuple[int, ...]:
    """Convert geometric scales to deterministic integer periods.

    Python's bankers rounding is avoided; ties are rounded upward.
    """
    scales = geometric_scales(base, ratio, count)
    return tuple(max(1, int(s + 0.5)) for s in scales)
