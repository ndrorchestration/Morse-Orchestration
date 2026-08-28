"""Phase-accumulator scheduling for irrational and non-integer cadences."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class PhaseLoopSpec:
    """One loop's normalized activation frequency.

    A frequency of 1.0 means one activation per primary cycle on average.
    Frequencies above 1.0 may produce multiple activations in a cycle.
    """

    name: str
    frequency: float
    priority: int = 0

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("loop name must be non-empty")
        if not isfinite(self.frequency) or self.frequency <= 0:
            raise ValueError("frequency must be finite and > 0")


@dataclass
class PhaseAccumulator:
    """Deterministic accumulator preserving the requested long-run frequency."""

    frequency: float
    phase: float = 0.0

    def __post_init__(self) -> None:
        if not isfinite(self.frequency) or self.frequency <= 0:
            raise ValueError("frequency must be finite and > 0")
        if not isfinite(self.phase) or self.phase < 0:
            raise ValueError("phase must be finite and >= 0")

    def tick(self) -> int:
        """Advance one primary cycle and return the number of activations."""
        self.phase += self.frequency
        activations = int(self.phase)
        self.phase -= activations
        return activations


class PhaseScheduler:
    """Independent phase clocks evaluated against a common primary cycle."""

    def __init__(self, loops: tuple[PhaseLoopSpec, ...]):
        names = [loop.name for loop in loops]
        if len(names) != len(set(names)):
            raise ValueError("loop names must be unique")
        self.loops = tuple(sorted(loops, key=lambda x: (x.priority, x.name)))
        self.accumulators = {loop.name: PhaseAccumulator(loop.frequency) for loop in self.loops}
        self.cycle = 0

    def tick(self) -> list[str]:
        self.cycle += 1
        active: list[str] = []
        for loop in self.loops:
            if self.accumulators[loop.name].tick() > 0:
                active.append(loop.name)
        return active

    def run(self, cycles: int) -> list[tuple[int, list[str]]]:
        if cycles < 0:
            raise ValueError("cycles must be non-negative")
        return [(self.cycle + 1, self.tick()) for _ in range(cycles)]
