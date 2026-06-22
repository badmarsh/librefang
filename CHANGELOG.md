# Changelog

All notable changes to the Mediálny Dezolator pipeline will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2026-06-22

### Added
- **Multi-Source Credibility Registry**: Integrated NewsGuard, MBFC, EUvsDisinfo, and Konšpirátori.sk ratings with weighted-mean consensus fusion.
- **Decomposed Uncertainty Routing**: Implemented explicit aleatoric (`u_ale`) and epistemic (`u_epi`) uncertainty estimation, with uncertainty-gated routing paths (Fast-path, Ambiguous HITL, Targeted/Deep Verify, Debate).
- **Information Laundering Detection**: Added tracking of narrative propagation from known-bad domains within the last 72 hours and automated neutrality overrides on laundering risk.
- **Calibration Corpus**: Added a 200-article Slovak calibration dataset (`tests/fixtures/calibration_corpus.json`) and evaluation metrics logic.
- **Inter-Annotator Agreement**: Added Krippendorff's alpha calculation on borderline reviews to workflows.
- **Ethics Framework & Guidelines**: Documented legal defamation context, appeals procedure, and annotation instructions.
- **Weekly GART Evaluation**: Added a weekly red-teaming loop to monitor bypass rates.
- **Speculative Agent Warning Banners**: Created READMEs with warning banners for experimental agents.

### Changed
- **Ensemble Weight Re-calibration**: Adjusted baseline weights to w_src=0.08/0.06 and w_wiki=0.26/0.22 to prioritize verifiable checks.
- **ML Classifier BERT Upgrade**: Upgraded FastAPI endpoint and training scripts to support SlavicBERT/SlovakBERT sequence classifiers with robust TF-IDF fallback.
- **CIB Detector SBERT Integration**: Upgraded coordinated sharing check to use SBERT semantic similarity (>= 0.75), account posting rate, and network amplification signals.

### Removed
- **Speculative Agents Quarantined**: Moved `qsvm-classifier`, `zk-attestor`, and `gart-synthesizer` to `agents/speculative/` to isolate untested/hardware-dependent components.
