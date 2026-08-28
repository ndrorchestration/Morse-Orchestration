# MORSE Experimental Specification v0.2

## 1. Name

**MORSE — Multi-Orbital Resonance Scheduling Experiment**

MORSE evaluates **MOLI — Multi-Orbital Loop Interchange**, a hierarchical communication/scheduling topology for AI orchestration.

## 2. Research question

Does multi-timescale loop scheduling with conditional interchange through a shared hub produce measurable improvements over conventional scheduling under equivalent task and compute constraints?

## 3. Hypotheses

**H0:** Ratio-based or heterogeneous scheduling does not improve the predefined outcomes relative to the selected baseline.

**H1:** At least one ratio-based scheduling regime produces a predefined improvement in one or more primary outcomes without unacceptable cost or instability.

No ratio is presumed optimal.

## 4. Experimental factors

### Factor A — leaf count

- 3 leaves
- 4 leaves

### Factor B — scheduling regime

- C0 Uniform
- C1 Binary
- C2 Platinum
- C3 Multi-ratio

Initial design: **2 × 4 = 8 conditions**.

## 5. Operational model

Each loop has an objective, state, cadence, role, and gate policy.

The interchange hub performs explicit receive/classify/arbitrate/route/reconcile operations and emits a machine-readable event trace.

Activation can occur from periodic cadence or a gate predicate. Gate evaluation may use cycle number and the currently active set.

## 6. Primary reference apparatus

The provider-independent simulator is the first validation layer. A reference sweep uses 128 primary cycles and can inject a deterministic synthetic anomaly every 13 cycles.

The simulator is not evidence of AI efficacy. It establishes that the scheduling and interchange apparatus behaves deterministically and reproducibly.

## 7. Candidate regimes

### C0 — Uniform
All leaves use a one-cycle cadence.

### C1 — Binary
Cadences follow powers of two: `1, 2, 4, 8, ...`.

### C2 — Platinum
Temporal scales follow a geometric progression using the project-defined Platinum Mean:

`pP = 1/(2 sin(pi/11)) ≈ 1.7747`

Integer periods are produced using a declared deterministic rounding rule.

### C3 — Multi-ratio
The candidate clocks are `1`, `sqrt(2)`, Platinum, and Silver. The current deterministic reference uses the declared integer surrogate ladder `[1, 2, 3, 5]`; this is not an exact representation of irrational ratios.

## 8. Outcomes

Primary candidates: task success/quality, latency, compute/token cost.

Secondary candidates: unnecessary activations, recovery time, disagreement/revision frequency, convergence/stability, failure propagation, and hub contention.

## 9. Controls

Provider-level comparisons must hold constant, where practical, the task set, model/provider, tools, context budget, wall-clock budget, stopping criteria, randomization policy, and fault-injection policy.

## 10. Scientific boundary

Mathematical elegance is not evidence of performance. Ratio choice, leaf count, and the cloverleaf metaphor are hypotheses/design parameters. Any claim of benefit requires controlled empirical evidence.
