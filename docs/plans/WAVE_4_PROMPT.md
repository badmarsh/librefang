═══════════════════════════════════════════════════════════════════
  LIBREFANG / MEDIÁLNY DEZOLATOR — WAVE 4 IMPLEMENTATION PROMPT
  Repository: badmarsh/librefang  (branch: main)
  Generated from: deep academic research session, June 22 2026
═══════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTEXT — READ BEFORE ACTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are working inside the private GitHub repository badmarsh/librefang.
The project is "Mediálny Dezolator" — an MCP-orchestrated, multi-agent
disinformation-detection pipeline targeting Slovak, Czech, and Russian-language
media (pipeline version v3.1.0, just released).

Current repo layout (branch: main):
  .gitignore  CHANGELOG.md  CITATION_AUDIT.md  README.md
  config.toml  cron_jobs.json  custom_models.json
  migration_report.md  models.list  nginx.conf
  agents/    bin/    data/    docs/    ontology/
  pipelines/ scripts/ skills/ tests/ workflows/

Known agents (dirs under agents/):
  arbiter, archivist, browser-hand, cib-detector, claim-decomposer,
  claim-extractor, clip-hand, coherence-checker, collector-hand,
  cross-lingual-aligner, dennikn, disinfo-orchestrator, impact-comms,
  injection-shield, inquisitor, investigator, kg-consistency-checker,
  ml-classifier, narrative-tracker, predictor-hand, queue-monitor,
  researcher-hand, source-rater, speculative/, stance-detector,
  temporal-checker, triplet-fact-checker, visual-analyst, watchdog,
  wiki-checker, writer

Pipeline ensemble weights (current, v3.1.0):
  ml-classifier w=0.26 | wiki-checker w=0.22 | coherence-checker w=0.16
  triplet-fact-checker w=0.24 | source-rater w=0.12
  P_fake = Σ wᵢ × scoreᵢ   (Bayesian + F2 adaptation)

Instance-hardness routing:
  H = u_epi × (1 − max_agent_conf)
  H < 0.25  → ensemble_fast     (~60 % of claims)
  0.25 ≤ H < 0.55 → targeted_verify  (inquisitor 3-src)
  H ≥ 0.55  → deep_verify       (inquisitor 10-src + HITL flag)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCOPE — WHAT THIS PROMPT ASKS YOU TO DO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is a WAVE 4 academic uplift across four work-streams:

  A. Fix every broken / mismatched citation in CITATION_AUDIT.md
     and propagate correct references to README.md

  B. Strengthen 7 existing agents with grounded scientific methods

  C. Add 4 new, real (non-speculative) capabilities backed by
     peer-reviewed literature found in the research session

  D. Update CHANGELOG.md with a [4.0.0] entry, bump pipeline version
     in README.md to v4.0.0, and make all config/TOML consistent

All changes must pass:
  python3 -c "import tomllib; tomllib.load(open('config.toml','rb'))"
  python3 tests/test_pipeline.py

No speculative or fiction-science additions. Every new feature must
be mappable to a real paper cited below.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WORK-STREAM A — CITATION FIXES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Edit CITATION_AUDIT.md and README.md to replace all UNVERIFIED /
MISMATCHED entries with the following authoritative papers.
Keep the same table/section format already in the files.

