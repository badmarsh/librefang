use petgraph::graph::{DiGraph, NodeIndex};
use std::collections::HashMap;

/// Directed graph where nodes are actors and edges are amplification events.
pub struct ActorGraph {
    pub graph: DiGraph<String, EdgeData>,
    pub node_indices: HashMap<String, NodeIndex>,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct EdgeData {
    pub temporal_delta: f64,
    pub semantic_sim: f64,
    pub credibility_diff: f64,
    pub co_occurrence: f64,
    pub weight: f64,
}

impl ActorGraph {
    pub fn new() -> Self {
        Self {
            graph: DiGraph::new(),
            node_indices: HashMap::new(),
        }
    }

    pub fn get_or_add_node(&mut self, actor_id: &str) -> NodeIndex {
        if let Some(&idx) = self.node_indices.get(actor_id) {
            idx
        } else {
            let idx = self.graph.add_node(actor_id.to_string());
            self.node_indices.insert(actor_id.to_string(), idx);
            idx
        }
    }

    /// Adds an edge and computes its weight according to the pipeline formula.
    ///
    /// Reference: Hamilton, W., Ying, R., Leskovec, J. (2017). "Inductive Representation
    /// Learning on Large Graphs (GraphSAGE)." NeurIPS 2017. arXiv:1706.02216.
    /// (Future upgrade path for edge embedding)
    pub fn add_amplification_edge(
        &mut self,
        source: &str,
        target: &str,
        temporal_delta_seconds: f64,
        semantic_sim: f64,
        credibility_diff: f64,
        co_occurrence: u32,
    ) {
        let u = self.get_or_add_node(source);
        let v = self.get_or_add_node(target);

        // Normalize temporal delta (e.g., convert to hours to avoid division by huge numbers)
        // Adding 1.0 to avoid division by zero.
        let temporal_delta_normalized = temporal_delta_seconds.max(0.0) / 3600.0;

        let weight = (1.0 / (1.0 + temporal_delta_normalized))
            * semantic_sim.max(0.0)
            * (1.0 - credibility_diff.abs().clamp(0.0, 1.0))
            * (1.0 + co_occurrence as f64).ln();

        let edge_data = EdgeData {
            temporal_delta: temporal_delta_seconds,
            semantic_sim,
            credibility_diff,
            co_occurrence: co_occurrence as f64,
            weight,
        };

        self.graph.add_edge(u, v, edge_data);
    }
}

impl Default for ActorGraph {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_edge_weight_formula() {
        let mut g = ActorGraph::new();
        g.add_amplification_edge("A", "B", 3600.0, 0.8, 0.1, 10);
        
        let edge_idx = g.graph.edge_indices().next().unwrap();
        let edge = g.graph.edge_weight(edge_idx).unwrap();
        
        // temporal_delta_normalized = 3600.0 / 3600.0 = 1.0
        // weight = (1 / (1 + 1)) * 0.8 * (1 - 0.1) * ln(11) 
        // weight = 0.5 * 0.8 * 0.9 * 2.39789...
        // weight = 0.36 * 2.39789... ≈ 0.863
        
        let expected = 0.5 * 0.8 * 0.9 * 11.0_f64.ln();
        assert!((edge.weight - expected).abs() < 1e-6);
    }
}
