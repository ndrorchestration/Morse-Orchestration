# MORSE

**Multi-Orbital Resonance Scheduling Experiment**

MORSE is an independent research project for testing multi-timescale, conditionally coupled orchestration loops.

## Architecture under study

**MOLI — Multi-Orbital Loop Interchange**

MOLI models a cloverleaf-like topology around a central interchange hub:

- multiple independent orchestration loops;
- explicit temporal cadence/phase;
- periodic and event-driven gates;
- central routing/arbitration/reconciliation;
- explicit return semantics;
- interchangeable scheduling regimes.

The project treats mathematical ratios as experimental scheduling parameters, not as presumed sources of benefit.

## Initial experimental matrix

The first topology/scheduling comparison is `2 × 4`:

| Leaf count | C0 | C1 | C2 | C3 |
|---:|---|---|---|---|
| 3 | Uniform | Binary | Platinum | Multi-ratio |
| 4 | Uniform | Binary | Platinum | Multi-ratio |

### Candidate ratios

- `sqrt(2)`
- Golden Ratio
- **Project Platinum Mean:** `1/(2 sin(pi/11)) ≈ 1.7747`
- Silver Ratio: `1 + sqrt(2) ≈ 2.4142`
- Binary ratio: `2`

The project-defined Platinum Mean must not be conflated with the unrelated plastic constant.

## Scientific status

**Phase:** deterministic apparatus validation

**Empirical N:** 0

**Claim status:** no efficacy claim established

The current C3 condition uses an explicit integer surrogate ladder `[1, 2, 3, 5]` rather than claiming that irrational ratios can be represented exactly by integer periods. A phase-accumulator scheduler is the next layer for preserving average irrational frequencies without discretization aliasing.

See:

- `docs/MODEL.md` — executable architecture model
- `docs/EXPERIMENT.md` — conceptual experiment specification
- `docs/EXPERIMENT_PLAN.md` — current experimental plan
- `docs/ROADMAP.md` — implementation roadmap
- `examples/run_reference.py` — deterministic matrix example
