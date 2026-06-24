# LibreFang Workflow Inventory

This document details the inventory of workflows available in the `workflows/` directory, categorized by their theoretical foundations and intended functions.

## 1. Visual & Multimedia Forensics
**Workflows:** `c1a4f7d2-meme-deepfake-triage.json`, `visual-debunk.json`, `e32083dc-972f-412e-8d5d-7ee1ae5e1655.json`

Pipelines that fetch assets, extract text via OCR, and run VLM prompts for manipulation detection, ultimately generating fact-check overlays. They leverage cross-modal consistency checking and branch into specialized forensics (e.g., pixel-level deepfake vs. layout anomaly).

## 2. Multi-Agent Consensus & Deep Fact-Checking
**Workflows:** `consensus-vote.json`, `d9b2e851-coordinated-debunk-engine-v2.json`, `coordinated-debunk-engine`, `investigative-report-generation.json`, `msm-archive-audit.json`

Mixture-of-Experts (MoE) patterns where claims are evaluated by multiple LLM backends (deep reasoning, retrieval, large models). Results are merged via Bayesian weighting by an Arbiter, occasionally triggering an adversarial "Debate" phase on high variance.

## 3. End-to-End Orchestration & Monitoring
**Workflows:** `disinfo-pipeline.toml`, `e8d5c310-watchdog-osint-full-pipeline.json`, `osint-dezinformacia-monitor.json`, `high-impact-misinfo-monitor.json`

Continuous ingest pipelines that fetch from OSINT feeds, translate content, run ML classifiers, and orchestrate full end-to-end multi-stage processing using native topological DAG execution.

## 4. Narrative & Campaign Clustering
**Workflows:** `narrative-campaign-scan.json`

Proactive scanning pipelines that cluster recent claims to detect Coordinated Inauthentic Behavior (CIB) and trigger investigations. These use multi-window CIB analysis to detect both swarms and slow-burn amplification campaigns.

## 5. System Health, Red-Teaming, & Self-Healing
**Workflows:** `gart-evaluation.toml`, `gart-stress-test.toml`, `self-healing-pipeline.toml`, `feedback-ingestion.toml`, `health-check.toml`, `health-check-critical.toml`, `dashboard-kpi-tracker.toml`

Scheduled infrastructure pipelines that synthesize adversarial articles (GART) to measure bypass rates, ingest human feedback for continuous weight adaptation, track system KPIs, and attempt multi-turn self-healing on errors.

## 6. Accountability & Impact Comms
**Workflows:** `f3c7a924-social-impact-accountability-v2.json`, `social-impact-accountability.json`

Responsible for the delivery of final verdicts to external channels, generating DOCX letters, firing webhooks, and orchestrating outbound communications to advertisers and regulators.
