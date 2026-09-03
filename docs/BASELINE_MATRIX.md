# MORSE Competitive Baseline Matrix

## Objective

Establish the minimum comparison set required before claiming that MORSE improves orchestration.

| Baseline | Communication / scheduling characteristic | Purpose |
|---|---|---|
| Single loop | No multi-agent coordination | Cost/quality floor |
| Sequential pipeline | Fixed ordered handoff | Pipeline comparison |
| Uniform multi-loop | All leaves participate each cycle | Tests value of differentiated cadence |
| Fixed periodic | Communication at fixed intervals | Separates periodicity from multi-ratio structure |
| Asynchronous | Opportunistic independent communication | Tests whether explicit phase adds value beyond asynchrony |
| Sparse/static topology | Limited fixed communication edges | Separates temporal structure from topology sparsity |
| Event-driven | Activation on state conditions | Tests phase scheduling against reactive scheduling |
| MORSE | Central interchange + recurrent phase/cadence regimes | Target architecture |

## Required controls

Comparisons should match, where feasible:

- task set and task ordering;
- model family and model capability;
- inference/token budget;
- tool-call budget;
- maximum latency budget;
- number of agents/leaves when topology is the independent variable;
- randomization and seed handling;
- stopping and failure rules.

## Analysis principle

Report both absolute outcomes and resource-normalized outcomes. A higher success rate obtained by spending substantially more inference is not an unqualified architectural improvement.

## Current status

This is an experimental-design requirement. No baseline comparison has yet established MORSE superiority.