REPLACEMENT MAP (old placeholder → correct citation):

  Improvement 1 (Bayesian weight adaptation):
    OLD: arXiv:2310.01555  [UNVERIFIED]
    NEW: Bayesian Model Averaging is foundational ML;
         cite instead the survey grounding your online update rule:
         Opitz & Maclin (1999) "Popular Ensemble Methods: An Empirical
         Study", JAIR 11, pp. 169–198.
         Also add: Hoeting et al. (1999) "Bayesian Model Averaging:
         A Tutorial", Statistical Science 14(4):382–417.

  Improvement 2 (Semantic claim deduplication — SBERT):
    OLD: arXiv:2305.14325  [MISMATCHED — this is the debate paper]
    NEW: Reimers & Gurevych (2019). "Sentence-BERT: Sentence Embeddings
         using Siamese BERT-Networks." EMNLP 2019. arXiv:1908.10084.
    NOTE: Move the debate paper (arXiv:2305.14325) to Improvement 14
         where it actually belongs (adversarial mini-debate).

  Improvement 3 (Source credibility 5th ensemble signal):
    OLD: arXiv:2401.17786  [UNVERIFIED]
    NEW: Falcone & Castelfranchi (2001).
         "Social Trust: A Cognitive Approach." In Trust and Deception
         in Virtual Societies. Springer. (Multi-agent trust modelling.)
         + Horne et al. (2019). "Rating the quality of evidence and
         recommendations." BMJ Evidence-Based Medicine.
         Use these to frame your credibility registry as a
         multi-source Bayesian trust aggregation.

  Improvement 4 (CIB detector):
    OLD: arXiv:2302.07934  [MISMATCHED — cosmology paper]
    NEW (primary): Nizzoli, L., Tardelli, S., Avvenuti, M., Cresci, S.,
         & Tesconi, M. (2021). "Coordinated Behavior on Social Media in
         the 2019 UK General Election." ICWSM 2021. arXiv:2008.08370.
    NEW (secondary): Nizzoli et al., Zenodo dataset doi:10.5281/zenodo.4647893
    NEW (tertiary): Cresci et al. (2022). "The Spread of Propaganda by
         Coordinated Communities on Social Media." ACM WebSci.
         doi:10.1145/3501247.3531543
    Update cib-detector/agent.toml comment block with all three.

  Improvement 7 (Slovak NER entity preservation):
    OLD: arXiv:2305.09586  [UNVERIFIED]
    NEW: Ardevop-sk/sk-bert-ner: Training BERT for NER in Slovak
         (GitHub, 2020). https://github.com/Ardevop-sk/sk-bert-ner
         + Raychani/Text_Parsing_Methods_Using_NLP:
         SlovakBERT-based NER for Slovak.
         https://github.com/Raychani1/Text_Parsing_Methods_Using_NLP
         + SlovakBERT CoNLL2003-SK-NER (HuggingFace):
         ju-bezdek/slovakbert-conll2003-sk-ner  (P=0.819, R=0.839, F1=0.829)

  Improvement 9 (Cross-lingual aligner):
    OLD: arXiv:2209.05056  [UNVERIFIED]
    NEW: DeepPavlov Slavic-BERT-NER (GitHub, 2019):
         github.com/deeppavlov/Slavic-BERT-NER
         Covers BG/CS/PL/RU NER on BSNLP-2019.
         + For multilingual query expansion:
         Conneau et al. (2020). "Unsupervised Cross-lingual
         Representation Learning at Scale." ACL 2020. arXiv:1911.02116.

  Improvement 14 (Adversarial mini-debate):
    OLD: github.com/hanshenmesen/Debate-to-Detect  [no arXiv anchor]
    NEW (primary): Du, Y., Li, S., Torralba, A., Tenenbaum, J.B., &
         Mordatch, I. (2023). "Improving Factuality and Reasoning in
         Language Models through Multiagent Debate." ICML 2024.
         arXiv:2305.14325.  ← this is the paper that was misplaced on
         Improvement 2; correct home is here.
    NEW (secondary): Ding, Z. et al. (2025). "A Multi-Agent Framework
         with Automated Decision Rule Optimization for Cross-Domain
         Misinformation Detection." arXiv:2503.23329.

After edits, mark every fixed entry as [VERIFIED] with the correct
paper title, authors, venue, and arXiv/DOI link.
Mark the two previously-verified ones (Improvements 5, 6, 8, 10)
as [VERIFIED — UNCHANGED].

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WORK-STREAM B — STRENGTHEN EXISTING AGENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For each agent listed below, make the changes described. Touch only
the files inside that agent's directory (primarily agent.toml and
any Python files present). Do NOT remove existing functionality.

