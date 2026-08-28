"""Derived deterministic metrics for scheduler traces."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .model import SimulationTrace


@dataclass(frozen=True)
class TraceMetrics:
    cycles: int
    total_activations: int
    activations_by_loop: dict[str, int]
    event_activations: int
    periodic_activations: int
    interchanges: int
    accepted_interchanges: int
    rejected_interchanges: int
    activation_density: float
    interchange_acceptance_rate: float

    def as_dict(self) -> dict[str, object]:
        return {
            "cycles": self.cycles,
            "total_activations": self.total_activations,
            "activations_by_loop": self.activations_by_loop,
            "event_activations": self.event_activations,
            "periodic_activations": self.periodic_activations,
            "interchanges": self.interchanges,
            "accepted_interchanges": self.accepted_interchanges,
            "rejected_interchanges": self.rejected_interchanges,
            "activation_density": self.activation_density,
            "interchange_acceptance_rate": self.interchange_acceptance_rate,
        }


def summarize(trace: SimulationTrace, cycles: int) -> TraceMetrics:
    counts = Counter(a.loop for a in trace.activations)
    events = sum(a.reason.value == "event" for a in trace.activations)
    periodic = sum(a.reason.value == "periodic" for a in trace.activations)
    accepted = sum(e.accepted for e in trace.interchanges if e.action == "route")
    rejected = sum(not e.accepted for e in trace.interchanges if e.action == "route")
    routed = accepted + rejected
    return TraceMetrics(
        cycles=cycles,
        total_activations=len(trace.activations),
        activations_by_loop=dict(sorted(counts.items())),
        event_activations=events,
        periodic_activations=periodic,
        interchanges=routed,
        accepted_interchanges=accepted,
        rejected_interchanges=rejected,
        activation_density=(len(trace.activations) / cycles) if cycles else 0.0,
        interchange_acceptance_rate=(accepted / routed) if routed else 0.0,
    )
