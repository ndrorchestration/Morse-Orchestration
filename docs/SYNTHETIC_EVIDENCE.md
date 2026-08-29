# Synthetic Evidence Artifact Contract

MORSE synthetic runs must produce machine-verifiable provenance before their observations are interpreted.

## Required manifest fields

- schema version
- source commit SHA
- task seed
- task count
- repetition count
- observation count
- canonical SHA-256 digest of observations
- analysis version

## Interpretation boundary

A valid manifest establishes artifact identity and provenance. It does not establish that a scheduling regime is beneficial.

Synthetic results are mechanism-level evidence only and remain separate from AI efficacy evidence.

## Integrity rule

The observation digest is computed from canonical JSON with sorted keys and deterministic separators. Reordering JSON object keys does not change the digest; changing an observation does.
