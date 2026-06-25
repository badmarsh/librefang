# Wave 5 Adaptation Plan: SlovakBERT Post-2025

Based on the methodologies from **Don't Stop Pretraining: Adapt Language Models to Domains and Tasks** (Gururangan et al., arXiv:2004.10964).

## 1. Objective
Adapt the existing `SlovakBERT` model (currently trained on pre-2025 `FakeNewsDetection_DRES` data) to emerging post-2025 disinformation narratives in the Slovak domain.

## 2. Procedure
1. **Domain-Adaptive Pretraining (DAPT)**:
   - Construct a large corpus of unlabeled Slovak news/social media data from 2025 onwards.
   - Continue masked language modeling (MLM) pretraining on SlovakBERT using this corpus.
2. **Task-Adaptive Pretraining (TAPT)**:
   - Identify the unlabeled subset of the task-specific post-2025 disinformation dataset.
   - Run additional MLM pretraining strictly on this task dataset.
3. **Fine-tuning**:
   - Fine-tune the DAPT+TAPT adapted model on the labeled post-2025 ground truth targets.

## 3. Data Requirements
- ~5GB unlabeled Slovak webtext (post-2025).
- Task-specific dataset: Curated set of newly emerging coordination strategies, deepfakes, and political narratives.

## 4. Rollback
If the adapted model exhibits catastrophic forgetting on pre-2025 historical data (F1 drop > 5%), we will revert to the baseline `SlovakBERT` and utilize an ensemble approach.
