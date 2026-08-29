# MORSE Top-to-Bottom Stack Audit

## Audit scope

The stack is reviewed from dependency/configuration boundaries through domain models, scheduling, topology, simulation, experiment generation, evidence, analysis, tests, and documentation.

## Layers

1. **Packaging/configuration** — Python >=3.11, setuptools build, pytest test path, zero runtime dependencies.
2. **Domain model** — LoopSpec, Gate, Activation, InterchangeEvent, HubState, SimulationTrace.
3. **Integer scheduler** — deterministic legacy/reference cadence and event gates.
4. **Phase scheduler** — normalized frequency accumulator for non-integer and irrational period ratios.
5. **Ratios** — sqrt(2), Golden, Platinum Mean, Silver, binary candidates; no optimality implied.
6. **Topology** — explicit 3- and 4-leaf clover structures.
7. **Simulation/hub** — provider-neutral interchange behavior.
8. **Synthetic experiment** — phase-backed C0-C3 conditions and paired 3/4-leaf matrix.
9. **Evidence** — canonical observation digest and source-commit-bound manifest.
10. **Analysis** — deterministic paired bootstrap with finite-input validation.
11. **Tests/CI** — phase, matrix, evidence, analysis, and cross-layer contracts.
12. **Documentation** — methodology, independence, evidence ladder, synthetic protocol, and internal inspiration separated from scientific rationale.

## Defects corrected during audit

- phase compatibility API missing from the implementation
- incorrect Platinum test indexing
- synthetic harness not actually consuming phase state
- scheduler state leaking between tasks
- malformed condition parsing in matrix validation
- observation identity not including repetition
- analysis accepting non-finite deltas
- metric summaries accepting mismatched cycle counts
- integer surrogate documentation conflicting with phase-backed implementation

## Remaining validation boundary

Repository inspection can establish structural consistency, but it cannot substitute for executing the full synthetic matrix under CI and preserving the resulting artifacts. No AI efficacy claim is implied by this audit.
