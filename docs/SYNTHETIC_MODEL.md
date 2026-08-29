# MORSE Synthetic Mechanism Model

## Purpose

The synthetic harness is a mechanism test, not an AI-performance benchmark. Its purpose is to expose whether scheduler-generated activations and hub coincidences propagate into measurable differences under a fully deterministic workload.

## Causal path

```text
candidate ratio
    -> phase scheduler
    -> leaf activations
    -> same-cycle coincidences
    -> synthetic signal opportunity
    -> task outcome
```

No regime-specific reward, success bonus, or hidden parameter is assigned to Platinum, Silver, binary, or any other named condition.

## Synthetic task

Each task has deterministic difficulty and signal requirements derived from a task seed. A condition receives a deterministic condition-specific seed. The scheduler determines activation count and hub coincidences. Those observables feed the synthetic outcome function.

The model is intentionally simple. It is suitable for testing apparatus coupling, determinism, provenance, and comparative mechanics. It is **not** intended to be a realistic model of an LLM, agent, cognition, or production workload.

## Interpretation boundary

A difference in synthetic success means only that the specified synthetic mechanism responds differently to the tested scheduler/topology conditions. It does not demonstrate that the same effect occurs with language models or useful real-world tasks.

## Required checks before use as evidence

- phase-frequency accuracy
- deterministic replay
- paired task identity
- condition-independent task generation
- no hidden regime-specific parameters
- complete provenance
- fault behavior where applicable
- frozen analysis procedure

Synthetic results should remain labeled exploratory until the experimental protocol is frozen.
