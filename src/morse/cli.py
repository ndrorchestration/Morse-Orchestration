"""Command-line interface for deterministic MORSE reference runs."""
from __future__ import annotations

import argparse
from pathlib import Path

from .runner import RunConfig, matrix, write_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(prog="morse")
    parser.add_argument("--cycles", type=int, default=128)
    parser.add_argument("--anomaly-every", type=int, default=13)
    parser.add_argument("--output", type=Path, default=Path("morse-reference.jsonl"))
    args = parser.parse_args()
    records = matrix(RunConfig(args.cycles, args.anomaly_every, None))
    write_jsonl(records, args.output)
    print(f"wrote {len(records)} deterministic records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
