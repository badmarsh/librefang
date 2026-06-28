---
name: disarm-skill
description: "Maps disinformation behavioral tactics, techniques, and procedures (TTPs) using the DISARM framework (T0000-series). Used to structurally classify how a narrative is manipulated."
---

# DISARM TTP Mapping Skill

This skill allows agents (specifically the `disarm-hunter` or `orchestrator`) to map unstructured claims and narratives to formal DISARM (Disinformation Analysis and Risk Management) Framework TTPs.

## Purpose
By tagging claims with TTPs (e.g., T0007, T0023, T0143), downstream systems (like Memgraph and the `compliance-officer`) can track the *behavior* of the disinformation, not just its content.

## Common TTPs to Identify

| TTP ID | Phase | Name | Description |
|---|---|---|---|
| **T0007** | PREPARE | Create Inauthentic Accounts | Use of botnets or fake personas to seed the claim. |
| **T0023** | EXECUTE | Develop Narrative | Creating a false but compelling story to explain an event. |
| **T0038** | EXECUTE | Manipulate Media | Deepfakes, cheapfakes, or misleadingly cropped images/videos. |
| **T0089** | EXECUTE | Flood Information Space | High-volume posting to drown out authentic counter-narratives. |
| **T0143** | ASSESS  | Monitor Reactions | Assessing audience engagement to iterate on the narrative. |

## Instructions for the Agent

When analyzing a claim or narrative cluster:
1. Examine the ingestion source and associated metadata.
2. Determine if any manipulation behaviors (bot-like repetition, deepfakes, emotional appeals) are present.
3. Map these behaviors to the appropriate DISARM TTPs.

## Output Schema Contract

You MUST write the mapping results to memory using `memory_store` to the key `disarm_hunter.session_results` exactly matching this JSON schema:

```json
[
  {
    "ttp_id": "T0023",
    "phase": "EXECUTE",
    "name": "Develop Narrative",
    "verdict": "PASS",
    "evidence": "The claim relies on a fabricated backstory about foreign biolabs."
  }
]
```

*Note: The `verdict` field must be "PASS" (TTP detected) or "FAIL" (checked but not detected).*
