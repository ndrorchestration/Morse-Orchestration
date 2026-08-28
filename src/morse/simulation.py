"""Reference deterministic MOLI simulation without an AI provider."""
from __future__ import annotations

from dataclasses import dataclass

from .hub import InterchangeHub
from .model import Gate, SimulationTrace
from .scheduler import Scheduler
from .topology import Topology


@dataclass(frozen=True)
class SimulationConfig:
    cycles: int = 128
    inject_anomaly_every: int | None = None
    route_ring: bool = True


def simulate(topology: Topology, config: SimulationConfig = SimulationConfig()) -> SimulationTrace:
    if config.cycles < 0:
        raise ValueError("cycles must be >= 0")
    names = tuple(loop.name for loop in topology.loops)
    anomaly_target = topology.loops[-1].name

    def anomaly_gate(cycle: int, active: frozenset[str]) -> bool:
        return (
            config.inject_anomaly_every is not None
            and config.inject_anomaly_every > 0
            and cycle % config.inject_anomaly_every == 0
        )

    scheduler = Scheduler(
        topology.loops,
        gates=(Gate("synthetic-anomaly", anomaly_gate, anomaly_target, priority=-100),),
    )
    trace = scheduler.trace(config.cycles)
    hub = InterchangeHub(names)

    for snapshot in trace.snapshots:
        cycle = int(snapshot["cycle"])
        active = set(snapshot["active_loops"])
        hub.state.active_loops = active
        hub.reconcile(cycle, active, trace)
        if config.route_ring and active:
            ordered = [n for n in names if n in active]
            for source, target in zip(ordered, ordered[1:] + ordered[:1]):
                hub.route(cycle, source, target, active, payload={"cycle": cycle}, trace=trace)
    return trace