──────────────────────────────────────────
B1. agents/cib-detector/
──────────────────────────────────────────
Current: 3-window temporal scoring + SBERT similarity ≥ 0.75.
Research finding: Nizzoli et al. show that coordination exists on
a CONTINUOUS spectrum, not a binary flag. The "superspreader
similarity network" uses weighted edges (cosine similarity of
posting behavior vectors).

Changes:
1. In agent.toml, add a [cib.coordination_index] section:
     method = "continuous_spectrum"    # Nizzoli et al. 2021
     superspreader_similarity_threshold = 0.70
     propagation_graph_enabled = true
     edge_weight_features = ["posting_rate", "content_overlap_sbert",
                              "repost_timing_delta_seconds"]

2. Add a [cib.propaganda_fusion] section (Cresci et al. 2022):
     propaganda_score_weight = 0.30   # fused into cib_score
     coordination_score_weight = 0.70
     # cib_score_final = propaganda_score_weight * propaganda_score
     #                 + coordination_score_weight * cib_score

3. Update the citations comment block at the top of agent.toml:
   # References:
   # - Nizzoli et al. (ICWSM 2021) arXiv:2008.08370
   # - Cresci et al. (WebSci 2022) doi:10.1145/3501247.3531543
   # - Nizzoli et al. dataset doi:10.5281/zenodo.4647893

──────────────────────────────────────────
B2. agents/ml-classifier/
──────────────────────────────────────────
Current: TF-IDF + Logistic Regression baseline; SlavicBERT/
SlovakBERT upgrade added in v3.1.0 CHANGELOG but needs grounding.

Research finding: SlovakBERT CoNLL2003-SK-NER achieves F1=0.829
on Slovak NER. Slavic-BERT-NER covers BG/CS/PL/RU. Both are
HuggingFace-compatible.

Changes:
1. In agent.toml, add a [classifier.bert] section:
     primary_model = "gerulata/slovakbert"
     ner_model = "ju-bezdek/slovakbert-conll2003-sk-ner"
     slavic_ner_model = "DeepPavlov/bert-base-slavic-ner"
     fallback_model = "tfidf_logistic_regression"
     fallback_trigger = "transformers_unavailable OR ram_mb < 4096"
     sequence_classification_max_length = 512
     # References: arXiv:1908.10084 (SBERT), sk-bert-ner GitHub 2020

2. Verify (or create) scripts/train_classifier.py references both
   models with try/except import guarding for the BERT path,
   falling back gracefully to TF-IDF+LR. Add a docstring header:
     """
     Slovak disinformation classifier.
     Primary: SlovakBERT (gerulata/slovakbert) sequence classification.
     NER: ju-bezdek/slovakbert-conll2003-sk-ner (F1=0.829 on CoNLL2003-SK).
     Fallback: TF-IDF + Logistic Regression (sklearn).
     Ref: Reimers & Gurevych (EMNLP 2019) arXiv:1908.10084
          sk-bert-ner: github.com/Ardevop-sk/sk-bert-ner
     """

──────────────────────────────────────────
B3. agents/wiki-checker/
──────────────────────────────────────────
Current: Wikidata SPARQL + Wikipedia NER verify (v1.2.0), w=0.22.
Research finding: Cross-lingual alignment across SK/CZ/DE/EN can
be grounded in Conneau et al. XLM-R (arXiv:1911.02116) and
DeepPavlov Slavic-BERT-NER for non-English entity linking.

Changes:
1. In agent.toml, add [wiki.cross_lingual]:
     xlmr_model = "xlm-roberta-base"
     slavic_ner_backend = "DeepPavlov/bert-base-slavic-ner"
     wikidata_languages = ["sk", "cs", "de", "en", "ru", "hu"]
     entity_linking_fallback = "exact_string_match"
     # Reference: Conneau et al. (ACL 2020) arXiv:1911.02116
     #            DeepPavlov/Slavic-BERT-NER github.com/deeppavlov/Slavic-BERT-NER

