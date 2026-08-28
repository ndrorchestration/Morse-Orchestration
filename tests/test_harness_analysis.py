from morse.analysis import paired_bootstrap
from morse.harness import generate_tasks, run_harness
from morse.paired import run_paired


def test_task_generation_is_deterministic():
    assert generate_tasks(42, 5) == generate_tasks(42, 5)


def test_harness_is_deterministic():
    a = run_harness(42, "C0", 50, 0.0)
    b = run_harness(42, "C0", 50, 0.0)
    assert a == b


def test_pair_reuses_task_population():
    result = run_paired(42, "C0", 0.0, "C2", 0.1, 25)
    assert result.a.task_count == result.b.task_count == 25
    assert result.condition_a != result.condition_b


def test_bootstrap_is_deterministic_and_directional():
    result = paired_bootstrap([0.2] * 20, resamples=1000, seed=7)
    assert result == paired_bootstrap([0.2] * 20, resamples=1000, seed=7)
    assert result.directional_support


def test_bootstrap_rejects_empty_input():
    try:
        paired_bootstrap([])
    except ValueError:
        pass
    else:
        raise AssertionError("empty input must fail")
