from morse.synthetic import MULTI_RATIO, PLATINUM_REGIME, schedule_trace, period_ratios
from morse.phase import activation_count


def test_platinum_frequency_is_phase_preserved_over_long_run():
    ratio = period_ratios(3, PLATINUM_REGIME)[1]
    observed = activation_count(ratio, 10000) / 10000
    assert abs(observed - 1.0 / ratio) < 1e-4


def test_multi_ratio_trace_contains_real_phase_schedule_events():
    trace = schedule_trace(4, MULTI_RATIO, 64)
    assert any(len(active) >= 2 for _, active in trace)
    assert any(len(active) == 1 for _, active in trace)
