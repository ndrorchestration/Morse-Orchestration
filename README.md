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

**Phase:** apparatus validation / synthetic harness preparation

**Empirical N:** 0 for AI efficacy claims

**Claim status:** no efficacy claim established

The integer scheduler remains a simple reproducible baseline. The phase-accumulator scheduler preserves non-integer/irrational average frequencies without integer-period surrogates. A provider-neutral seeded harness and paired-condition analysis layer support controlled synthetic apparatus experiments.

Synthetic results must not be presented as real-world AI efficacy. External-model experiments require a frozen protocol and explicit authorization gate.

## Evidence model

MORSE separates conceptual design, formal specification, implementation, deterministic verification, fault testing, synthetic comparative evidence, controlled AI evidence, and independent replication. See `docs/EVIDENCE_MODEL.md`.

Prior orchestration research may inform MORSE's methods and hypotheses but does not constitute MORSE evidence. See `docs/ARCHITECTURE_TRANSFER.md`.

## References

- `docs/MODEL.md` — executable architecture model
- `docs/EXPERIMENT.md` — conceptual experiment specification
- `docs/EXPERIMENT_PLAN.md` — current experimental plan
- `docs/PHASE_SCHEDULING.md` — phase-preserving scheduler
- `docs/EVIDENCE_MODEL.md` — evidence ladder and provenance requirements
- `docs/ARCHITECTURE_TRANSFER.md` — research transfer boundary
- `docs/ROADMAP.md` — implementation roadmap
- `configs/pilot_matrix.json` — controlled pilot configuration
- `examples/run_reference.py` — deterministic matrix example
