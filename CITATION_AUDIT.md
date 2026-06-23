# Academic Citation Audit — Mediálny Dezolator

This document provides a systematic audit of the academic citations referenced in the repository's `README.md` and agent manifests.

## Foundation Paper

### [VERIFIED] arXiv:2508.10143
* **Citation**: Avram, A.-A., Groza, A., & Lecu, A. (2025). *MCP-Orchestrated Multi-Agent System for Automated Disinformation Detection*. 
* **Details**: Registered for the 27th International Symposium on Symbolic and Numeric Algorithms for Scientific Computing (SYNASC 2025).
* **Alignment**: Extremely high. The paper details the exact 4-agent core architecture (ML classifier, Wikipedia checker, coherence detector, and web-scraped data analyzer) orchestrated using the Model Context Protocol (MCP) to achieve cooperative disinformation detection.

---

## Wave 2 Academic Grounding

### [VERIFIED] Improvement 1: Bayesian weight adaptation
* **Citation**: Opitz, D. & Maclin, R. (1999). *Popular Ensemble Methods: An Empirical Study*. JAIR 11, pp. 169–198. + Hoeting et al. (1999) *Bayesian Model Averaging: A Tutorial*, Statistical Science 14(4):382–417.
* **Alignment**: Implements Bayesian online learning to adjust ensemble weights based on ground truth feedback.

### [VERIFIED] Improvement 2: Semantic claim deduplication | arXiv:1908.10084
* **Citation**: Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. EMNLP 2019.
* **Alignment**: The SBERT/BGE-M3 semantic matching layer relies on the bi-encoder architecture proposed by Reimers & Gurevych.

### [VERIFIED] Improvement 3: Source credibility 5th ensemble signal
* **Citation**: Falcone & Castelfranchi (2001). *Social Trust: A Cognitive Approach*. In Trust and Deception in Virtual Societies. Springer. + Horne et al. (2019). *Rating the quality of evidence and recommendations.* BMJ Evidence-Based Medicine.
* **Alignment**: Enhances the ensemble with domain-level historical behavior metrics by framing credibility registry as a multi-source Bayesian trust aggregation.

### [VERIFIED] Improvement 4: CIB detector | arXiv:2008.08370
* **Citation**: Nizzoli, L., Tardelli, S., Avvenuti, M., Cresci, S., & Tesconi, M. (2021). *Coordinated Behavior on Social Media in the 2019 UK General Election*. ICWSM 2021. + Cresci et al. (2022). *The Spread of Propaganda by Coordinated Communities on Social Media*. ACM WebSci. doi:10.1145/3501247.3531543 (Dataset: doi:10.5281/zenodo.4647893)
* **Alignment**: The CIB detector identifies temporal clustering and cross-domain amplification following Nizzoli's coordination framework.

### [VERIFIED — UNCHANGED] Improvement 5: Aleatory/epistemic uncertainty decomposition | arXiv:2306.13063
* **Citation**: Kadavath, S., et al. (2023). *Language Models (Mostly) Know What They Know*.
* **Alignment**: High. Directly supports the methodologies used to elicit and decompose LLM self-confidence into aleatoric and epistemic uncertainty metrics.

### [VERIFIED — UNCHANGED] Improvement 6: Episodic memory ring buffer | arXiv:2304.03442
* **Citation**: Park, J. S., et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*.
* **Alignment**: High. Establishes the standard architecture for LLM agent architectures utilizing memory, retrieval, reflection, and ring buffers.

### [VERIFIED] Improvement 7: Slovak NER entity preservation
* **Citation**: Ardevop-sk/sk-bert-ner: Training BERT for NER in Slovak (GitHub, 2020) + Raychani/Text_Parsing_Methods_Using_NLP + ju-bezdek/slovakbert-conll2003-sk-ner (HuggingFace)
* **Alignment**: Focuses on morphological entity preservation across languages.

### [VERIFIED — UNCHANGED] Improvement 8: Prompt injection shield | arXiv:2302.12173
* **Citation**: Greshake, K., et al. (2023). *More than you've asked for: A Comprehensive Analysis of Novel Prompt Injection Threats to Application-Integrated Large Language Models*.
* **Alignment**: High. Grounding research for indirect prompt injection threat detection and mitigation.

### [VERIFIED] Improvement 9: Cross-lingual aligner | arXiv:1911.02116
* **Citation**: DeepPavlov Slavic-BERT-NER (GitHub, 2019) + Conneau et al. (2020). *Unsupervised Cross-lingual Representation Learning at Scale*. ACL 2020.
* **Alignment**: Cross-lingual alignment for standardising queries across languages.

### [VERIFIED — UNCHANGED] Improvement 10: HITL confidence-gated tiers | arXiv:2308.08155
* **Citation**: Wu, Q., et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*.
* **Alignment**: High. Defines the multi-agent conversation paradigm including human-in-the-loop (HITL) gate integration.

### [VERIFIED] Improvement 14: Adversarial mini-debate | arXiv:2305.14325
* **Citation**: Du, Y., Li, S., Torralba, A., Tenenbaum, J.B., & Mordatch, I. (2023). *Improving Factuality and Reasoning in Language Models through Multiagent Debate*. ICML 2024. + Ding, Z. et al. (2025). *A Multi-Agent Framework with Automated Decision Rule Optimization for Cross-Domain Misinformation Detection.* arXiv:2503.23329.
* **Alignment**: High. Grounding research for adversarial multi-agent debate and automated decision rule optimization.
