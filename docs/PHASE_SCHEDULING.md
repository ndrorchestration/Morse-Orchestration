# Phase-preserving scheduling

For a loop with period ratio `r >= 1`, MORSE defines normalized activation frequency as `f = 1/r` activations per primary cycle.

A deterministic phase accumulator updates:

`phase(t+1) = phase(t) + f`

Every integer boundary crossed emits an activation; the fractional residual is retained. This preserves the requested long-run frequency without replacing an irrational ratio with an integer period.

## Candidate ratios

- sqrt(2)
- Golden Ratio
- Project Platinum Mean: `1/(2 sin(pi/11)) ≈ 1.7747`
- Silver Ratio: `1 + sqrt(2) ≈ 2.4142`
- Binary: `2`

## Scientific boundary

Phase preservation establishes implementation fidelity only. It does not establish resonance, superiority, efficiency, or AI efficacy.

## Reproducibility

Given identical loop specifications, initial phase, and cycle count, activation traces are deterministic. Long-run observed frequency should converge to the configured frequency with bounded finite-horizon error.
