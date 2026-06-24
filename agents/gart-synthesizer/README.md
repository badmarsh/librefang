# GART Synthesizer — Implemented

The GART (Generative Adversarial Red-Teaming) Synthesizer generates adversarial disinformation articles for weekly pipeline stress-testing.

**Wave 3.5 — IMPROVE-4**: Promoted from `agents/speculative/` to `agents/` as a fully implemented evaluation tool.

> [!WARNING]
> **ABSOLUTE SEGREGATION RULE**: GART-generated articles are **NEVER** used for Bayesian weight training, ensemble calibration, or any feedback loop. All outputs are stored in `output/gart_adversarial/` (separate namespace from real verdicts) and tagged with `gart_generated: true`. This prevents the adversarial synthesis loop from poisoning the credibility model.

## Purpose

Implements the adversarial red-teaming loop from Perez et al. (2022) "Red Teaming Language Models with Language Models" (arXiv:2202.03286):

1. Generates 20 adversarial articles per week designed to bypass current detection signals
2. Runs them through the full pipeline  
3. Measures bypass rate (% receiving P_fake < 0.50)
4. If bypass rate > **30%**, triggers human audit alert via Telegram

## Evasion Strategies

| Strategy | Target Signal | Description |
|---|---|---|
| A — Morphological Variation | ML Classifier | Morphologically diverse Slovak vocabulary |
| B — Negation Framing | Coherence Checker | Conditional/negated disinformation framing |
| C — Laundering Simulation | Source Rater | Cite high-credibility outlet for known-bad narrative |
| D — Slow-Burn Temporal | CIB Detector | Spread articles over 72h+ to evade 2h window |
| E — Semantic Paraphrasing | Network Amplification | SBERT cosine ~0.74 (just below 0.75 threshold) |

## Schedule

Runs weekly: **Sunday 03:00 UTC** via `workflows/gart-evaluation.toml`.

## Reference

Perez et al. (2022), "Red Teaming Language Models with Language Models", arXiv:2202.03286
