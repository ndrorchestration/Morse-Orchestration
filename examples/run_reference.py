from __future__ import annotations

import json

from morse import SimulationConfig, make_topology, simulate, summarize

for leaves in (3, 4):
    for regime_name in ("uniform", "binary", "platinum", "multi_ratio"):
        topology = make_topology(leaves, regime_name)
        trace = simulate(topology, SimulationConfig(cycles=128, inject_anomaly_every=13))
        print(json.dumps({
            "leaves": leaves,
            "regime": regime_name,
            "periods": [loop.period for loop in topology.loops],
            "metrics": summarize(trace, 128).as_dict(),
        }, sort_keys=True))
