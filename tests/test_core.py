from morse import InterchangeHub, RoutingPolicy, SimulationConfig, make_topology, simulate, summarize


def test_three_and_four_leaf_topologies_are_complete_graphs():
    assert len(make_topology(3, "uniform").edges) == 3
    assert len(make_topology(4, "uniform").edges) == 6


def test_platinum_periods_are_deterministic():
    assert [loop.period for loop in make_topology(4, "platinum").loops] == [1, 2, 3, 6]


def test_binary_periods_match_power_of_two_hierarchy():
    assert [loop.period for loop in make_topology(4, "binary").loops] == [1, 2, 4, 8]


def test_multi_ratio_uses_declared_integer_surrogate_ladder():
    periods3 = [loop.period for loop in make_topology(3, "multi_ratio").loops]
    periods4 = [loop.period for loop in make_topology(4, "multi_ratio").loops]
    assert periods3 == [1, 2, 3]
    assert periods4 == [1, 2, 3, 5]
    assert periods4 == sorted(set(periods4))


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