2. Update agent version to 1.3.0 and add a [meta.references] block.

──────────────────────────────────────────
B4. agents/visual-analyst/
──────────────────────────────────────────
Current: ELA, deepfake, OCR, meme overlay (v0.3.0). No benchmark
grounding. Research finding: Deepfake-Eval-2024 shows open-source
detectors drop ~50% AUC on 2024 in-the-wild content; multi-modal
audio-visual fusion is the direction of travel.

Changes:
1. In agent.toml, add [visual.benchmark]:
     eval_dataset = "Deepfake-Eval-2024"
     # doi: arXiv:2503.02857  (Chandra et al. 2025)
     expected_auc_floor = 0.65   # below this, trigger alert
     reevaluation_schedule = "weekly_gart"

2. Add [visual.multimodal]:
     audio_visual_fusion = true          # Phase 1: flag for future
     text_visual_fusion = true           # OCR → claim pipe
     modalities_active = ["image", "ocr_text"]
     modalities_planned = ["audio", "video"]
     # Ref: Tao et al. (2024) arXiv:2406.06965 (multi-modal deepfake survey)
     # Ref: Passive Deepfake Detection Survey arXiv:2411.17911

3. Update version to 0.4.0.

──────────────────────────────────────────
B5. agents/disinfo-orchestrator/
──────────────────────────────────────────
Current: Bayesian + F2 weights, instance-hardness routing,
adversarial mini-debate.
Research finding: Ding et al. (arXiv:2503.23329) show automated
decision-rule optimization over LLM-agent ensembles outperforms
manually-tuned thresholds on cross-domain misinfo.

Changes:
1. In agent.toml, add [orchestrator.decision_rules]:
     optimization_method = "automated_rule_search"  # Ding et al. 2025
     cross_domain_adaptation = true
     rule_search_trigger = "accuracy_drop_pct > 5"  # vs. calibration corpus
     # Reference: Ding et al. arXiv:2503.23329
     #            Du et al. (ICML 2024) arXiv:2305.14325 (debate grounding)

2. In agent.toml, update [orchestrator.debate]:
     grounding_paper = "arXiv:2305.14325"   # Du et al. — multiagent debate
     debate_rounds = 2
     arbiter_confidence_threshold = 0.75

──────────────────────────────────────────
B6. agents/source-rater/
──────────────────────────────────────────
Current: known-good/bad lists, multi-source credibility registry
(NewsGuard, MBFC, EUvsDisinfo, Konšpirátori.sk), w=0.12.
Research finding: academic grounding should be multi-agent trust
modelling (Falcone & Castelfranchi 2001) + the misinfo trust
frameworks from the agent-based misinfo survey.

Changes:
1. In agent.toml, add [source.trust_model]:
     aggregation_method = "weighted_bayesian_consensus"
     registry_sources = ["newsguard", "mbfc", "euvsDisinfo",
                         "konspiratori_sk", "media_bias_fact_check"]
     trust_decay_enabled = true
     trust_decay_halflife_days = 90
     # Reference: Falcone & Castelfranchi (2001) "Social Trust:
     #            A Cognitive Approach." Springer.
     # Reference: "Addressing Misinformation ... Multiagent Trust
     #            Modeling" (MDPI Information 2020)

2. Add a comment explaining that credibility is treated as a
   continuous Bayesian prior, not a binary flag.

──────────────────────────────────────────
B7. agents/inquisitor/
──────────────────────────────────────────
Current: deep 3/10-source adversarial fact-check. No explicit
uncertainty documentation.
Research finding: Xiong et al. arXiv:2306.13063 show that
verbalized LLM confidence is systematically overconfident;
sampling-based aggregation (e.g., consistency over N=10 samples)
improves calibration.

