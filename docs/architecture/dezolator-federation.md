# Federated Signal Sharing Architecture

**Status**: PLANNED (Wave 5)
**Reference**: McMahan, H. B., et al. (2017). *Communication-Efficient Learning of Deep Networks from Decentralized Data*. arXiv:1602.05629.

## 1. Context
Currently, `librefang-wire` transmits signals across the network, but the protocol is plaintext-by-design. Cross-network federation requires an overlay. To allow participating nodes (fact-checkers, external OSINT partners) to share intelligence on emerging disinformation campaigns without exposing proprietary datasets or violating privacy constraints, we will implement a Federated Learning architecture.

## 2. Methodology: Federated Averaging (FedAvg)
We will adopt the **FedAvg** algorithm for continuous model weight updates across the node network. 
1. **Local Training**: Each trusted node continues training their local `ml-classifier` and `cib-detector` instances on their private, locally-ingested data.
2. **Gradient Aggregation**: Instead of sharing the raw disinformation text or user graphs, nodes will transmit their computed model gradients to the central orchestrator node.
3. **Global Update**: The central node aggregates the gradients, applies them to the global model, and broadcasts the updated model weights back to the federation.

## 3. Integration Points
- Extends the `librefang-wire` OFP component.
- The `disinfo-orchestrator` will mediate the aggregation logic.
- Requires securing the transport layer (e.g., mTLS over WireGuard/Tailscale) before enabling.
