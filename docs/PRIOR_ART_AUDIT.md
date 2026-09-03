# MORSE Prior-Art Audit

## Scope

This document records the current literature-level comparison for MORSE/MOLI. It is a prior-art map, not a novelty opinion or patentability determination.

## Closest families

### Blackboard architectures

Classical blackboard systems coordinate specialized knowledge sources through a shared information space. Temporal blackboard work explicitly treats time and temporal knowledge as part of the communication framework. Modern LLM blackboard systems likewise use shared state and controller-driven activation.

**Overlap with MORSE:** central shared interchange state, specialized processes, opportunistic or controlled activation.

**Difference:** MORSE makes multi-loop cadence/phase relationships an explicit experimental variable.

### Asynchronous and periodic multi-agent communication

Multi-agent research includes asynchronous communication and periodic message exchange to reduce communication overhead while retaining coordination.

**Overlap with MORSE:** not every process communicates or activates every cycle.

**Difference:** MORSE studies relationships among multiple recurring frequencies, including phase-preserving non-integer ratios.

### Sparse communication topology

LLM multi-agent debate research has shown that sparse communication graphs can preserve or improve performance while reducing computational cost. Newer work also explores dynamic topology selection based on trust, divergence, and task relevance.

**Overlap with MORSE:** communication should not necessarily be all-to-all or continuous.

**Difference:** MORSE's central independent variable is temporal scheduling coupled to topology rather than only edge selection.

### Learned/dynamic communication scheduling

Research systems learn when or where agents should communicate, often under bandwidth, cost, or consensus constraints.

**Overlap with MORSE:** communication opportunity itself is an orchestration decision.

**Difference:** MORSE initially treats scheduling rules as controlled experimental conditions rather than learning the schedule from outcomes.

## Research position

The audit does **not** support the claim that MORSE is an entirely unprecedented multi-agent architecture. Its components have substantial precedent.

The potentially distinctive research contribution is the explicit treatment of **phase relationships among recurrent orchestration loops** as a first-class experimental variable, combined with a central interchange mechanism and direct comparison of 3-leaf versus 4-leaf topologies.

This remains a hypothesis about research novelty, not an established novelty claim.

## Consequence for experimental design

Prior art changes the hypothesis framing from:

> "No one has done this."

to:

> "Existing work establishes that communication topology, communication frequency, timing, and central/shared-state coordination matter. MORSE tests whether structured relationships among multiple recurring loop frequencies add measurable value beyond those known mechanisms."

That framing is the appropriate basis for literature review, experimental design, and any future publication claim.

## Sources reviewed

- Jiang, Yi, Zhang & Zhong (2005), *Constructing agents blackboard communication architecture based on graph theory*, Computer Standards & Interfaces, DOI 10.1016/j.csi.2004.09.003.
- *A temporal blackboard for a multi-agent environment* (1995), Data & Knowledge Engineering.
- Li et al. (2024), *Improving Multi-Agent Debate with Sparse Communication Topology*, arXiv:2406.11776.
- Sun et al. (2025), *CortexDebate: Debating Sparsely and Equally for Multi-Agent Debate*, arXiv:2507.03928.
- Gou & Liu (2026), *Dynamic Trust-Aware Sparse Communication Topology for LLM-Based Multi-Agent Consensus*, arXiv:2606.01828.
- Jiang et al. (2025), *Dynamic Generation of Multi-LLM Agents Communication Topologies with Graph Diffusion Models*, arXiv:2510.07799.

## Status

This audit should be revisited before any publication or explicit novelty claim, because the literature continues to change and because architectural similarity does not by itself establish anticipation, equivalence, or patentability.
