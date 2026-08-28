"""Provider-neutral controlled pilot matrix runner.

This executes the synthetic harness only. It is apparatus validation, not an
AI efficacy study and must not be interpreted as evidence for real-world model
performance.
"""
from __future__ import annotations

from dataclasses import asdict
import json
from .harness import run_harness
from .analysis import paired_bootstrap

CONDITIONS = ("C0_uniform", "C1_binary", "C2_platinum", "C3_multi_ratio")
STRENGTH = {"C0_uniform": 0.00, "C1_binary": 0.01, "C2_platinum": 0.02, "C3_multi_ratio": 0.02}


def run_matrix(seeds: list[int], task_count: int = 100) -> dict:
    rows = []
    for topology in (3, 4):
        for seed in seeds:
            for condition in CONDITIONS:
                # Topology is encoded in the condition namespace to ensure
                # independent deterministic solver streams.
                label = f"clover-{topology}:{condition}"
                result = run_harness(seed, label, task_count, STRENGTH[condition])
                rows.append({"topology": topology, "condition": condition, "seed": seed, **asdict(result)})
    return {"status": "synthetic-apparatus-only", "rows": rows}


def compare(matrix: dict, topology: int, treatment: str, baseline: str = "C0_uniform") -> dict:
    selected = [r for r in matrix["rows"] if r["topology"] == topology]
    by_seed = {r["seed"]: r for r in selected}
    deltas = [by_seed[s][treatment]["successes"] / by_seed[s][treatment]["task_count"] - by_seed[s][baseline]["successes"] / by_seed[s][baseline]["task_count"] for s in by_seed]
    estimate = paired_bootstrap(deltas)
    return {"topology": topology, "treatment": treatment, "baseline": baseline, "n": len(deltas), "deltas": deltas, "analysis": asdict(estimate)}


def dumps(matrix: dict) -> str:
    return json.dumps(matrix, sort_keys=True, separators=(",", ":"))
