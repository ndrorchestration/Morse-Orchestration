# MORSE Controlled Pilot Protocol — Draft for Freeze

## Status

**Draft / not authorized for confirmatory execution.** No AI efficacy observations are included in this document.

## Objective

Compare orchestration conditions while holding task identity and computational budget constant, testing whether topology and scheduling regime affect predefined outcomes.

## Factor matrix

Primary topology factor: 3 leaves vs 4 leaves.

Scheduling factor:

- C0 Uniform
- C1 Binary
- C2 Platinum
- C3 Multi-ratio

Recommended initial matrix: 2 × 4 = 8 MORSE conditions, plus separately specified conventional baselines.

## Paired execution

For each task instance, derive a condition-independent task seed. Each condition receives a deterministic condition seed derived from the task identity and global experiment seed. Conditions must not share mutable runtime state.

## Candidate primary endpoint

Task success under a preregistered task-specific correctness criterion.

The final endpoint definition must be frozen before confirmatory execution.

## Secondary endpoints

- quality score
- completion latency
- orchestration events
- loop activations
- gate activations
- recovery success
- error propagation
- token/compute cost
- unnecessary activations

## Analysis

The paired difference is the primary comparison unit. The frozen analysis implementation uses deterministic 10,000-resample paired bootstrap confidence intervals, percentile two-sided 95% intervals, and alpha = 0.05.

Directional support requires a positive point estimate with the confidence interval entirely above zero. This criterion is an analysis rule, not evidence that any condition is universally superior.

Multiplicity policy, primary contrast, and final sample size must be frozen before confirmatory execution.

## Blinding

Where practical, condition identifiers should be blinded during scoring and analysis. Unblinding must occur only after the analysis dataset and primary analysis procedure are frozen.

## Exclusions

No post-hoc exclusion based on outcome value is permitted. Technical failures must be classified using rules frozen before analysis.

## Reproducibility record

Each run must preserve repository SHA, configuration hash, task-set identity, seed derivation, environment fingerprint, raw records, analysis version, and artifact hash.

## Epistemic status

This protocol defines a controlled experiment. It does not assert that any scheduling ratio or leaf count is beneficial.
