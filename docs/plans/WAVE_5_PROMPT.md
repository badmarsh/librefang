# WAVE 5: Trustless Verification & Adversarial Self-Evolution

**Target Version:** 5.0.0
**Focus:** Cryptographic Attestations (ZK), Multi-Agent Red Teaming (GART), and AiTM Defenses
**State:** Executing

## Motivation
As the autonomous LibreFang pipeline evolves, we must guarantee that:
1. Fact-checking operations can mathematically prove their integrity without leaking confidential contexts.
2. The agent ecosystem is resilient to Agent-in-the-Middle (AiTM) manipulation.
3. The self-improvement cycle is rigorously tested via Generative Adversarial Red-Teaming (GART).

## Academic Grounding (The Research)

The implementation of Wave 5 is strictly governed by the following 2025/2026 academic research:

1. **Verifiable Model Inference & zk-img:** Establishing Zero-Knowledge SNARKs to prove a specific fact-check was executed on an unmodified model state.
   - Reference: *Verifiable Model Inference (2025)* and *zk-img (arXiv:2211.04775)*
2. **RedDebate (2025):** A multi-agent framework employing collaborative argumentation to autonomously discover failure modes and mitigate unsafe behaviors.
   - Reference: *RedDebate: Multi-Agent Collaborative Argumentation for LLM Safety (2025)*
3. **Agent-in-the-Middle (AiTM):** An attack framework targeting LLM-MAS (Multi-Agent Systems) communications. We implement active defenses against these vectors.
   - Reference: *Agent-in-the-Middle: Intercepting and Manipulating Multi-Agent Systems (2025)*

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## WORK-STREAM A — CORE CRYPTOGRAPHY (librefang-wire)
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### A1. Zero-Knowledge Attestations (`zk_attest.rs`)
Implement Halo2/Bellman-based Zero-Knowledge wrappers.
- Generate SNARK proofs that encapsulate a fact-check verdict.
- Prove that specific LLM weights were used without exposing the raw user input prompt.

### A2. Temporal Topology (`topology.rs`)
Implement decentralized Temporal Knowledge Graph topology propagation.
- Enable agents to share cryptographic attestations across nodes peer-to-peer.

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## WORK-STREAM B — ADVERSARIAL RED-TEAMING (Agents)
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### B1. agents/red-debater/
**Goal:** Continuous adversarial stress-testing.
- Implement the `RedDebate` architecture.
- This agent generates adversarial disinformation and actively debates the `inquisitor` to map logic gaps.

### B2. agents/aitm-defender/
**Goal:** Protect inter-agent message buses.
- Implements the defense protocols for the `AiTM` vulnerability model.
- Analyzes message flow anomalies to detect injected commands traversing between nodes.

---

## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## WORK-STREAM C — CONFIGURATION & RELEASE
## ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### C1. config.toml
Add new blocks:
- `[cryptography.zk]` for Zero-Knowledge configuration (e.g., proving backend).
- `[red_teaming]` for configuring the rate and aggressiveness of the GART synthesized attacks.

### C2. README.md & CHANGELOG.md
- Bump version to `v5.0.0`.
- Record Wave 5 enhancements and cite the academic grounding explicitly in the `Academic Grounding` table.
