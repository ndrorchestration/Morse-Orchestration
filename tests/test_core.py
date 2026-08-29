import pytest

from morse import InterchangeHub, RoutingPolicy, SimulationConfig, make_topology, simulate, summarize
from morse.experiment import period_ratios
from morse.ratios import PLATINUM, SILVER, SQRT2


def test_three_and_four_leaf_topologies_are_complete_graphs():
    assert len(make_topology(3, "uniform").edges) == 3
    assert len(make_topology(4, "uniform").edges) == 6


def test_platinum_ratio_is_preserved_separately_from_integer_periods():
    assert period_ratios(4, "platinum") == pytest.approx((1.0, PLATINUM, PLATINUM**2, PLATINUM**3))
    assert [loop.period for loop in make_topology(4, "platinum").loops] == [1, 2, 3, 6]


def test_binary_periods_match_power_of_two_reference_hierarchy():
    assert [loop.period for loop in make_topology(4, "binary").loops] == [1, 2, 4, 8]


def test_multi_ratio_phase_ratios_are_not_integer_surrogates():
    assert period_ratios(3, "multi_ratio") == pytest.approx((1.0, SQRT2, PLATINUM))
    assert period_ratios(4, "multi_ratio") == pytest.approx((1.0, SQRT2, PLATINUM, SILVER))


def test_event_gate_wakes_slowest_leaf():
    trace = simulate(make_topology(4, "binary"), SimulationConfig(cycles=5, inject_anomaly_every=5))
    events = [a for a in trace.activations if a.reason.value == "event"]
    assert any(a.loop == "L4" and a.cycle == 5 for a in events)


def test_hub_rejects_self_route_by_default():
    hub = InterchangeHub(("L1",), RoutingPolicy())
    event = hub.route(1, "L1", "L1", {"L1"})
    assert not event.accepted
    assert event.reason == "self-route-disallowed"


def test_summary_is_deterministic():
    topology = make_topology(4, "multi_ratio")
    a = summarize(simulate(topology, SimulationConfig(cycles=32)), 32).as_dict()
    b = summarize(simulate(topology, SimulationConfig(cycles=32)), 32).as_dict()
    assert a == b
