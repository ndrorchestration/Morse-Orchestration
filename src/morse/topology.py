"""Canonical 3-leaf and 4-leaf MOLI topology constructors."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .model import LoopSpec


@dataclass(frozen=True)
class Topology:
    name: str
    loops: tuple[LoopSpec, ...]
    edges: tuple[tuple[str, str], ...]

    @property
    def leaf_count(self) -> int:
        return len(self.loops)


def clover_topology(leaf_count: int, periods: tuple[int, ...] | None = None) -> Topology:
    if leaf_count not in (3, 4):
        raise ValueError("MORSE initial topology comparison supports exactly 3 or 4 leaves")
    if periods is None:
        periods = tuple(1 for _ in range(leaf_count))
    if len(periods) != leaf_count:
        raise ValueError("period count must equal leaf count")
    loops = tuple(
        LoopSpec(name=f"L{i+1}", period=periods[i], priority=i, role=f"leaf-{i+1}")
        for i in range(leaf_count)
    )
    edges = tuple(combinations([loop.name for loop in loops], 2))
    return Topology(name=f"clover-{leaf_count}", loops=loops, edges=edges)
