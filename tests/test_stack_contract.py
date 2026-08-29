import math

import pytest

from morse.analysis import paired_bootstrap
from morse.evidence import observations_digest
from morse.experiment import paired_matrix
from morse.metrics import summarize
from morse.model import SimulationTrace
from morse.phase import PhaseScheduler, PhaseLoopSpec
from morse.run import execute_synthetic, validate_observations


def test_phase_to_matrix_contract():
    scheduler = PhaseScheduler((PhaseLoopSpec("L1", 1.0), PhaseLoopSpec("L2", 0.5)))
    trace = scheduler.run(4)
    assert trace == [(1, ["L1"]), (2, ["L1", "L2"]), (3, ["L1"]), (4, ["L1", "L2"])]


def test_evidence_digest_is_order_sensitive_at_record_level():
    rows = paired_matrix(11, task_count=1, repetitions=1)
    assert observations_digest(rows) == observations_digest(list(rows))
    assert observations_digest(rows) != observations_digest(list(reversed(rows)))


def test_analysis_rejects_nonfinite_input():
    with pytest.raises(ValueError, match="finite"):
        paired_bootstrap([0.1, math.nan])


def test_metrics_rejects_snapshot_mismatch():
    with pytest.raises(ValueError, match="snapshots"):
        summarize(SimulationTrace(), cycles=1)


def test_full_small_run_contract():
    result = execute_synthetic(commit="contract", task_seed=11, task_count=2, repetitions=1)
    assert result["manifest"]["observation_count"] == 16
    observations = [
        __import__("morse.experiment", fromlist=["Observation"]).Observation(**row)
        for row in result["observations"]
    ]
    validate_observations(observations, 2, 1)
