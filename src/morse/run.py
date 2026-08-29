"""Execute and validate a complete deterministic MORSE synthetic run."""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .evidence import build_manifest
from .experiment import Observation, paired_matrix

EXPECTED_LEAVES = (3, 4)
EXPECTED_REGIMES = ("C0", "C1", "C2", "C3")


def validate_observations(rows: list[Observation], task_count: int, repetitions: int) -> None:
    expected = task_count * repetitions * len(EXPECTED_LEAVES) * len(EXPECTED_REGIMES)
    if len(rows) != expected:
        raise ValueError(f"observation count {len(rows)} != expected {expected}")
    expected_per_condition = task_count * repetitions
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.condition] = counts.get(row.condition, 0) + 1
        if not row.task_id.startswith("T"):
            raise ValueError("invalid task identifier")
        if row.condition[:1] != "L" or row.condition[2:] not in EXPECTED_REGIMES:
            raise ValueError(f"invalid condition: {row.condition}")
    expected_conditions = {f"L{leaf}-{regime}" for leaf in EXPECTED_LEAVES for regime in EXPECTED_REGIMES}
    if set(counts) != expected_conditions:
        raise ValueError("condition matrix is incomplete")
    if any(count != expected_per_condition for count in counts.values()):
        raise ValueError("condition cardinality mismatch")


def execute_synthetic(*, commit: str, task_seed: int, task_count: int = 100, repetitions: int = 50) -> dict[str, Any]:
    rows = paired_matrix(task_seed, task_count, repetitions)
    validate_observations(rows, task_count, repetitions)
    manifest = build_manifest(commit=commit, task_seed=task_seed, task_count=task_count, repetitions=repetitions, rows=rows)
    return {"manifest": manifest, "observations": [asdict(row) for row in rows]}
