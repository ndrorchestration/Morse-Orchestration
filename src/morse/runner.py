"""Reference matrix runner producing deterministic JSON evidence."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .evidence import evidence_record, validate_record
from .experiment import BINARY, MULTI_RATIO, PLATINUM_REGIME, UNIFORM, make_topology
from .metrics import summarize
from .simulation import SimulationConfig, simulate


REGIMES = (UNIFORM, BINARY, PLATINUM_REGIME, MULTI_RATIO)


@dataclass(frozen=True)
class RunConfig:
    cycles: int = 128
    anomaly_every: int | None = 13
    seed: int | None = None


def matrix(config: RunConfig = RunConfig()) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for leaves in (3, 4):
        for regime_name in REGIMES:
            topology = make_topology(leaves, regime_name)
            trace = simulate(topology, SimulationConfig(config.cycles, config.anomaly_every))
            record = evidence_record(
                project="MORSE",
                run_id=f"ref-{leaves}-{regime_name}",
                topology=topology.name,
                regime=regime_name,
                cycles=config.cycles,
                periods=[loop.period for loop in topology.loops],
                metrics=summarize(trace, config.cycles).as_dict(),
                seed=config.seed,
            )
            validate_record(record)
            records.append(record)
    return records


def write_jsonl(records: list[dict[str, object]], path: str | Path) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, sort_keys=True) + "\n")
