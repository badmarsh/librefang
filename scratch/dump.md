## msm-historical-audit-engine
**Description:** Multi-agent historical audit engine: Agentic Archive Retrieval, MoE debate on predictive accuracy, and ontological mapping of narrative shifts.
**Current Trigger:** manual_audit_request / 
**Steps (5):** agentic-archive-retrieval, collect-extractions, historical-outcome-alignment, moe-debate-audit, ontological-narrative-mapping
**Final Output Var:** accountability_report

## meme-deepfake-triage
**Description:** Dedicated visual disinformation pipeline: Multimodal VLM reasoning, deepfake indicators, adaptive debunk generation.
**Current Trigger:** visual_flag / 
**Steps (6):** fetch-asset, metadata-parsing, vlm-forensics, generate-overlay, escalate-to-inquisitor, deliver-visual-debunk
**Final Output Var:** delivery_result

## consensus-vote-protocol-v1
**Description:** Multi-model consensus gate: MoE routing, rubric-driven arbitration, multi-turn reflection.
**Current Trigger:** claim_verified / 
**Steps (8):** provenance-init, complexity-router, vote-deep-reasoning, vote-large-model, collect-votes, debate-reflection, arbiter-rubric-decision, route-decision
**Final Output Var:** routing_result

## coordinated-debunk-engine-v2
**Description:** Deep investigation pipeline: ontology lookup -> parallel deep research + archive audit -> optional adversarial check -> verdict synthesis -> graph update -> accountability action.
**Current Trigger:** manual_escalation / 
**Steps (7):** ontology-lookup, deep-research, archive-audit, adversarial-check, synthesize-verdict, update-ontology, accountability-action
**Final Output Var:** accountability_result

## dashboard-kpi-tracker
**Description:** Calculates research velocity, fact-check accuracy, and agent uptime from session-logs and agent states.
**Current Trigger:** scheduled / */15 * * * *
**Steps (3):** fetch_logs, calculate_kpis, push_to_dashboard
**Final Output Var:** None

## desolator-omni-ingest
**Description:** State-of-the-art OSINT monitor: dynamic cross-lingual ingestion, LLM-based disinformation triage, graph enrichment, and orchestrator handover.
**Current Trigger:** scheduled / */15 * * * *
**Steps (6):** dynamic-osint-ingestion, collect-raw-claims, cross-lingual-translation, disinfo-triage-vlm, wikidata-graph-enrichment, orchestrator-handover
**Final Output Var:** handover_status

## disinfo-pipeline
**Description:** End-to-end disinformation detection: Firecrawl web backend, claim extraction, orchestrator gate, parallel multi-agent verification, instance-hardness routing, adversarial mini-debate, Bayesian+F2 consensus, multi-window CIB, and impact comms.
**Current Trigger:** manual / 
**Steps (14):** ingest, sanitize, orchestrate, stance-detect, verify-fast, verify-deep, verify-visual, verify-kg, narrative-scan, consensus, investigate, legal-gate, communicate, archive_record
**Final Output Var:** archived_record

## coordinated-debunk-engine
**Description:** Deep investigative fact-checking and debunking of high-priority malicious claims using multi-source verification.
**Current Trigger:** manual / 
**Steps (7):** deconstruct-claim, deep-evidence-gathering, source-integrity-check, cross-check-diversity, craap-verification, qa-review, generate-debunking-report
**Final Output Var:** debunking_report

## social-impact-accountability-v2
**Description:** Notifies advertisers, regulators, and civil society on confirmed high-confidence verdicts. Supports DOCX letters, email/webhook delivery, and outbound phone calls.
**Current Trigger:** verdict_confirmed / 
**Steps (5):** determine-tier, draft-advertiser-notice, draft-regulator-complaint, phone-outreach, deliver-notifications
**Final Output Var:** delivery_confirmations

## feedback-ingestion
**Description:** Ingests human-confirmed verdicts from writer review queue into ensemble.agent_stats. Enables Bayesian weight adaptation (Improvement 1) to converge. Wires the open feedback loop identified in audit.
**Current Trigger:** manual / 
**Steps (4):** read-review-queue, ingest-to-ensemble-stats, trigger-weight-recompute, archive-feedback-record
**Final Output Var:** feedback_archive_record

## gart-evaluation-cart
**Description:** Continuous Automated Red Teaming (CART) for pipeline bypass evaluation with root cause analysis.
**Current Trigger:** manual / 
**Steps (4):** synthesize-adversarial-articles, evaluate-bypass-rate, diagnostic-root-cause, log-gart-results
**Final Output Var:** gart_evaluation_logged

## health-check-critical
**Description:** Probes the researcher-hand and collector-hand with a benign request to ensure they are online and responding within thresholds. Auto-restarts on failure.
**Current Trigger:** scheduled / */30 * * * *
**Steps (3):** probe_collector, probe_researcher, assert_health
**Final Output Var:** None

## health-check
**Description:** Daily end-to-end pipeline validator. Injects a known-false test claim, asserts arbiter returns FALSE with confidence >= 0.75. Alerts operator on failure.
**Current Trigger:** scheduled / 0 6 * * *
**Steps (6):** inject, hc-verify-fast, hc-verify-deep, hc-consensus, assert, alert
**Final Output Var:** None

## investigative-report-generation-v1
**Description:** Full investigative journalism pipeline: actor mapping, timeline reconstruction, evidence chain assembly, impact assessment, report generation, editorial handoff or auto-publish.
**Current Trigger:** investigation_commissioned / 
**Steps (6):** actor-mapping, timeline-reconstruction, evidence-chain-assembly, impact-assessment, report-synthesis, editorial-routing
**Final Output Var:** editorial_result

## narrative-campaign-scan-v1
**Description:** Scheduled proactive disinformation campaign detector: clusters recent claims, scores for coordinated inauthentic behaviour, triggers investigator on high-CIB clusters.
**Current Trigger:** scheduled / 0 */6 * * *
**Steps (3):** claim-cluster-scan, high-cib-triage, investigator-dispatch
**Final Output Var:** dispatch_result

## agentic-security-redteam
**Description:** Advanced agentic security red-teaming: automated exploit generation, dynamic sandboxed execution checks, and rigorous zero-day vulnerability reasoning.
**Current Trigger:** code_push / 
**Steps (5):** codebase-surface-mapping, automated-exploit-generation, collect-exploits, dynamic-sandbox-execution, zero-day-vulnerability-reasoning
**Final Output Var:** vulnerability_report

## self-healing-pipeline
**Description:** Monitors pipeline runs and applies the self-improving-agent skill to automatically propose and implement fixes for failures.
**Current Trigger:** scheduled / 30 * * * *
**Steps (4):** fetch_errors, analyze_failures, apply_fix, alert_operator
**Final Output Var:** None

