from math import sqrt

import pytest

from morse.phase import PhaseAccumulator, PhaseLoopSpec, PhaseScheduler


def test_accumulator_preserves_long_run_frequency():
    acc = PhaseAccumulator(sqrt(2))
    activations = sum(acc.tick() for _ in range(10_000))
    assert activations == 14_142


def test_scheduler_preserves_order_and_average_rate():
    scheduler = PhaseScheduler(
        (
            PhaseLoopSpec("fast", 1.0, 0),
            PhaseLoopSpec("platinum", 1.0 / 1.7747, 1),
            PhaseLoopSpec("silver", 1.0 / (1.0 + sqrt(2)), 2),
        )
    )
    result = scheduler.run(10_000)
    counts = {name: sum(name in active for _, active in result) for name in ("fast", "platinum", "silver")}
    assert counts["fast"] == 10_000
    assert abs(counts["platinum"] - 10_000 / 1.7747) <= 1
    assert abs(counts["silver"] - 10_000 / (1.0 + sqrt(2))) <= 1


def test_invalid_frequency_rejected():
    with pytest.raises(ValueError):
        PhaseAccumulator(0)
    with pytest.raises(ValueError):
        PhaseLoopSpec("x", float("inf"))


def test_duplicate_names_rejected():
    with pytest.raises(ValueError):
        PhaseScheduler((PhaseLoopSpec("x", 1), PhaseLoopSpec("x", 2)))
