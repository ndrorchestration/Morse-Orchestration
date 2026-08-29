import pytest

from morse.run import execute_synthetic, validate_observations
from morse.experiment import Observation


def test_execute_synthetic_cardinality_and_manifest():
    result = execute_synthetic(commit="abc123", task_seed=7, task_count=3, repetitions=2)
    assert result["manifest"]["observation_count"] == 3 * 2 * 2 * 4
    assert result["manifest"]["commit"] == "abc123"
    assert len(result["observations"]) == 48


def test_validate_rejects_incomplete_matrix():
    row = Observation("T0000", "L3-C0", 1, True, 1, 1, 0)
    with pytest.raises(ValueError, match="observation count"):
        validate_observations([row], task_count=1, repetitions=1)
