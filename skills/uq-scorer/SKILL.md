---
name: uq-scorer
description: >
  Uncertainty Quantification (UQ) wrapping protocol for LLM classification outputs.
  Use when any agent produces a binary or probabilistic classification verdict and
  a confidence interval or variance estimate is required. Provides Deep Ensemble UQ
  (primary) across 3 distinct providers, MC-Dropout fallback (N=20), and Bayesian
  confidence floor from Fisher's exact test. Integrates with the DISARM statistical
  gate. Do not invoke directly — attach to individual classifier agents via the
  `skills = ["uq-scorer"]` field in their agent.toml.
---

# UQ-Scorer — Uncertainty Quantification Skill

Implements the three UQ methods from Puczyńska & Djenouri (2024) DOI:10.60097/ACIG/200200
adapted for the LibreFang multi-agent disinformation detection pipeline.

**Paper**: "AI in Disinformation Detection", Applied Cybersecurity & Internet Governance 2024.

---

## Why UQ Matters

A wrong high-confidence label is more dangerous than a correct uncertain one.
In adversarial contexts (disinformation, FIMI), over-confident false negatives
propagate uncorrected. UQ enables:
1. **Prioritization**: uncertain classifications flagged for human review
2. **Taint propagation**: `UQ_confidence: low` tag carried through downstream agents
3. **Calibration feedback**: provider variance informs Bayesian weight updates in orchestrator

---

## Method 1: Deep Ensembles (Primary)

Route each classification through **3 distinct LLM providers**. Measure prediction variance
as the uncertainty signal.

```
Input:  claim_text (string)
Providers used: [primary_provider, fallback_1, fallback_2]
  — MUST be 3 genuinely distinct providers (different model families)
  — e.g. nvidia/llama-3.3 + gemini/gemini-2.5-flash + freellmpool/Meta-Llama-3.3

For each provider p_i:
  score_i = classify(claim_text, provider=p_i)   # float 0.0–1.0

ensemble_mean = mean([score_1, score_2, score_3])
uq_variance   = variance([score_1, score_2, score_3])

Output contract:
  {
    "score":                   <float, ensemble_mean>,
    "uq_variance":             <float>,
    "uq_std":                  <float, sqrt(uq_variance)>,
    "uq_method":               "deep_ensemble",
    "providers_used":          [<provider_id_1>, <provider_id_2>, <provider_id_3>],
    "per_provider_scores":     { "<provider_id>": <score>, ... },
    "confidence_band_low":     <ensemble_mean - 1.96*uq_std>,
    "confidence_band_high":    <ensemble_mean + 1.96*uq_std>,
    "confidence_floor_passed": <bool, see Method 3>,
    "uq_flag":                 "HIGH_UNCERTAINTY" | "MODERATE_UNCERTAINTY" | "LOW_UNCERTAINTY"
  }

uq_flag thresholds:
  uq_variance > 0.08   → HIGH_UNCERTAINTY    (flag for human review)
  uq_variance > 0.03   → MODERATE_UNCERTAINTY
  uq_variance <= 0.03  → LOW_UNCERTAINTY
```

---

## Method 2: Monte Carlo Dropout (Fallback)

When only one provider is available or provider ensemble cannot be formed.

```
For each forward pass i in [1..N] (N=20, default):
  score_i = classify(claim_text, dropout_active=true, dropout_rate=0.1)

mc_mean     = mean([score_1 .. score_N])
mc_variance = variance([score_1 .. score_N])

Output: same contract as Deep Ensembles, with:
  "uq_method": "mc_dropout",
  "mc_passes":  20
```

**Note**: MC Dropout requires the underlying model to support stochastic inference.
Not all API-served LLMs support this. When unavailable, fall back to single-provider
score with `uq_method = "single_provider"` and `uq_variance = null` (flag explicitly).

---

## Method 3: Bayesian Confidence Floor (DISARM Integration)

When the DISARM-hunter has run a statistical gate for the same content item:

```
If disarm_hunter.session_results contains an EvidenceAtom for this claim's TTP:
  confidence_floor_passed = (atom.odds_ratio >= 3.0 AND atom.p_value < 0.05)
  If confidence_floor_passed = true:
    score = max(score, atom.odds_ratio / (atom.odds_ratio + 1))  # OR→probability conversion
    uq_flag = "BAYESIAN_FLOOR_APPLIED"
```

This gives every DISARM-verified claim a statistical confidence minimum,
preventing the ensemble from assigning a low-confidence verdict to
statistically-confirmed TTP evidence.

---

## Integration Contract

### Upstream (per-agent UQ output)

Each agent using `uq-scorer` writes to its memory namespace:

```
memory_store("<agent_name>.uq_variance",  <float>)
memory_store("<agent_name>.uq_method",    <string>)
memory_store("<agent_name>.uq_flag",      <string>)
memory_store("<agent_name>.providers_used", <JSON array>)
```

### Downstream (orchestrator consumption)

The disinfo-orchestrator reads per-agent UQ fields and computes:

```
orchestrator.uq_summary = {
  "per_signal_variance": {
    "ml_classifier":        <uq_variance>,
    "coherence_checker":    <uq_variance or null>,
    "wiki_checker":         <uq_variance or null>,
    "triplet_fact_checker": <uq_variance or null>,
    "source_rater":         <uq_variance or null>
  },
  "high_uncertainty_signals": [<agent names where uq_flag = HIGH_UNCERTAINTY>],
  "needs_human_review":       <true if any signal HIGH_UNCERTAINTY>,
  "bayesian_floor_applied":   <true if DISARM confidence floor raised any score>
}
```

### Taint propagation

Any downstream agent action triggered by a `HIGH_UNCERTAINTY` verdict carries the
taint tag `UQ_confidence: low`. This is tracked via LibreFang's 16-layer taint
tracking system. Human review queue receives all tainted verdicts.

---

## Provider Diversity Requirement

Deep Ensemble UQ is ONLY meaningful when providers are genuinely distinct:

| Acceptable trio | Variance measures real disagreement |
|-----------------|-------------------------------------|
| nvidia/llama + gemini/gemini + freellmpool/meta-llama | ✅ Different families |
| freellmpool/meta-llama × 3 | ❌ All same model — variance = 0 |

When configuring `[[fallback_models]]` in an agent, ensure the three entries use
different base model families. See `agents/ml-classifier/agent.toml` for reference.
