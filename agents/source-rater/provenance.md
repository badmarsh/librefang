# Source Credibility Registry Provenance Chain

This document outlines the design, provenance sources, and fusion logic for the `source-rater` agent. By integrating multiple independent credibility scoring databases, the agent avoids internal bias and circular priors.

> **Wave 3.5 — FIX-1**: The source-rater weight was reduced from 0.12 → 0.08 in the ensemble, and the known-bad/known-good lists were replaced with dynamic external lookups from at least 3 independent sources. This eliminates the circular prior problem where credibility judgments derived from the same contested attributions being evaluated.
>
> Reference: Baly et al., "Multi-Source Fake News Classification" (arXiv:1908.05049)

---

## 1. External Data Sources

We synthesize domain credibility evaluations from four independent registries. All sources are external and independently maintained — none derive from internal LibreFang or partner datasets.

### A. NewsGuard API
* **Provider**: NewsGuard Technologies (newsguardtech.com)
* **Type**: Professional journalistic evaluations based on 9 credibility and transparency criteria (process transparency, accuracy of headlines, gathering/presenting information, etc.).
* **Metric**: Trust score from 0 to 100.
* **Mapping**: `newsguard_score = trust_score / 100.0`.
* **Weight**: 0.35 (reflecting high standardized auditing standards and transparent methodology).
* **Access**: API key required (configured via `NEWSGUARD_API_KEY`).

### B. Media Bias/Fact Check (MBFC)
* **Provider**: Media Bias/Fact Check (mediabiasfactcheck.com)
* **Type**: Independent factual reporting and bias categorization, maintained since 2015.
* **Metric**: Qualitative classifications (Very High, High, Mostly Factual, Mixed, Low, Very Low, Conspiracy/Pseudoscience).
* **Mapping**:
  * `HIGH` or `VERY HIGH` → 0.85
  * `MOSTLY FACTUAL` → 0.70
  * `MIXED` → 0.50
  * `LOW` → 0.25
  * `VERY LOW` → 0.10
  * `CONSPIRACY` / `PSEUDOSCIENCE` → 0.05
* **Weight**: 0.20.
* **Access**: Web scraping via Firecrawl (self-hosted instance). MBFC does not provide an official API.

### C. EUvsDisinfo Database
* **Provider**: European External Action Service (EEAS) East StratCom Task Force (euvsdisinfo.eu)
* **Type**: Repository of pro-Kremlin disinformation cases and outlets documented since 2015.
* **Metric**: Listed / Not listed as a disinformation outlet in verified disinformation cases.
* **Mapping**:
  * Specifically listed as disinformation source → 0.10.
  * Not listed → 1.00 (note: absence of listing is NOT a positive endorsement — treated as neutral if no other data).
* **Weight**: 0.10.
* **Access**: Public dataset via euvsdisinfo.eu/disinformation-cases API.

### D. Konšpirátori.sk Slovak-Specific Database
* **Provider**: Konšpirátori.sk association (konspiratori.sk) — an independent commission of Slovak journalists, academics, and experts.
* **Type**: Slovak-specific credibility ratings for Central European disinformation/unreliable domains.
* **Metric**: Rating from 1.0 to 10.0 (higher = riskier/less credible).
* **Mapping**: `konspiratori_score = 1.0 - (score / 10.0)`.
* **Weight**: 0.35 (reflecting localized, region-specific expertise directly relevant to Slovak media ecosystem).
* **Access**: Web scraping or partner data agreement.

---

## 2. Source Independence Verification

These four sources are **independently maintained** with distinct methodologies, funding, and editorial processes:

| Source | Operator | Funding | Methodology |
|---|---|---|---|
| NewsGuard | NewsGuard Technologies (private) | Subscription + advertising industry | 9-criteria journalistic audit |
| MBFC | Dave Van Zandt (independent) | Donations | Volunteer reviewer panels |
| EUvsDisinfo | European External Action Service (EU institution) | EU budget | Case-by-case verification by EEAS analysts |
| Konšpirátori.sk | Slovak civil society association | Grants (IJF, OSF) | Panel of Slovak experts |

No circular dependency exists between these sources. None derive from LibreFang's own historical verdicts.

---

## 3. Fusion Function

The final credibility score is a weighted average of all available ratings, preventing any single missing or biased database from dominating the evaluation.

$$credibility\_score = \frac{\sum (score_i \times weight_i)}{\sum weight_i}$$

where the sum is taken only over sources for which a rating is available.

### Insufficient Information Handling
We compute `credibility_confidence` as the number of available source registries that returned a rating.
* If `credibility_confidence < 2`, the domain lacks sufficient external consensus.
* In this case, we flag the claim for human review (`needs_human_review = true`) and default the credibility score to neutral (`0.50`).
* Rationale: a single-source judgment is insufficient to establish credibility or non-credibility, especially for lesser-known Slovak portals not yet covered by international registries.

---

## 4. Credibility Confidence Field

Each verdict output includes a `credibility_confidence` integer (1–4) representing the number of independent sources that returned a score:
* `credibility_confidence = 1` → flag for human review, score = 0.50
* `credibility_confidence = 2` → low confidence, score reported with warning
* `credibility_confidence = 3` → moderate confidence, score reported as-is
* `credibility_confidence = 4` → high confidence (all sources agree)

This field is propagated into the orchestrator's ensemble uncertainty decomposition (u_epi signal). A low `credibility_confidence` increases epistemic uncertainty.

---

## 5. Information Laundering Override

To combat the tactic of publishing narratives on low-credibility outlets before republishing them on high-credibility ones (information laundering):
* If the `laundering_risk_score > 0.60` (indicating the claim appeared on a known-bad source within ≤ 72 hours prior, with SBERT cosine similarity ≥ 0.82), the domain's credibility score is overridden to neutral (`0.50`) regardless of the immediate source's registry ratings.
* The verdict is annotated with `information_laundering_risk_override` and flagged in the review queue with "LAUNDERING RISK".

---

## 6. PageRank-based Credibility Propagation (Conceptual)

Conceptually, a PageRank-style propagation over the domain co-citation graph can propagate credibility scores from trusted seed domains to unknown domains. This is listed as a conceptual enhancement (Weight: 0.15 if implemented). Current implementation uses only the four external sources above.

---

## References
* Baly et al., "Multi-Source Fake News Classification" (arXiv:1908.05049) — foundational multi-source fusion methodology.
* Falcone & Castelfranchi (2001), "Social Trust: A Cognitive Approach." Springer.
* Alliance for Europe, "Information Laundering in Slovakia", March 2026.
* NewsGuard rating methodology: newsguardtech.com/ratings/rating-process-criteria/
* MBFC methodology: mediabiasfactcheck.com/methodology/
* EUvsDisinfo database: euvsdisinfo.eu/disinformation-cases
* Konšpirátori.sk: konspiratori.sk
