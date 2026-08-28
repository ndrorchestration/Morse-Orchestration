from morse.analysis import paired_bootstrap
from morse.harness import generate_tasks, run_harness
from morse.paired import run_paired


def test_task_generation_is_reproducible():
    assert generate_tasks(7, 20) == generate_tasks(7, 20)


def test_harness_is_reproducible():
    a = run_harness(7, "C0_uniform", 25, 0.0)
    b = run_harness(7, "C0_uniform", 25, 0.0)
    assert a == b


def test_paired_run_uses_same_task_population():
    result = run_paired(7, "A", 0.0, "B", 0.0, 25)
    assert [x.task_id for x in result.a.outcomes] == [x.task_id for x in result.b.outcomes]


def test_bootstrap_is_reproducible_and_directional():
    estimate = paired_bootstrap([0.1, 0.2, 0.15, 0.05], resamples=1000, seed=9)
    same = paired_bootstrap([0.1, 0.2, 0.15, 0.05], resamples=1000, seed=9)
    assert estimate == same
    assert estimate.directional_support