Changes:
1. In agent.toml, add [inquisitor.uncertainty]:
     confidence_elicitation = "sampling_consistency"  # Xiong et al.
     n_samples = 10       # for deep_verify path
     n_samples_targeted = 3
     overconfidence_correction = true
     u_ale_estimation = "variance_of_samples"
     u_epi_estimation = "entropy_of_sample_distribution"
     # Reference: Xiong et al. (NeurIPS 2023) arXiv:2306.13063

2. Update the docstring or comment header referencing the paper.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WORK-STREAM C — NEW CAPABILITIES (4 additions)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Each new capability is backed by a peer-reviewed paper found in
the research session. Implement as a new agent.toml (and stub
Python file if appropriate) in an existing or new agent directory.

──────────────────────────────────────────
C1. NEW: Cross-Domain Misinfo Robustness Evaluator
    Directory: agents/cross-domain-evaluator/
──────────────────────────────────────────
Motivation: Ding et al. (arXiv:2503.23329) show that LLM-based
misinfo detectors fail when domain shifts. Your pipeline currently
has no cross-domain evaluation harness.

Create agents/cross-domain-evaluator/agent.toml:

  [agent]
  name = "cross-domain-evaluator"
  version = "0.1.0"
  description = """
  Evaluates pipeline robustness across domain shifts (politics,
  health, economics, climate) using automated decision-rule probing.
  Triggers weight recalibration when cross-domain accuracy drops
  below threshold.
  Ref: Ding et al. (2025) arXiv:2503.23329
  """
  enabled = false        # activate after calibration corpus is ready
  trigger = "weekly_gart OR manual"

  [evaluation]
  domains = ["politics", "health", "economics", "climate", "sport"]
  accuracy_drop_threshold_pct = 8.0
  recalibration_trigger = "disinfo-orchestrator.decision_rules.rule_search"
  report_path = "output/cross_domain_eval.json"

  [meta]
  paper = "arXiv:2503.23329"
  authors = "Ding et al. (2025)"

Also create agents/cross-domain-evaluator/README.md with a brief
description and the paper citation.

──────────────────────────────────────────
C2. NEW: Multimodal Deepfake Benchmark Integration
    Directory: agents/visual-analyst/ (extend, not new dir)
    + scripts/eval_deepfake.py (new file)
──────────────────────────────────────────
Motivation: Deepfake-Eval-2024 (arXiv:2503.02857) shows a 50% AUC
drop for off-the-shelf detectors on 2024 in-the-wild media.

Create scripts/eval_deepfake.py:

  """
  Deepfake detector AUC evaluation against Deepfake-Eval-2024 benchmark.
  Run: python3 scripts/eval_deepfake.py --manifest data/deepfake_manifest.json

  Reference:
    Chandra et al. (2025). Deepfake-Eval-2024: A Multi-Modal In-the-Wild
    Deepfake Detection Benchmark. arXiv:2503.02857.
    Dataset: https://github.com/nuriachandra/Deepfake-Eval-2024
  """
  import argparse, json, pathlib

  BENCHMARK_METRICS = {
      "video_auc_sota": 0.50,   # arXiv:2503.02857 Table 1
      "audio_auc_sota": 0.52,
      "image_auc_sota": 0.55,
  }

  def evaluate(manifest_path: str) -> dict:
      """Load manifest and compute per-modality AUC vs. benchmark."""
      manifest = json.loads(pathlib.Path(manifest_path).read_text())
      results = {}
      for modality, records in manifest.items():
          # Placeholder: replace with real sklearn roc_auc_score call
          results[modality] = {
              "n": len(records),
              "auc": None,                       # filled by actual eval
              "benchmark_auc": BENCHMARK_METRICS.get(f"{modality}_auc_sota"),
          }
      return results

  if __name__ == "__main__":
      ap = argparse.ArgumentParser()
      ap.add_argument("--manifest", required=True)
      args = ap.parse_args()
      print(json.dumps(evaluate(args.manifest), indent=2))

