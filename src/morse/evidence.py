"""Evidence and provenance helpers for MORSE synthetic runs."""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from typing import Any, Iterable

from .experiment import Observation


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def observations_digest(rows: Iterable[Observation]) -> str:
    payload = [asdict(row) for row in rows]
    return sha256_text(canonical_json(payload))


def build_manifest(*, commit: str, task_seed: int, task_count: int, repetitions: int, rows: Iterable[Observation], analysis_version: str = "unanalysed") -> dict[str, Any]:
    observations = list(rows)
    return {"schema": "morse.synthetic-evidence.v1", "commit": commit, "task_seed": task_seed, "task_count": task_count, "repetitions": repetitions, "observation_count": len(observations), "observations_sha256": observations_digest(observations), "analysis_version": analysis_version}
