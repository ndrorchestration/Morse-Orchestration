"""Experiment configuration and deterministic regime construction."""
from __future__ import annotations

from dataclasses import dataclass

from .ratios import PLATINUM, rounded_periods
from .topology import Topology, clover_topology


@dataclass(frozen=True)
class Regime:
    name: str
    topology: str
    periods: tuple[int, ...]
    rationale: str


UNIFORM = "uniform"
BINARY = "binary"
PLATINUM_REGIME = "platinum"
MULTI_RATIO = "multi_ratio"


def regime(topology: int, name: str) -> Regime:
    if topology not in (3, 4):
        raise ValueError("topology must be 3 or 4 leaves")
    if name == UNIFORM:
        periods = tuple(1 for _ in range(topology))
        rationale = "Equal cadence baseline."
    elif name == BINARY:
        periods = tuple(2 ** i for i in range(topology))
        rationale = "Power-of-two temporal hierarchy."
    elif name == PLATINUM_REGIME:
        periods = rounded_periods(1.0, PLATINUM, topology)
        rationale = "Geometric cadence using the project-defined Platinum Mean."
    elif name == MULTI_RATIO:
        # Deterministic integer surrogate for heterogeneous clocks. The
        # reference apparatus uses a declared quantization ladder rather than
        # pretending that irrational ratios can be represented exactly by
        # integer periods. Continuous/phase-accumulator scheduling is a later
        # engineering layer.
        surrogate = (1, 2, 3, 5)
        periods = surrogate[:topology]
        rationale = (
            "Heterogeneous surrogate clocks corresponding to sqrt(2), Platinum, "
            "and Silver; integer periods are a reproducibility baseline, not exact ratio representations."
        )
    else:
        raise ValueError(f"unknown regime: {name}")
    return Regime(name=name, topology=f"clover-{topology}", periods=periods, rationale=rationale)


def make_topology(leaf_count: int, regime_name: str) -> Topology:
    cfg = regime(leaf_count, regime_name)
    return clover_topology(leaf_count, cfg.periods)
