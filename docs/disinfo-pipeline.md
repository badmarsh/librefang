# MCP Disinformation Detection Pipeline

> Implementation of arXiv:2508.10143 — "MCP-Orchestrated Multi-Agent System for Automated Disinformation Detection"
> Avram, Groza, Lecu (2025)

## Architecture

```
Input (text/URL)
       |
       v
[claim-extractor]          — NER-based factual claim extraction
       |
       +---> [ml-classifier]        (weight: 0.38) — TF-IDF logistic regression
       +---> [coherence-checker]    (weight: 0.21) — LLM coherence & logic
       +---> [triplet-fact-checker] (weight: 0.41) — S-P-O web verification
       |
       v
[disinfo-orchestrator]     — Weighted ensemble aggregation
       |
       v
[writer]                   — Human-readable briefing
```

All agents share a **live MCP context** (memory_store/memory_recall) so each downstream
agent benefits from prior agents' findings without explicit message passing.

## Weighted Aggregation

Weights derived from per-agent misclassification rates (e_i):

```
w_i = (1 - e_i) / sum_j(1 - e_j)

Default weights:
  ml-classifier:        0.38  (e ≈ 0.18)
  coherence-checker:    0.21  (e ≈ 0.36)
  triplet-fact-checker: 0.41  (e ≈ 0.12)
```

Final fake probability per claim:
```
P_fake = 0.38 * ml_score + 0.21 * (1 - coherence_score) + 0.41 * triplet_score
```

## Verdict Thresholds

| P_fake | Verdict |
|--------|------------------|
| ≥ 0.70 | DISINFORMATION |
| ≥ 0.50 | SUSPICIOUS |
| ≥ 0.35 | UNCERTAIN |
| < 0.35 | CREDIBLE |

## Paper Benchmark

| Metric | Value |
|--------|-------|
| Accuracy | 95.3% |
| F1 Score | 0.964 |
| Coherence agent alone | ~64% |

## API / MCP Context Keys

| Agent | Writes key | Reads keys |
|-------|------------|------------|
| claim-extractor | `claim_extractor.output` | — |
| ml-classifier | `ml_classifier.output` | `claim_extractor.*` |
| coherence-checker | `coherence_checker.output` | `claim_extractor.*` |
| triplet-fact-checker | `triplet_fact_checker.output` | `claim_extractor.*` |
| disinfo-orchestrator | `orchestrator.verdicts` | all of the above |
| writer | `writer.*` | `orchestrator.*` |

## Known Limitations

1. **DuckDuckGo dependency** — triplet-fact-checker is vulnerable to recursive disinformation
   if search results themselves are polluted. Flag `search_quality_flag: true` when detected.
2. **Coherence accuracy ceiling** — coherence-checker is intentionally limited (~64% standalone);
   it contributes ~21% weight to the ensemble.
3. **LLM simulation** — ml-classifier and coherence-checker are LLM simulations of the
   original trained classifiers. For production use, replace with actual trained models
   (scikit-learn LogisticRegression + TfidfVectorizer recommended).

## Running the Pipeline

```bash
# 1. Extract claims
librefang run claim-extractor --input '{"type": "url", "url": "https://example.com/article"}'

# 2. Run scoring agents in parallel
librefang run ml-classifier &
librefang run coherence-checker &
librefang run triplet-fact-checker &
wait

# 3. Aggregate and report
librefang run disinfo-orchestrator
librefang run writer
```

Output files: `claim_extractor_output.json`, `ml_classifier_output.json`,
`coherence_checker_output.json`, `triplet_fact_checker_output.json`,
`disinfo_verdicts.json`