──────────────────────────────────────────
C3. NEW: Slavic Cross-Lingual NER Upgrade
    Directory: agents/cross-lingual-aligner/
──────────────────────────────────────────
Motivation: DeepPavlov Slavic-BERT-NER covers BG/CS/PL/RU on
BSNLP-2019; XLM-R (Conneau et al. ACL 2020, arXiv:1911.02116)
gives robust cross-lingual sentence-level representations.

In agents/cross-lingual-aligner/agent.toml, add or update:

  [aligner.ner]
  slavic_ner_model = "DeepPavlov/bert-base-slavic-ner"
    # Covers: BG, CS, PL, RU — BSNLP-2019
    # Ref: github.com/deeppavlov/Slavic-BERT-NER
  slovak_ner_model = "ju-bezdek/slovakbert-conll2003-sk-ner"
    # F1=0.829 on CoNLL2003-SK
    # Ref: dataloop.ai/library/model/ju-bezdek_slovakbert-conll2003-sk-ner
  hungarian_ner_model = "SZTAKI-HLT/hubert-base-cc"
    # Placeholder for HU coverage

  [aligner.embeddings]
  xlmr_model = "xlm-roberta-base"
    # Conneau et al. (ACL 2020) arXiv:1911.02116
  sentence_embedding_model = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    # Reimers & Gurevych (EMNLP 2019) arXiv:1908.10084
  supported_languages = ["sk", "cs", "de", "en", "ru", "hu"]

  [aligner.wikidata]
  sparql_endpoint = "https://query.wikidata.org/sparql"
  q_id_cache_ttl_hours = 24
  political_entity_classes = ["Q5", "Q7278", "Q4164871", "Q9135"]
    # person, political party, political position, government

Update agent version to 0.2.0.
Add a [meta.references] section listing Conneau, Reimers, DeepPavlov.

──────────────────────────────────────────
C4. NEW: MCP Contract-Driven Observability
    Directory: agents/ top-level config
    File: config.toml (extend existing)
──────────────────────────────────────────
Motivation: "Operationalizing Multi-Agent Interoperability via
Contract-Driven Model Context Protocols" (IEEE 2026) shows 7.4%
improvement in integration success rate, 60.6% reduction in MTTR,
and 4.4× schema mismatch detection by using explicit capability
descriptors + semantic version negotiation over MCP.

In config.toml, add a [mcp.contracts] section:

  [mcp.contracts]
  enabled = true
  schema_validation = true
  semantic_version_negotiation = true
  capability_descriptors = true
  telemetry_structured = true
  failure_isolation = true
  p95_latency_overhead_ms = 18.4   # per paper Table 3
  schema_drift_detection = true
  # Reference: "Operationalizing Multi-Agent Interoperability via
  #   Contract-Driven MCP" IEEE 2026
  #   doi:10.1109/ACCESS.2026.11476405

Also add to config.toml under [observability]:

  [observability]
  prometheus_port = 9100
  health_port = 4200
  mcp_schema_mismatch_alert = true
  mcp_mediation_latency_p95_ms_threshold = 25.0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WORK-STREAM D — CHANGELOG + VERSION BUMP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Prepend a [4.0.0] entry to CHANGELOG.md:

## [4.0.0] - 2026-06-23

### Fixed — Academic Citations (CITATION_AUDIT Wave 4)
- **Improvement 1**: Replaced UNVERIFIED arXiv:2310.01555 with
  Opitz & Maclin (1999) JAIR + Hoeting et al. (1999) Stat.Sci.
  Bayesian Model Averaging references.
- **Improvement 2**: Replaced MISMATCHED arXiv:2305.14325 (debate paper)
  with correct Reimers & Gurevych SBERT paper (arXiv:1908.10084).
  Moved debate paper to its correct Improvement 14 slot.
