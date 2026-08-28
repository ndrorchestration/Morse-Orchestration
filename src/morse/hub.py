"""Central MOLI interchange hub and explicit routing semantics."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .model import HubState, InterchangeEvent, SimulationTrace


@dataclass(frozen=True)
class RoutingPolicy:
    """Deterministic routing policy used by the reference simulator."""

    allow_self: bool = False
    require_active_source: bool = True

    def accept(self, source: str, target: str, active: set[str]) -> tuple[bool, str]:
        if not self.allow_self and source == target:
            return False, "self-route-disallowed"
        if self.require_active_source and source not in active:
            return False, "source-not-active"
        return True, "accepted"


class InterchangeHub:
    """Small state machine representing the central roundabout.

    The hub does not execute agent logic. It records and arbitrates exchanges.
    That separation makes the topology independently testable.
    """

    def __init__(self, loops: tuple[str, ...], policy: RoutingPolicy | None = None) -> None:
        if len(set(loops)) != len(loops):
            raise ValueError("hub loop names must be unique")
        self.loops = frozenset(loops)
        self.policy = policy or RoutingPolicy()
        self.state = HubState()

    def route(
        self,
        cycle: int,
        source: str,
        target: str,
        active: set[str],
        payload: Mapping[str, Any] | None = None,
        trace: SimulationTrace | None = None,
    ) -> InterchangeEvent:
        if source not in self.loops or target not in self.loops:
            raise ValueError("source and target must be registered hub loops")
        accepted, reason = self.policy.accept(source, target, active)
        self.state.cycle = cycle
        self.state.messages_seen += 1
        if accepted:
            self.state.messages_accepted += 1
            self.state.revision += 1
        else:
            self.state.messages_rejected += 1
        event = InterchangeEvent(
            cycle=cycle,
            source=source,
            target=target,
            action="route",
            accepted=accepted,
            reason=reason,
            payload=dict(payload or {}),
        )
        if trace is not None:
            trace.interchanges.append(event)
        return event

    def reconcile(self, cycle: int, active: set[str], trace: SimulationTrace | None = None) -> InterchangeEvent:
        """Record a deterministic hub reconciliation boundary.

        Reconciliation itself is intentionally provider/model agnostic.
        """
        self.state.cycle = cycle
        self.state.active_loops = set(active)
        event = InterchangeEvent(
            cycle=cycle,
            source="hub",
            target="hub",
            action="reconcile",
            accepted=True,
            reason="state-boundary",
            payload={"active_loops": sorted(active), "revision": self.state.revision},
        )
        if trace is not None:
            trace.interchanges.append(event)
        return event
