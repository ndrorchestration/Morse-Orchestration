"""Phase-accumulator scheduling for irrational and non-integer cadences."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class PhaseLoopSpec:
    """One loop's normalized activation frequency."""
    name: str
    frequency: float
    priority: int = 0

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("loop name must be non-empty")
        if not isfinite(self.frequency) or self.frequency <= 0 or self.frequency > 1:
            raise ValueError("frequency must be finite and in (0, 1]")


@dataclass
class PhaseAccumulator:
    """Deterministic accumulator preserving long-run activation frequency."""
    frequency: float
    phase: float = 0.0

    def __post_init__(self) -> None:
        if not isfinite(self.frequency) or self.frequency <= 0 or self.frequency > 1:
            raise ValueError("frequency must be finite and in (0, 1]")
        if not isfinite(self.phase) or self.phase < 0:
            raise ValueError("phase must be finite and >= 0")

    def tick(self) -> int:
        self.phase += self.frequency
        activations = int(self.phase)
        self.phase -= activations
        return activations


class PhaseScheduler:
    """Independent phase clocks evaluated against one primary cycle."""

    def __init__(self, loops: tuple[PhaseLoopSpec, ...]):
        names = [loop.name for loop in loops]
        if len(names) != len(set(names)):
            raise ValueError("loop names must be unique")
        self.loops = tuple(sorted(loops, key=lambda x: (x.priority, x.name)))
        self.accumulators = {loop.name: PhaseAccumulator(loop.frequency) for loop in self.loops}
        self.cycle = 0

    def tick(self) -> list[str]:
        self.cycle += 1
        return [
            loop.name for loop in self.loops
            if self.accumulators[loop.name].tick() > 0
        ]

    def run(self, cycles: int) -> list[tuple[int, list[str]]]:
        if cycles < 0:
            raise ValueError("cycles must be non-negative")
        return [(self.cycle + 1, self.tick()) for _ in range(cycles)]


def frequency_for_ratio(period_ratio: float) -> float:
    """Convert a period ratio into activations per primary cycle."""
    if not isfinite(period_ratio) or period_ratio < 1:
        raise ValueError("period_ratio must be finite and >= 1")
    return 1.0 / period_ratio


def activation_count(period_ratio: float, cycles: int) -> int:
    """Count activations over a deterministic finite run."""
    if cycles < 0:
        raise ValueError("cycles must be non-negative")
    accumulator = PhaseAccumulator(frequency_for_ratio(period_ratio))
    return sum(accumulator.tick() for _ in range(cycles))


# Compatibility aliases retained for the original API vocabulary.
PhaseClock = PhaseAccumulator


@dataclass(frozen=True)
class PhaseSchedule:
    """Compatibility wrapper representing one period ratio."""
    period_ratio: float

    def __post_init__(self) -> None:
        frequency_for_ratio(self.period_ratio)
