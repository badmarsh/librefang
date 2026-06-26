//! Decentralized P2P Topology Agent for sharing Temporal Knowledge Graphs.
//!
//! Provides the network mesh overlay for Wave 5.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeGraphNode {
    pub id: String,
    pub entity: String,
    pub timestamp: i64,
}

#[derive(Default)]
pub struct TopologyManager {
    nodes: Vec<KnowledgeGraphNode>,
}

impl TopologyManager {
    pub fn new() -> Self {
        Self { nodes: Vec::new() }
    }

    pub fn add_node(&mut self, node: KnowledgeGraphNode) {
        self.nodes.push(node);
    }
}
