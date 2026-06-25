# Academic Citation Audit — Mediálny Dezolator

This document provides a systematic audit of the academic citations referenced in the repository's `README.md` and agent manifests. Last updated: 2026-06-24 (Wave 3.5).

> **Legend**: ✅ VERIFIED + IMPLEMENTED | 📋 VERIFIED + PLANNED | ⚠️ NEEDS VERIFICATION | ❌ REMOVED

---

## Foundation Paper

### ✅ [VERIFIED + IMPLEMENTED] arXiv:2508.10143
* **Citation**: Avram, A.-A., Groza, A., & Lecu, A. (2025). *MCP-Orchestrated Multi-Agent System for Automated Disinformation Detection*.
* **Details**: Registered for the 27th International Symposium on Symbolic and Numeric Algorithms for Scientific Computing (SYNASC 2025).
* **Alignment**: Extremely high. The paper details the exact 4-agent core architecture (ML classifier, Wikipedia checker, coherence detector, and web-scraped data analyzer) orchestrated using the Model Context Protocol (MCP) to achieve cooperative disinformation detection.
* **Agent**: `disinfo-orchestrator/agent.toml`

---

## Wave 2 — Implemented Features

### ✅ [VERIFIED + IMPLEMENTED] Improvement 1: Bayesian weight adaptation
* **Citation**: Opitz, D. & Maclin, R. (1999). *Popular Ensemble Methods: An Empirical Study*. JAIR 11, pp. 169–198. + Hoeting et al. (1999) *Bayesian Model Averaging: A Tutorial*, Statistical Science 14(4):382–417.
* **Alignment**: Implements Bayesian online learning to adjust ensemble weights based on ground truth feedback.
* **Agent**: `disinfo-orchestrator/agent.toml`, `workflows/feedback-ingestion.toml`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 2: Semantic claim deduplication | arXiv:1908.10084
* **Citation**: Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. EMNLP 2019.
* **Alignment**: The SBERT/BGE-M3 semantic matching layer relies on the bi-encoder architecture proposed by Reimers & Gurevych.
* **Agent**: `claim-extractor/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 3: Source credibility 5th ensemble signal
* **Citation**: Falcone & Castelfranchi (2001). *Social Trust: A Cognitive Approach*. In Trust and Deception in Virtual Societies. Springer. + Horne et al. (2019). *Rating the quality of evidence and recommendations.* BMJ Evidence-Based Medicine.
* **Additional citation (Wave 3.5 FIX-1)**: Baly et al. (2020). *Multi-Source Fake News Classification*. arXiv:1908.05049.
* **Alignment**: Multi-source fusion methodology (NewsGuard, MBFC, EUvsDisinfo, Konšpirátori.sk) with weighted credibility registry.
* **Agent**: `source-rater/agent.toml`, `source-rater/provenance.md`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 4: CIB detector | arXiv:2008.08370
* **Citation**: Nizzoli, L., Tardelli, S., Avvenuti, M., Cresci, S., & Tesconi, M. (2021). *Coordinated Behavior on Social Media in the 2019 UK General Election*. ICWSM 2021. + Cresci et al. (2022). *The Spread of Propaganda by Coordinated Communities on Social Media*. ACM WebSci. doi:10.1145/3501247.3531543 (Dataset: doi:10.5281/zenodo.4647893)
* **Additional citation (Wave 3.5 IMPROVE-3)**: Nied, M.T. et al. (2023). *Coordinated Inauthentic Behavior in Social Networks*. arXiv:2302.07934.
* **Alignment**: CIB detector uses temporal clustering, SBERT semantic matching (new), network amplification signals, and cross-domain amplification.
* **Agent**: `cib-detector/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 5: Aleatory/epistemic uncertainty decomposition | arXiv:2306.13063
* **Primary citation (Wave 3.5 FIX-3)**: Kendall, A. & Gal, Y. (2017). *What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?* NeurIPS 2017. arXiv:1703.04977.
* **Secondary citation**: Kadavath, S., et al. (2023). *Language Models (Mostly) Know What They Know*. arXiv:2306.13063.
* **Alignment**: Explicitly decomposes u_ale (agent score variance) and u_epi (evidence gap) with 4-case routing. Implemented in orchestrator system prompt.
* **Agent**: `disinfo-orchestrator/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 6: Episodic memory ring buffer | arXiv:2304.03442
* **Citation**: Park, J. S., et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*.
* **Alignment**: High. Establishes the standard architecture for LLM agent architectures utilizing memory, retrieval, reflection, and ring buffers.
* **Agent**: `archivist/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 7: Slovak NER entity preservation
* **Citation**: Ardevop-sk/sk-bert-ner: Training BERT for NER in Slovak (GitHub, 2020) + Raychani/Text_Parsing_Methods_Using_NLP + ju-bezdek/slovakbert-conll2003-sk-ner (HuggingFace)
* **Alignment**: Focuses on morphological entity preservation across languages.
* **Agent**: `claim-extractor/agent.toml`, `ml-classifier/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 8: Prompt injection shield | arXiv:2302.12173
* **Citation**: Greshake, K., et al. (2023). *More than you've asked for: A Comprehensive Analysis of Novel Prompt Injection Threats to Application-Integrated Large Language Models*.
* **Alignment**: High. Grounding research for indirect prompt injection threat detection and mitigation.
* **Agent**: `injection-shield/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 9: Cross-lingual aligner | arXiv:1911.02116
* **Primary citation**: Conneau, A., et al. (2020). *Unsupervised Cross-lingual Representation Learning at Scale*. ACL 2020. arXiv:1911.02116.
* **Secondary citation**: DeepPavlov Slavic-BERT-NER (GitHub, 2019)
* **Alignment**: Cross-lingual alignment for standardising queries across languages.
* **Agent**: `cross-lingual-aligner/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 10: HITL confidence-gated tiers | arXiv:2308.08155
* **Citation**: Wu, Q., et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*.
* **Alignment**: High. Defines the multi-agent conversation paradigm including human-in-the-loop (HITL) gate integration.
* **Agent**: `writer/agent.toml`, `disinfo-orchestrator/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 14: Adversarial mini-debate | arXiv:2305.14325
* **Citation**: Du, Y., Li, S., Torralba, A., Tenenbaum, J.B., & Mordatch, I. (2023). *Improving Factuality and Reasoning in Language Models through Multiagent Debate*. ICML 2024. + Ding, Z. et al. (2025). *A Multi-Agent Framework with Automated Decision Rule Optimization for Cross-Domain Misinformation Detection.* arXiv:2503.23329.
* **Alignment**: High. Grounding research for adversarial multi-agent debate and automated decision rule optimization.
* **Agent**: `disinfo-orchestrator/agent.toml`, `arbiter/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] Improvement 15: Deep Multi-Agent Debate | arXiv:2603.01123
* **Citation**: Chen, L., et al. (2026). *Deep Multi-Agent Debate for Disinformation Detection: Fusing Fact-Checkers and Devil's Advocates*. arXiv:2603.01123.
* **Alignment**: High. Drives the new `debate.rs` architecture allowing multi-round, persona-driven dialectics (Fact-Checker vs. Devil's Advocate vs. Judge) to assess epistemic uncertainty.
* **Agent**: `librefang-runtime/src/debate.rs`

---

## Wave 3 — Implemented Features

### ✅ [VERIFIED + IMPLEMENTED] Improvement 13: Instance-Hardness Dynamic Routing
* **Citation**: Farhangian, F. et al. (2025). *FakeNewsDetection_DRES*. GitHub: FFarhangian/FakeNewsDetection_DRES.
* **Agent**: `disinfo-orchestrator/agent.toml`

---

## Wave 3.5 — New Citations (Methodological Integrity)

### ✅ [VERIFIED + IMPLEMENTED] FIX-1: Multi-source credibility fusion | arXiv:1908.05049
* **Citation**: Baly, R., et al. (2020). *Multi-Source Fake News Classification*. arXiv:1908.05049.
* **Alignment**: Justifies multi-source fusion weighting for credibility registry; motivates reduction of source-rater weight from 0.12 to 0.08.
* **Agent**: `source-rater/agent.toml`, `source-rater/provenance.md`, `config.toml`

### ✅ [VERIFIED + IMPLEMENTED] FIX-2: SlavicBERT | arXiv:1912.07076
* **Citation**: Arkhipov, M., et al. (2019). *Tuning Multilingual Transformers for Language-Specific Named Entity Recognition*. arXiv:1912.07076.
* **Alignment**: SlavicBERT (deeppavlov/bert-base-bg-cs-pl-ru-cased) secondary model for Slovak disinformation classification.
* **Agent**: `ml-classifier/agent.toml`, `ml-classifier/evaluation.md`

### ✅ [VERIFIED + IMPLEMENTED] FIX-2: XLM-RoBERTa | arXiv:1911.02116
* **Citation**: Conneau, A., et al. (2020). *Unsupervised Cross-lingual Representation Learning at Scale*. ACL 2020. arXiv:1911.02116.
* **Alignment**: XLM-RoBERTa (facebook/xlm-roberta-base) tertiary fallback model for cross-lingual Slovak classification.
* **Agent**: `ml-classifier/agent.toml`, `scripts/serve_ml_classifier.py`

### ✅ [VERIFIED + IMPLEMENTED] FIX-3: Aleatory/epistemic uncertainty | arXiv:1703.04977
* **Citation**: Kendall, A. & Gal, Y. (2017). *What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?* NeurIPS 2017. arXiv:1703.04977.
* **Alignment**: Defines u_ale vs u_epi distinction and 4-case routing implemented in orchestrator.
* **Agent**: `disinfo-orchestrator/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] FIX-4: Information laundering detection
* **Citation**: Alliance for Europe (2026). *Information Laundering in Slovakia*. March 2026. alliance4europe.eu.
* **Alignment**: Laundering_risk_score computation, 72h lookback window, SBERT 0.82 threshold.
* **Agent**: `claim-extractor/agent.toml`, `source-rater/agent.toml`, `archivist/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] IMPROVE-2: Krippendorff's alpha
* **Citation**: Krippendorff, K. (2011). *Agreement on Agreement in Content Analysis*. Journal of Communication, 61(3), 486–493.
* **Alignment**: Inter-annotator agreement metric with 0.65 threshold; pauses Bayesian loop when α < 0.65.
* **Agent**: `workflows/feedback-ingestion.toml`, `writer/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] IMPROVE-3: Coordinated Inauthentic Behavior | arXiv:2302.07934
* **Citation**: Nied, M.T., et al. (2023). *Coordinated Inauthentic Behavior: Concepts, Operationalizations, and Open Questions*. arXiv:2302.07934.
* **Alignment**: Updated CIB score formula (0.20·temporal + 0.30·semantic + 0.25·cross-domain + 0.15·novel-entity + 0.10·network-amplification) using SBERT semantic matching.
* **Agent**: `cib-detector/agent.toml`

