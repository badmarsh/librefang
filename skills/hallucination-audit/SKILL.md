# Hallucination Audit Skill

This skill analyzes agent outputs or texts against the typed hallucination taxonomy (`ontology/hallucination_types.toml`). 

## Triggers
- Automatic execution during the `disinfo-pipeline` evaluation.
- Triggered on outputs before final aggregation.

## Modes
- **FAST**: Quick pass checking for basic factual inconsistencies (H-FACT, H-REF).
- **DEEP**: Exhaustive check against all 7 hallucination types.
- **DEBATE**: Used when a `HARD_FLAG` is issued. Invokes multi-agent debate to resolve ambiguity.

## Memory Namespace Contract
- Audit results are written to the `audit.hallucination` memory namespace.
- If a hallucination is detected, `audit.hallucination.flagged = true`, and `audit.hallucination.type` is set to the corresponding taxonomy ID.
- Outputs with `HARD_FLAG` verdict are escalated to the debate stage.

## Prompt Injection
The skill reads `ontology/hallucination_types.toml` and dynamically injects the `prompt_fragment` corresponding to the selected mode into the LLM context.
