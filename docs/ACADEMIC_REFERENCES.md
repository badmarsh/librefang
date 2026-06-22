# Academic References — Mediálny Dezolator

Complete bibliography for the Mediálny Dezolator disinformation detection pipeline (v3.1.x).
Citations are grouped by domain. See `CITATION_AUDIT.md` for verification status of each entry.

---

## Foundation

[1] Avram, A.-A., Groza, A., & Lecu, A. (2025). *MCP-Orchestrated Multi-Agent System
    for Automated Disinformation Detection*. SYNASC 2025.
    arXiv:2508.10143

---

## Multi-Agent Orchestration & MCP

[2] Wu, Q., et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via
    Multi-Agent Conversation*. arXiv:2308.08155

[3] Du, Y., et al. (2023). *Improving Factuality and Reasoning in Language Models
    through Multiagent Debate*. arXiv:2305.14325

[4] Park, J.S., et al. (2023). *Generative Agents: Interactive Simulacra of Human
    Behavior*. arXiv:2304.03442

[5] *Operationalizing Multi-Agent Interoperability via Contract-Driven Model Context
    Protocols*. IEEE 2026. (DOI pending)

---

## Semantic Embeddings & Multilingual NLP

[6] Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using
    Siamese BERT-Networks*. EMNLP 2019.
    arXiv:1908.10084

[7] Pikuliak, M., et al. (2021). *SlovakBERT: Slovak Masked Language Model*.
    EMNLP 2021 Findings.
    HuggingFace: gerulata/slovakbert

[8] Conneau, A., et al. (2020). *Unsupervised Cross-lingual Representation Learning
    at Scale (XLM-R)*. ACL 2020.
    arXiv:1911.02116

[9] DeepPavlov. (2019). *Slavic-BERT NER*. BSNLP 2019.
    GitHub: deeppavlov/Slavic-BERT-NER

---

## Coordinated Inauthentic Behavior

[10] Nizzoli, L., Tardelli, S., Avvenuti, M., Cresci, S., & Tesconi, M. (2021).
     *Coordinated Behavior on Social Media in 2019 UK General Election*.
     ICWSM 2021.
     arXiv:2008.08370

[11] Cresci, S., Nizzoli, L., et al. (2022). *The Spread of Propaganda by
     Coordinated Communities on Social Media*. ACM CSCW 2022.
     DOI: 10.1145/3501247.3531543

---

## Source Credibility & Trust

[12] Falcone, R., & Castelfranchi, C. (2001). *Social Trust: A Cognitive Approach*.
     In: Trust and Deception in Virtual Societies. Springer.

[13] *Addressing Misinformation in Online Social Networks: Diverse Platforms and
     the Potential of Multiagent Trust Modeling*. MDPI Information 2020.
     DOI: 10.3390/info11110539

---

## Uncertainty Estimation

[14] Xiong, M., et al. (2023). *Can LLMs Express Their Uncertainty? An Empirical
     Evaluation of Confidence Elicitation in LLMs*.
     arXiv:2306.13063

---

## Ensemble & Bayesian Methods

[15] Hoeting, J.A., Madigan, D., Raftery, A.E., & Volinsky, C.T. (1999).
     *Bayesian Model Averaging: A Tutorial*. Statistical Science 14(4).

[16] Cesa-Bianchi, N., & Lugosi, G. (2006). *Prediction, Learning, and Games*.
     Cambridge University Press.

---

## Security & Adversarial

[17] Greshake, K., et al. (2023). *More than you've asked for: A Comprehensive
     Analysis of Novel Prompt Injection Threats to Application-Integrated Large
     Language Models*. arXiv:2302.12173

[18] Perez, E., et al. (2022). *Red Teaming Language Models with Language Models*.
     arXiv:2202.03286

---

## Visual & Deepfake Detection

[19] Chandra, N., et al. (2025). *Deepfake-Eval-2024: A Multi-Modal In-the-Wild
     Deepfake Detection Benchmark*. arXiv:2503.02857

[20] *Evolving from Single-Modal to Multi-Modal Facial Deepfake Detection:
     Progress and Challenges*. arXiv:2406.06965

[21] *Passive Deepfake Detection Across Multi-Modalities: A Comprehensive Survey*.
     arXiv:2411.17911

---

## Knowledge Graphs

[22] Vrandečić, D., & Krötzsch, M. (2014). *Wikidata: A Free Collaborative
     Knowledgebase*. Communications of the ACM 57(10).
     DOI: 10.1145/2629489

---

## Inter-Annotator Agreement

[23] Krippendorff, K. (2004). *Content Analysis: An Introduction to Its
     Methodology* (2nd ed.). Sage Publications.

[24] Hayes, A.F., & Krippendorff, K. (2007). *Answering the Call for a Standard
     Reliability Measure for Coding Data*. Communication Methods and Measures 1(1).

---

## Speculative / Aspirational (Wave 5–6, quarantined)

> [!WARNING]
> The following references underpin speculative agents quarantined under
> `agents/speculative/`. They are aspirational research directions, NOT
> production-ready implementations.

[25] Ha, D., & Schmidhuber, J. (2021). *Recurrent Neural Networks for Control*.
     Nature Machine Intelligence.
     arXiv:2006.04439 — basis for Liquid Neural Network detector (Wave 5)

[26] Raposo, D., et al. (2024). *Mixture-of-Depths: Dynamically Allocating Compute
     in Transformer Models*. arXiv:2404.02258 — basis for MoD router (Wave 5)
