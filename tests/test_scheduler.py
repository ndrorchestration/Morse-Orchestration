from morse.scheduler import Gate, LoopSpec, Scheduler


def test_binary_cadence():
    s = Scheduler((LoopSpec("L1", 1), LoopSpec("L2", 8), LoopSpec("L3", 16), LoopSpec("L4", 32)))
    rows = s.run(32)
    assert rows[7][1] == ["L1", "L2"]
    assert rows[15][1] == ["L1", "L2", "L3"]
    assert rows[31][1] == ["L1", "L2", "L3", "L4"]


def test_event_gate_can_wake_slow_loop_early():
    s = Scheduler(
        (LoopSpec("L1", 1), LoopSpec("L4", 32)),
        (Gate("anomaly", lambda c: c == 5, "L4"),),
    )
    rows = s.run(5)
    assert rows[4][1] == ["L1", "L4"]
    assert s.events == [(5, "anomaly", "L4")]
