# MORSE Reference Model v0.2

## Scope

This document defines the minimum executable model of **MOLI (Multi-Orbital Loop Interchange)** used by MORSE. It intentionally excludes model-provider behavior so topology and scheduling can be tested independently.

## State

At cycle `t`, the system has a set of active loops `A(t)`, hub state `H(t)`, and an event trace `E(t)`.

A loop may activate because of:

- a periodic cadence predicate; or
- an event gate predicate.

The activation decision is deterministic for a fixed configuration.

## Gate model

A gate is a predicate of the form:

`G_i(t, A(t)) -> {true, false}`

When true, the target loop is added to the active set for that cycle.

Gates are therefore **permission mechanisms**, not execution logic.

## Interchange model

The central hub accepts a route request:

`R(t, source, target, payload)`

and returns an explicit acceptance decision and reason. The hub also records a reconciliation boundary after each cycle.

## Topology

The initial topology comparison contains 3-leaf and 4-leaf complete interaction graphs around a conceptual central hub.

For `n` leaves, pairwise relationships are:

`n(n-1)/2`

which yields 3 relationships for 3 leaves and 6 for 4 leaves.

## Temporal regimes

The reference implementation supports:

- **uniform** — all loops period 1;
- **binary** — periods `1, 2, 4, ...`;
- **platinum** — integer periods obtained from a geometric progression using the project-defined Platinum Mean;
- **multi_ratio** — heterogeneous integer-surrogate periods `[1, 2, 3, 5]` corresponding to candidate clocks `1, sqrt(2), Platinum, Silver`; exact irrational-frequency scheduling is reserved for the phase-accumulator layer.

These are experimental conditions, not claims of superiority.

## Evidence boundary

The reference simulator measures scheduling/topology behavior only. It does not establish improved reasoning, task quality, or AI-agent efficacy. Those require a controlled provider/model experiment built on top of this apparatus.
