# MORSE Research Methodology

## Purpose

MORSE is an independent research line. It may reuse engineering and experimental discipline developed elsewhere in the user's broader architecture research, but MORSE results remain independently generated and independently attributable.

## Evidence boundary

MORSE distinguishes:

1. **Conceptual** — proposed mechanism or topology.
2. **Specified** — definitions, hypotheses, and protocol are explicit.
3. **Implemented** — apparatus exists in executable form.
4. **Deterministically verified** — implementation satisfies automated invariants and reproducibility checks.
5. **Fault-tested** — controlled failures have been introduced and observed.
6. **Synthetic comparative evidence** — controlled non-LLM experiments compare conditions.
7. **AI empirical evidence** — actual model/provider experiments under a frozen protocol.
8. **Independent replication** — an independent execution reproduces the result.

A higher level must not be claimed solely from evidence at a lower level.

## Transfer boundary

Prior architecture research may inform:

- experiment governance
- deterministic seed handling
- provenance and hashing
- schema validation
- CI gating
- blinding and paired comparisons
- fault-injection design
- evidence separation
- reproducibility requirements

It does **not** provide empirical evidence for MORSE efficacy. Any claim about MOLI, temporal ratios, leaf count, or AI performance must be supported by MORSE-specific observations.

## Provenance requirements

Every comparative run should preserve, at minimum:

- repository commit SHA
- experiment configuration
- topology identifier
- scheduling regime and exact parameters
- task-set identifier
- seed derivation rule
- runtime/environment fingerprint
- raw observations
- derived metrics
- analysis version
- artifact hashes

## Pre-registration requirement

Before confirmatory comparison, freeze:

- primary endpoint
- secondary endpoints
- task-generation method
- sample size
- paired-seed/randomization procedure
- compute/token budget
- exclusion rules
- missing/failure handling
- statistical procedure
- confidence level
- alpha
- multiple-comparison policy
- stopping rule
- unblinding procedure

## Epistemic constraints

- Ratios are candidate scheduling parameters, not privileged constants.
- "Resonance" is a working architectural term until operationally defined and measured.
- The 3-leaf versus 4-leaf question is an empirical factor.
- Synthetic-agent results do not establish LLM efficacy.
- Positive results must include effect size and uncertainty, not only significance.
- Negative and null results are retained as valid outcomes.
- Exploratory observations must not silently become confirmatory hypotheses after results are inspected.

## Current status

MORSE has an implemented deterministic apparatus and experimental scaffolding. AI efficacy has not been established; empirical N for AI efficacy remains 0.
