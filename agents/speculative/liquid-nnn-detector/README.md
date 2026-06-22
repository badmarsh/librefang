# Liquid Neural Network Detector [SPECULATIVE / UNIMPLEMENTED]

> [!WARNING]
> This agent is quarantined under `agents/speculative/` as a research-only component. It is NOT implemented in the production pipeline and is not active.

## Speculative Overview

This agent is designed for continuous-time threat detection using Liquid Neural Networks (LNNs), which process time-series data without fixed temporal windows. Unlike the current 2h/12h/72h multi-window CIB detector, an LNN-based agent would detect coordination signatures continuously across arbitrary time horizons.

## Aspirational Citation

- Ha, D., & Schmidhuber, J. (2021). *Recurrent Neural Networks for Control*.
  Nature Machine Intelligence. arXiv:2006.04439
- **Note**: LNNs (Liquid Time-Constant Networks, Hasani et al. 2021) are the
  technical basis for continuous-time disinformation pattern detection. Hardware
  and software requirements for real-time LNN inference exceed the current runtime
  environment. This agent would supersede the current multi-window CIB detector
  (Improvement 16) in Wave 5.