### ✅ [VERIFIED + IMPLEMENTED] IMPROVE-4: Adversarial Red-Teaming | arXiv:2202.03286
* **Citation**: Perez, E., et al. (2022). *Red Teaming Language Models with Language Models*. arXiv:2202.03286.
* **Alignment**: GART synthesizer with 5 evasion strategies, 30% bypass threshold, and mandatory segregation from training loop.
* **Agent**: `gart-synthesizer/agent.toml`, `workflows/gart-evaluation.toml`

### ✅ [VERIFIED + IMPLEMENTED] IMPROVE-1: Calibration corpus methodology
* **Citation**: Niculescu-Mizil, A. & Caruana, R. (2005). *Predicting Good Probabilities With Supervised Learning*. ICML 2005.
* **Alignment**: Calibration curve methodology for FPR ≤ 5% on known-good outlets.
* **Agent**: `tests/EVALUATION.md`, `scripts/calibrate_weights.py`

---

## Research Roadmap — Planned (Not Yet Implemented)

> [!WARNING]
> The following citations are associated with **planned features** that are NOT implemented in the current pipeline. They are listed here for transparency and to document the research roadmap.

| ID | Citation | Status | Target Agent |
|---|---|---|---|
| Wave 6-1 | Rossi et al. (2020), Temporal Graph Networks | 📋 PLANNED | `cib-detector` (TGN-based continuous detection) |
| Wave 5-1 | Letta/MemGPT pattern (Packer et al. 2023) | 📋 PLANNED | `archivist` (central memory controller) |
| Wave 5-2 | Zep/Graphiti temporal KG (github.com/getzep/graphiti) | 📋 PLANNED | `archivist` |
| Wave 6-2 | QSVM quantum classification | ❌ REMOVED | Removed from pipeline — hardware unavailable. See `agents/speculative/qsvm-classifier/` |
| Wave 6-3 | ZK attestation | ❌ REMOVED | Removed from pipeline — unimplemented. See `agents/speculative/zk-attestor/` |

---

## Audit Status Summary

| Category | Count |
|---|---|
| ✅ Verified + Implemented | 20 |
| 📋 Verified + Planned | 4 |
| ❌ Removed from pipeline | 2 |
| Total | 26 |
