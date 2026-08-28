"""Stable JSON evidence records and SHA-256 manifest helpers."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "morse-evidence-v1"


def evidence_record(*, project: str, run_id: str, topology: str, regime: str, cycles: int, metrics: dict[str, Any], periods: list[int], seed: int | None = None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "project": project,
        "run_id": run_id,
        "seed": seed,
        "topology": topology,
        "regime": regime,
        "cycles": cycles,
        "periods": periods,
        "metrics": metrics,
    }


def validate_record(record: dict[str, Any]) -> None:
    required = {"schema_version", "project", "run_id", "topology", "regime", "cycles", "periods", "metrics"}
    missing = required - record.keys()
    if missing:
        raise ValueError(f"evidence record missing fields: {sorted(missing)}")
    if record["schema_version"] != SCHEMA_VERSION:
        raise ValueError("unsupported evidence schema version")
    if not isinstance(record["cycles"], int) or record["cycles"] < 0:
        raise ValueError("cycles must be a non-negative integer")
    if not isinstance(record["periods"], list) or not all(isinstance(x, int) and x >= 1 for x in record["periods"]):
        raise ValueError("periods must be a list of positive integers")
    if not isinstance(record["metrics"], dict):
        raise ValueError("metrics must be an object")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
