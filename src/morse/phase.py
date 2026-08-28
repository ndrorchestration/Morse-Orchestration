"""Phase-accumulator scheduling for non-integer temporal relationships."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PhaseClock:
    """Deterministic clock whose frequency is activations per primary cycle."""

    frequency: float
    phase: float = 0.0

    def __post_init__(self) -> None:
        if self.frequency <= 0:
            raise ValueError("frequency must be > 0")
        if self.frequency > 1:
            raise ValueError("frequency must be <= 1 activation per primary cycle")
        if not 0 <= self.phase < 1:
            raise ValueError("phase must satisfy 0 <= phase < 1")

    def tick(self) -> bool:
        """Advance one primary cycle and report whether this clock fires."""
        self.phase += self.frequency
        if self.phase >= 1.0:
            self.phase -= 1.0
            return True
        return False


@dataclass(frozen=True)
class PhaseSchedule:
    """Immutable specification of a loop's desired period ratio."""

    period_ratio: float
    initial_phase: float = 0.0

    def __post_init__(self) -> None:
        if self.period_ratio < 1:
            raise ValueError("period_ratio must be >= 1")
        if not 0 <= self.initial_phase < 1:
            raise ValueError("initial_phase must satisfy 0 <= initial_phase < 1")

    def clock(self) -> PhaseClock:
        return PhaseClock(1.0 / self.period_ratio, self.initial_phase)


def activation_count(period_ratio: float, cycles: int, *, phase: float = 0.0) -> int:
    """Return deterministic activation count over ``cycles`` primary ticks."""
    if cycles < 0:
        raise ValueError("cycles must be non-negative")
    clock = PhaseSchedule(period_ratio, phase).clock()
    return sum(clock.tick() for _ in range(cycles))
