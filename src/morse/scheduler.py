"""Deterministic multi-loop scheduler for MOLI."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .model import Activation, Gate, GateReason, LoopSpec, SimulationTrace

GatePredicate = Callable[[int, frozenset[str]], bool]


@dataclass
class Scheduler:
    loops: tuple[LoopSpec, ...]
    gates: tuple[Gate, ...] = ()
    cycle: int = 0
    events: list[tuple[int, str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        names = [loop.name for loop in self.loops]
        if len(names) != len(set(names)):
            raise ValueError("loop names must be unique")
        loop_names = set(names)
        missing = {gate.target_loop for gate in self.gates} - loop_names
        if missing:
            raise ValueError(f"gate targets unknown loops: {sorted(missing)}")

    def tick(self) -> list[str]:
        """Advance one primary cycle and return loops activated this cycle."""
        self.cycle += 1
        active = {loop.name for loop in self.loops if loop.enabled and self.cycle % loop.period == 0}
        for gate in sorted(self.gates, key=lambda g: (g.priority, g.name)):
            predicate = gate.predicate
            try:
                fired = bool(predicate(self.cycle, frozenset(active)))
            except TypeError:
                fired = bool(predicate(self.cycle))
            if fired:
                active.add(gate.target_loop)
                self.events.append((self.cycle, gate.name, gate.target_loop))
        rank = {loop.name: (loop.priority, loop.name) for loop in self.loops}
        return sorted(active, key=lambda name: rank[name])

    def run(self, cycles: int) -> list[tuple[int, list[str]]]:
        if cycles < 0:
            raise ValueError("cycles must be non-negative")
        return [(self.cycle + 1, self.tick()) for _ in range(cycles)]

    def trace(self, cycles: int) -> SimulationTrace:
        trace = SimulationTrace()
        for _ in range(cycles):
            active = self.tick()
            periodic = {loop.name for loop in self.loops if self.cycle % loop.period == 0}
            for loop in active:
                reason = GateReason.PERIODIC if loop in periodic else GateReason.EVENT
                trigger = "cadence" if reason is GateReason.PERIODIC else "gate"
                trace.activations.append(Activation(self.cycle, loop, reason, trigger))
            trace.snapshots.append({"cycle": self.cycle, "active_loops": list(active)})
        return trace
