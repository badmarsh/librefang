# VLA Visual Agent [SPECULATIVE / UNIMPLEMENTED]

> [!WARNING]
> This agent is quarantined under `agents/speculative/` as a research-only component. It is NOT implemented in the production pipeline and is not active.

## Speculative Overview

This agent is designed for autonomous visual forensics using Vision-Language-Action (VLA) models. Unlike the current visual-analyst (which uses VLMs for analysis only), a VLA agent would autonomously plan and execute multi-step visual investigation workflows — for example, reverse-image searching, cross-referencing geolocation metadata, and generating factcheck overlays without per-step human prompting.

## Citation Note

- Grounded in VLM literature (LLaVA, GPT-4V, Gemini Vision) — no single
  production-ready canonical citation for VLA applied to disinformation forensics.
- Related work:
  - Chandra, N., et al. (2025). *Deepfake-Eval-2024*. arXiv:2503.02857
  - *Multi-modal Deepfake Detection survey*. arXiv:2406.06965
  - *Passive Deepfake Detection survey*. arXiv:2411.17911
- VLA in the robotics sense (embodied action execution) is aspirational for
  this context; the term is used to describe the autonomous multi-step planning
  capability rather than physical embodiment.
