from morse.synthetic import (
    MULTI_RATIO,
    PLATINUM_REGIME,
    UNIFORM,
    BINARY,
    derive_seed,
    paired_matrix,
    period_ratios,
    schedule_trace,
)
from morse.ratios import PLATINUM, SILVER, SQRT2


def test_period_ratios_are_distinct_for_candidate_regimes():
    assert period_ratios(3, UNIFORM) == (1.0, 1.0, 1.0)
    assert period_ratios(3, BINARY) == (1.0, 2.0, 4.0)
    assert period_ratios(3, PLATINUM_REGIME) == (1.0, PLATINUM, PLATINUM**2)
    assert period_ratios(3, MULTI_RATIO) == (1.0, SQRT2, PLATINUM)
    assert period_ratios(4, MULTI_RATIO) == (1.0, SQRT2, PLATINUM, SILVER)


def test_phase_trace_is_deterministic():
    assert schedule_trace(4, MULTI_RATIO, 64) == schedule_trace(4, MULTI_RATIO, 64)


def test_seed_derivation_is_stable_and_condition_specific():
    a = derive_seed(123, "T0001", "L3-C2")
    assert a == derive_seed(123, "T0001", "L3-C2")
    assert a != derive_seed(123, "T0001", "L4-C2")


def test_paired_matrix_has_expected_cardinality():
    rows = paired_matrix(20260829, task_count=2, repetitions=3)
    assert len(rows) == 3 * 2 * 4 * 2
    assert {r.leaf_count for r in rows} == {3, 4}
    assert {r.regime for r in rows} == {UNIFORM, BINARY, PLATINUM_REGIME, MULTI_RATIO}


def test_task_difficulty_does_not_change_scheduler_trace():
    trace_a = schedule_trace(3, MULTI_RATIO, 32)
    trace_b = schedule_trace(3, MULTI_RATIO, 32)
    assert trace_a == trace_b
