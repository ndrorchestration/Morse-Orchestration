# Phase-preserving scheduling

MORSE uses a phase accumulator when a condition requires a non-integer cadence. For loop `i` with frequency `f_i` activations per primary cycle:

`phase_i(t+1) = phase_i(t) + f_i`

An activation occurs whenever the accumulated phase crosses an integer boundary; the integer number of crossed boundaries is emitted and retained as residual phase. This avoids replacing irrational ratios with an integer period and therefore preserves the requested long-run activation frequency.

For a period ratio `r`, use:

`f = 1 / r`

Examples include `sqrt(2)`, the project Platinum Mean `1/(2 sin(pi/11))`, and the Silver Ratio `1 + sqrt(2)`.

## Why this matters

The earlier deterministic scheduler uses integer periods and remains useful as a simple baseline. It cannot faithfully encode an arbitrary irrational period. The phase scheduler is the apparatus for testing whether preserving the intended temporal relationship changes system behavior.

## Scientific boundary

Phase preservation establishes a more faithful implementation of the proposed scheduling conditions. It does **not** establish resonance, superiority, or efficacy. Those are empirical questions.

## Reproducibility

The scheduler is deterministic. Given identical loop specifications, initial phase, and cycle count, it must produce an identical activation trace.
