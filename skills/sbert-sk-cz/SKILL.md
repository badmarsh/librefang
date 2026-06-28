---
name: sbert-sk-cz
description: "Generates semantic embeddings for Slovak and Czech text using gerulata/slovakbert. Used for claim deduplication and semantic search."
---

# SlovakBERT Semantic Similarity Skill

This skill allows agents (e.g., `disinfo-orchestrator`, `cross-lingual-aligner`) to leverage the `sbert_embed_sk_cz` MCP tool for high-quality, dense vector representations of Slavic languages.

## Purpose
Traditional keyword search fails on heavily inflected languages like Slovak and Czech. By mapping claims to a 768-dimensional semantic space, we can accurately identify if a newly ingested claim is a paraphrase of a previously debunked narrative.

## Instructions for the Agent

When you receive a new claim to verify:
1. **Embed the Claim:** Call the `sbert_embed_sk_cz` MCP tool with the exact text of the claim.
   *Note: Ensure any curly quotes (“ or ”) are normalized to straight quotes (") before calling the tool, as the model is sensitive to this.*
2. **Retrieve Past Claims:** If you have access to a vector database (like Qdrant or Milvus via another tool), use the generated 768-float array to query for cosine similarity.
3. **Deduplication Threshold:** If a past claim matches with a cosine similarity > **0.88**, consider it a direct paraphrase.
   - If the past claim was already verified as `DISINFORMATION`, you may fast-track the current claim or use the previous evidence.

## Example Usage

**Input Claim:**
"Vláda potajomky chystá novú daň z nehnuteľností."

**Action:**
```json
{
  "tool": "sbert_embed_sk_cz",
  "arguments": {
    "text": "Vláda potajomky chystá novú daň z nehnuteľností."
  }
}
```

**Expected Output:**
A JSON array containing 768 floating-point numbers representing the semantic meaning of the sentence.
