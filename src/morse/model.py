"""Core domain models for the MORSE/MOLI research apparatus."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class GateReason(str, Enum):
    PERIODIC = "periodic"
    EVENT = "event"


@dataclass(frozen=True)
class LoopSpec:
    """Static specification for one orchestration loop."""

    name: str
    period: int = 1
    priority: int = 0
    role: str = "generic"
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("loop name must be non-empty")
        if self.period < 1:
            raise ValueError("loop period must be >= 1")


@dataclass(frozen=True)
class Gate:
    """A condition that can wake another loop independently of cadence."""

    name: str
    predicate: Any
    target_loop: str
    priority: int = 0

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("gate name must be non-empty")
        if not self.target_loop:
            raise ValueError("gate target_loop must be non-empty")


@dataclass(frozen=True)
class Activation:
    cycle: int
    loop: str
    reason: GateReason
    trigger: str


@dataclass(frozen=True)
class InterchangeEvent:
    cycle: int
    source: str
    target: str
    action: str
    accepted: bool
    reason: str
    payload: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class HubState:
    """Minimal serializable state for the central interchange hub."""

    cycle: int = 0
    messages_seen: int = 0
    messages_accepted: int = 0
    messages_rejected: int = 0
    revision: int = 0
    active_loops: set[str] = field(default_factory=set)
    state: dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationTrace:
    """Machine-readable evidence trace from one deterministic run."""

    activations: list[Activation] = field(default_factory=list)
    interchanges: list[InterchangeEvent] = field(default_factory=list)
    snapshots: list[dict[str, Any]] = field(default_factory=list)

    def activation_count(self, loop: str | None = None) -> int:
        if loop is None:
            return len(self.activations)
        return sum(a.loop == loop for a in self.activations)
