"""Fault injection primitives for later recovery experiments."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fault:
    cycle: int
    loop: str
    kind: str


class FaultPlan:
    def __init__(self, faults: tuple[Fault, ...] = ()) -> None:
        if any(f.cycle < 1 for f in faults):
            raise ValueError("fault cycle must be >= 1")
        self._faults = faults

    def at(self, cycle: int, loop: str) -> tuple[Fault, ...]:
        return tuple(f for f in self._faults if f.cycle == cycle and f.loop == loop)
