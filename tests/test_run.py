import pytest

from morse.experiment import Observation, period_ratios, paired_matrix
from morse.ratios import PLATINUM, SILVER, SQRT2
from morse.run import execute_synthetic, validate_observations


def test_execute_synthetic_cardinality_and_manifest():
    result = execute_synthetic(commit="abc123", task_seed=7, task_count=3, repetitions=2)
    assert result["manifest"]["observation_count"] == 3 * 2 * 2 * 4
    assert result["manifest"]["commit"] == "abc123"
    assert len(result["observations"]) == 48


def test_validate_rejects_incomplete_matrix():
    row = Observation(0, "T0000", "L3-C0", 1, True, 1, 1, 0)
    with pytest.raises(ValueError, match="observation count"):
        validate_observations([row], task_count=1, repetitions=1)


def test_repetition_is_part_of_observation_identity():
    rows = paired_matrix(7, task_count=1, repetitions=2)
    identities = {(r.repetition, r.task_id, r.condition) for r in rows}
    assert len(identities) == len(rows)
    assert {r.repetition for r in rows} == {0, 1}


def test_candidate_ratios_are_phase_backed():
    assert period_ratios(3, "platinum") == pytest.approx((1.0, PLATINUM, PLATINUM**2))
    assert period_ratios(4, "multi_ratio") == pytest.approx((1.0, SQRT2, PLATINUM, SILVER))


def test_matrix_is_deterministic():
    a = paired_matrix(20260828, task_count=2, repetitions=2)
    b = paired_matrix(20260828, task_count=2, repetitions=2)
    assert a == b
