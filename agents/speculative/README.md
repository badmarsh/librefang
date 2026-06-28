# ⚠️ Speculative Agents — Research Stubs Only

> [!WARNING]
> **NONE of the agents in this directory are operational.**
> They are research stubs, architectural experiments, or designs requiring hardware that is not available.
> They are NOT loaded by any pipeline stage. They do NOT affect any verdict or ensemble output.

This directory contains agent manifests that document **future research directions** only.

| Agent | Reason for Quarantine |
|---|---|
| `gart-synthesizer/` | Promoted to `agents/gart-synthesizer/` (Wave 3.5). This copy is a historical stub only. |
| `qsvm-classifier/` | Requires Google Willow 105-qubit QPU — hardware unavailable. Classical simulation does not provide the claimed speedup. |
| `zk-attestor/` | Historical stub. Promoted to `agents/zk-attestor/` (Wave 5). Production agent satisfies the `zk-attestation` pipeline stage. Requires compiled Halo2 proving key — degrades gracefully when unavailable. |
| `tgn-cib-detector/` | Historical stub. Promoted to `agents/tgn-cib-detector/` (Wave 5). Production agent runs TGN inference via `scripts/tgn_inference.py` and writes to `cib_score` in shared memory. Requires GPU. |
| `visual-claim-verifier/` | Historical stub. Promoted to `agents/visual-claim-verifier/` (Wave 5). Production agent handles multimodal image authenticity verification. Requires `llava:latest` via Ollama. |
| `liquid-nnn-detector/` | Liquid Neural Network continuous-time detector — research prototype, not production-ready. No training framework available. |
| `mod-router/` | Moderation router — functionality merged into `disinfo-orchestrator`. |
| `vla-visual/` | Vision-Language Agent for deepfake detection — superseded by `visual-analyst` and `visual-claim-verifier`. |

## For Implemented Agents

See `agents/` (the parent directory) for all operational pipeline agents.

## Roadmap

See `docs/roadmap.md` (if present) for the research roadmap and planned implementation timelines.
