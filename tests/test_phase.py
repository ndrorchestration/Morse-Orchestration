import math

import pytest

from morse.phase import PhaseAccumulator, PhaseClock, PhaseSchedule, activation_count, frequency_for_ratio


def test_platinum_long_run_frequency_is_preserved():
    ratio = 1.0 / (2.0 * math.sin(math.pi / 11.0))
    cycles = 100_000
    observed = activation_count(ratio, cycles) / cycles
    assert abs(observed - 1.0 / ratio) < 1.0 / cycles


def test_sqrt2_long_run_frequency_is_preserved():
    cycles = 100_000
    observed = activation_count(math.sqrt(2.0), cycles) / cycles
    assert abs(observed - 1.0 / math.sqrt(2.0)) < 1.0 / cycles


def test_phase_is_deterministic():
    a = PhaseAccumulator(1 / 1.7747)
    b = PhaseAccumulator(1 / 1.7747)
    trace_a = [a.tick() for _ in range(100)]
    trace_b = [b.tick() for _ in range(100)]
    assert trace_a == trace_b


def test_phase_scheduler_is_deterministic():
    from morse.phase import PhaseLoopSpec, PhaseScheduler
    loops = (PhaseLoopSpec("a", frequency_for_ratio(1.7747)), PhaseLoopSpec("b", frequency_for_ratio(math.sqrt(2))))
    assert PhaseScheduler(loops).run(1000) == PhaseScheduler(loops).run(1000)


def test_invalid_frequency_rejected():
    with pytest.raises(ValueError):
        PhaseClock(0)
    with pytest.raises(ValueError):
        PhaseClock(1.1)


def test_invalid_period_rejected():
    with pytest.raises(ValueError):
        PhaseSchedule(0.5)
