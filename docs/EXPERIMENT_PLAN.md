# MORSE Experimental Plan v0.2

## Primary comparison

Factor A: **leaf count**

- 3 leaves
- 4 leaves

Factor B: **temporal regime**

- C0 Uniform
- C1 Binary
- C2 Platinum
- C3 Multi-ratio

C3 uses heterogeneous candidate clocks corresponding to `1`, `sqrt(2)`, Platinum, and Silver. The current deterministic apparatus uses the declared integer surrogate ladder `[1, 2, 3, 5]`; this is a reproducibility baseline, not an exact representation of irrational ratios. A phase-accumulator scheduler is reserved for the next layer so average frequencies can be represented without integer-period aliasing.

This creates an initial `2 × 4` topology/scheduling matrix.

## Reference runs

First validate the deterministic apparatus without an AI model.

Recommended reference horizon: 128 primary cycles.

Recommended injected-event test: synthetic anomaly every 13 cycles.

The reference run should confirm exact cadence, event-gate behavior, hub routing, reproducibility, and trace serialization before any model/provider is introduced. It is deterministic without an RNG; stochastic seeds are reserved for the later AI/task harness.

## AI-provider phase

When the deterministic layer is stable, add a provider-neutral task harness. Hold constant, as practical:

- task suite;
- provider/model;
- tools;
- context budget;
- maximum wall-clock budget;
- stopping criteria;
- randomization policy;
- fault-injection policy.

Record model output separately from orchestration trace so topology effects can be audited.

## Candidate outcomes

Primary candidates:

- task success/quality;
- latency;
- compute/token cost.

Secondary candidates:

- unnecessary activations;
- recovery time;
- disagreement/revision frequency;
- convergence/stability;
- failure propagation;
- hub contention.

## Statistical status

No inferential analysis is frozen yet. The analysis plan must be declared before empirical comparison and must specify the estimand, paired/randomized design, exclusion rules, missing-data handling, confidence intervals, multiplicity handling if needed, and stopping rule.
