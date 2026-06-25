# Implementation Plan: Project Dezolator Temporal Upgrade

## 1. Analysis against the Quintuple Disruption Matrix

**The Weakest Link:** 
The `ml-classifier` agent currently relies on `gerulata/slovakbert`, a frozen transformer model whose weights pre-date 2025. It is fundamentally naive to post-2025 emerging disinformation vectors (e.g., 2026 elections, 2026 EU regulations, NATO operations in the Tatras). This represents a catastrophic **Quality** degradation and an **Integration** gap, as the fast-verification pass lacks temporal awareness, artificially degrading our F1-score to ~0.500 on novel narratives. Furthermore, the previous evaluation scripts used a fraudulent keyword-matching bypass, masking this architectural flaw.

**Quintuple Disruption Matrix Alignment:**
- **Quality:** Fixing this will eliminate the blind spot for post-2025 narratives, pushing F1-scores back above the 0.75 target threshold for emerging claims.
- **Quantity:** Fast-pass ML inference must remain scalable. Instead of abandoning the low-latency CPU-friendly transformer, we will augment it.
- **Integration:** The `verify-fast` stage must integrate with the Temporal Knowledge Graph without triggering the expensive 120s `verify-deep` path for every claim.
- **AI:** Leveraging semantic retrieval (Graphiti-style memory) or a lightweight RAG injection into the ML-classifier context.
- **Niche:** Perfectly calibrated for the Slovak disinformation landscape, where narratives shift rapidly around regional geopolitical events.

## 2. Proposed Architectural Refactoring

Instead of abandoning `gerulata/slovakbert` (which is still highly effective for morphological capturing), we will introduce a **Temporal Knowledge Graph Sync (TKG-Sync)** mechanism.

1. **Entity Extraction & Temporal Context Retrieval:**
   We will update `scripts/serve_ml_classifier.py` and the `ml-classifier` agent to conditionally query a local Temporal Knowledge Graph (or SQLite embedding cache) when an extracted entity has a high temporal novelty score (e.g., "2026", "voľby 2026").
   
2. **Dynamic Fallback to Llama-3 70B:**
   When the ML classifier detects out-of-distribution (OOD) terms or high uncertainty (as computed by the `uq-scorer`), it should dynamically route the claim to the `fallback_models` (Llama-3 70B via NVIDIA API) *with* injected temporal context, rather than failing silently.

3. **Evaluation Framework Overhaul:**
   We have already replaced the fraudulent keyword mock in `scripts/eval_slovak_post2025.py` with actual API calls to the ML classifier endpoint. We will ensure the test suite reflects this.

## 3. Execution Steps

1. **Modify `serve_ml_classifier.py`:** Implement out-of-distribution (OOD) detection based on term frequency and temporal keywords.
2. **Update `agent.toml`:** Add explicit routing instructions for the `ml-classifier` to leverage `fallback_models` for temporally novel claims.
3. **Calibrate Data:** Inject temporal context anchors into the ontology or cache.
4. **Test:** Run the CI/CD test suite (`test_pipeline.py`) to verify the F1-score climbs back up.
