# Cross-Lingual Semantic Laundering Upgrade

## Hypothesis
The `cross_lingual_analyzer.py` agent failed to recognize semantically equivalent disinformation strings across the Russian-Slovak boundary (score: 0.612, threshold: 0.85). The usage of `paraphrase-multilingual-MiniLM-L12-v2` is insufficient for the strict alignment needed between these specific Slavic languages in high-security disinformation environments. 

## Proposal
Upgrade the embedding model to `BAAI/bge-m3`, the state-of-the-art multilingual model that excels in cross-lingual retrieval and semantic alignment across 100+ languages including strict structural alignment for Russian and Slovak.

## Execution
Modified `scripts/cross_lingual_analyzer.py` to instantiate `SentenceTransformer("BAAI/bge-m3")`.

## Evaluation
The updated model correctly aligned the Russian known-bad claim with the Slovak translated claim, yielding a cosine similarity of 0.8601, passing the 0.85 threshold. The `test_semantic_laundering_detection` test is now passing.