- **Improvement 3**: Replaced UNVERIFIED arXiv:2401.17786 with
  Falcone & Castelfranchi (2001) Social Trust + MDPI trust modelling.
- **Improvement 4**: Replaced MISMATCHED cosmology arXiv with
  Nizzoli et al. ICWSM 2021 (arXiv:2008.08370) + Cresci et al.
  WebSci 2022 + Zenodo dataset doi:10.5281/zenodo.4647893.
- **Improvement 7**: Replaced UNVERIFIED arXiv:2305.09586 with
  Ardevop-sk/sk-bert-ner, Raychani NLP repo,
  SlovakBERT CoNLL2003-SK-NER (F1=0.829).
- **Improvement 9**: Replaced UNVERIFIED arXiv:2209.05056 with
  DeepPavlov/Slavic-BERT-NER + Conneau et al. XLM-R (arXiv:1911.02116).
- **Improvement 14**: Anchored to Du et al. ICML 2024 (arXiv:2305.14325)
  + Ding et al. 2025 (arXiv:2503.23329).

### Added — Agent Enhancements
- **cib-detector**: Continuous coordination-spectrum scoring
  (Nizzoli ICWSM 2021) + propaganda–coordination fusion
  (Cresci WebSci 2022).
- **ml-classifier**: SlovakBERT CoNLL2003-SK-NER (F1=0.829) +
  DeepPavlov Slavic-BERT-NER config; graceful TF-IDF fallback.
- **wiki-checker**: XLM-R cross-lingual embedding config;
  Wikidata political-entity class list extended; v1.3.0.
- **visual-analyst**: Deepfake-Eval-2024 benchmark floor (AUC≥0.65);
  audio-visual fusion flags; multimodal survey references; v0.4.0.
- **disinfo-orchestrator**: Automated decision-rule optimization
  (Ding et al. 2025); debate grounding updated to Du et al. ICML 2024.
- **source-rater**: Weighted Bayesian consensus trust model
  (Falcone & Castelfranchi 2001); trust decay half-life 90 days.
- **inquisitor**: Sampling-consistency confidence elicitation
  (Xiong et al. NeurIPS 2023, arXiv:2306.13063);
  u_ale = variance, u_epi = entropy over N=10 samples.

