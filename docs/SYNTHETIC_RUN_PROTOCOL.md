# MORSE Synthetic Run Protocol

## Purpose

This protocol defines the first executable mechanism-level experiment. It does not test or establish LLM efficacy.

## Matrix

- leaf counts: 3, 4
- scheduling regimes: C0, C1, C2, C3
- default tasks per repetition: 100
- default repetitions: 50
- expected observations: 100 × 50 × 2 × 4 = 40,000

## Controls

Task identity is shared across conditions within a repetition. Each observation is uniquely identified by **repetition + task ID + condition**. Condition seeds are derived deterministically from the global seed, repetition seed, task identity, and condition. Mutable scheduler state is reset for every task/condition execution so one task cannot alter the next task's phase state.

## Validation gates

A run is invalid if:

- observation cardinality is incorrect
- any expected condition is absent
- condition cardinalities differ
- task identifiers are malformed
- an observation identity is duplicated
- manifest observation digest cannot be reproduced

## Output

The run produces observations plus a provenance manifest. The manifest binds the source commit, task seed, configuration cardinality, observation count, observation digest, and analysis version.

## Interpretation

Synthetic results may establish properties of the modeled mechanism. They do not establish that MORSE improves actual AI systems, generalizes across models, or provides production-level efficiency gains.
