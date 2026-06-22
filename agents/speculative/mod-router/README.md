# Mixture-of-Depths Router [SPECULATIVE / UNIMPLEMENTED]

> [!WARNING]
> This agent is quarantined under `agents/speculative/` as a research-only component. It is NOT implemented in the production pipeline and is not active.

## Speculative Overview

This agent is designed for dynamic compute allocation across the pipeline using Mixture-of-Depths (MoD) routing. Rather than running every claim through all 5 ensemble agents at full depth, MoD would dynamically route easy claims to shallow (cheap) agent paths and hard claims to deep (expensive) paths — potentially reducing inference cost by 30–50% for simple cases.

## Aspirational Citation

- Raposo, D., et al. (2024). *Mixture-of-Depths: Dynamically Allocating Compute
  in Transformer Models*. arXiv:2404.02258
- **Note**: MoD routing requires integration at the transformer layer level within
  each agent model, which is not supported by the current builtin:chat module
  architecture. This agent would complement (not replace) the existing
  instance-hardness routing (Improvement 13) in Wave 5.