### Added — New Capabilities
- **agents/cross-domain-evaluator/**: Domain-shift robustness
  harness (Ding et al. arXiv:2503.23329); disabled by default.
- **scripts/eval_deepfake.py**: AUC evaluation harness vs.
  Deepfake-Eval-2024 (arXiv:2503.02857).
- **agents/cross-lingual-aligner/**: Slavic NER + XLM-R embeddings
  + multilingual SBERT config; v0.2.0.
- **config.toml [mcp.contracts]**: Contract-driven MCP observability
  (IEEE 2026 doi:10.1109/ACCESS.2026.11476405).

2. In README.md, change the pipeline version line to:
   Pipeline version: **v4.0.0** — 31 improvements across Waves 2–4.

3. Update the Wave 4 "Academic Grounding" table in README.md
   to mark all fixed citations with their correct references.
   Add a new "Wave 4 — Citation Repair & Academic Uplift" section
   below Wave 3.5 with a table of all 8 fixes above.

4. Confirm config.toml still passes TOML validation after your edits.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VALIDATION CHECKLIST — run before finalising
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ python3 -c "import tomllib; tomllib.load(open('config.toml','rb'))"
  → must exit 0

□ python3 tests/test_pipeline.py
  → all 3 golden-path fixtures (true/fake/ambiguous) must pass
  → P_fake tolerance ±0.10

□ grep -r "UNVERIFIED\|MISMATCHED" CITATION_AUDIT.md
  → should return 0 matches

□ grep "v4.0.0" README.md
  → should match exactly 1 line (the pipeline version header)

□ All new agent.toml files must include a [meta.references] block
  with at least one real paper title + DOI/arXiv ID.

□ No agent in agents/speculative/ should be enabled = true.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REFERENCE SUMMARY (all papers cited above)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[F1]  Avram, Groza, Lecu (2025). MCP-Orchestrated Multi-Agent System
      for Automated Disinformation Detection. arXiv:2508.10143. IEEE.

[F2]  Reimers & Gurevych (2019). Sentence-BERT: Sentence Embeddings
      using Siamese BERT-Networks. EMNLP 2019. arXiv:1908.10084.

[F3]  Nizzoli et al. (2021). Coordinated Behavior on Social Media
      in the 2019 UK General Election. ICWSM 2021. arXiv:2008.08370.

[F4]  Nizzoli et al. (2021). Dataset: Twitter — Coordinated Behavior
      2019 UK General Election. Zenodo. doi:10.5281/zenodo.4647893.

[F5]  Cresci et al. (2022). The Spread of Propaganda by Coordinated
      Communities on Social Media. ACM WebSci.
      doi:10.1145/3501247.3531543.

[F6]  Du, Li, Torralba, Tenenbaum, Mordatch (2023). Improving
      Factuality and Reasoning in LMs through Multiagent Debate.
      ICML 2024. arXiv:2305.14325.

[F7]  Ding et al. (2025). A Multi-Agent Framework with Automated
      Decision Rule Optimization for Cross-Domain Misinformation
      Detection. arXiv:2503.23329.

[F8]  Xiong et al. (2023). Can LLMs Express Their Uncertainty?
      An Empirical Evaluation of Confidence Elicitation in LLMs.
      NeurIPS 2023. arXiv:2306.13063.

[F9]  Park, J.S. et al. (2023). Generative Agents: Interactive
      Simulacra of Human Behavior. UIST 2023. arXiv:2304.03442.

[F10] Greshake et al. (2023). More than you've asked for: Prompt
      Injection Threats to Application-Integrated LLMs.
      arXiv:2302.12173.

[F11] Wu et al. (2023). AutoGen: Enabling Next-Gen LLM Applications
      via Multi-Agent Conversation. arXiv:2308.08155.

[F12] Conneau et al. (2020). Unsupervised Cross-lingual
      Representation Learning at Scale (XLM-R). ACL 2020.
      arXiv:1911.02116.

[F13] DeepPavlov/Slavic-BERT-NER. BG/CS/PL/RU NER on BSNLP-2019.
      github.com/deeppavlov/Slavic-BERT-NER

[F14] Ardevop-sk/sk-bert-ner. Slovak BERT NER.
      github.com/Ardevop-sk/sk-bert-ner

[F15] ju-bezdek/slovakbert-conll2003-sk-ner (HuggingFace).
      P=0.819, R=0.839, F1=0.829 on CoNLL2003-SK-NER.

[F16] Chandra et al. (2025). Deepfake-Eval-2024: A Multi-Modal
      In-the-Wild Deepfake Detection Benchmark. arXiv:2503.02857.

[F17] Tao et al. (2024). Evolving from Single-modal to Multi-modal
      Facial Deepfake Detection: Progress and Challenges.
      arXiv:2406.06965.

[F18] "Operationalizing Multi-Agent Interoperability via
      Contract-Driven Model Context Protocols." IEEE 2026.
      doi:10.1109/ACCESS.2026.11476405.

[F19] Falcone & Castelfranchi (2001). Social Trust: A Cognitive
      Approach. In Trust and Deception in Virtual Societies. Springer.

[F20] Hoeting et al. (1999). Bayesian Model Averaging: A Tutorial.
      Statistical Science 14(4):382–417.

[F21] Opitz & Maclin (1999). Popular Ensemble Methods: An Empirical
      Study. JAIR 11:169–198.

[F22] "Addressing Misinformation in Online Social Networks: Diverse
      Platforms and the Potential of Multiagent Trust Modeling."
      MDPI Information 11(11):539. 2020.
