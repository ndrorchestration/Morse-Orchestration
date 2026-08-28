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

**Phase:** deterministic apparatus + synthetic harness validation

**Empirical N:** 0 for external/AI efficacy claims

**Claim status:** no efficacy claim established

The integer scheduler remains the simple baseline. The phase-accumulator scheduler preserves non-integer/irrational average frequencies without integer-period surrogates. The provider-neutral seeded harness, paired-seed runner, and frozen percentile-bootstrap analysis are available for apparatus validation.

## Controlled pilot configuration

`configs/pilot_matrix.json` defines the initial 3/4-leaf × C0–C3 matrix, 50 paired seeds, 100 tasks per seed, 10,000 bootstrap resamples, and deterministic analysis seed `20260828`.

Synthetic harness results must not be presented as evidence of real-world AI efficacy. External-model experiments require an explicit pre-registration/authorization gate after apparatus validation.

See:

- `docs/MODEL.md` — executable architecture model
- `docs/EXPERIMENT.md` — conceptual experiment specification
- `docs/EXPERIMENT_PLAN.md` — current experimental plan
- `docs/PHASE_SCHEDULING.md` — phase-preserving scheduler
- `docs/ROADMAP.md` — implementation roadmap
- `configs/pilot_matrix.json` — controlled pilot configuration
