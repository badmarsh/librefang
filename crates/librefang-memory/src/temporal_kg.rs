//! Temporal Knowledge Graph (Wave 5 Memory Architecture)
//!
//! Implements a temporal KG structure inspired by Letta/Graphiti.
//! Edges in this graph carry temporal validity windows (`valid_from`, `valid_to`)
//! and time-decay functions, replacing the older flat KG approach.
//! This allows the `archivist` agent to track evolving disinformation narratives
//! and properly expire outdated claims.

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TemporalNode {
    pub id: String,
    pub label: String,
    pub properties: serde_json::Value,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TemporalEdge {
    pub source_id: String,
    pub target_id: String,
    pub relation: String,
    pub valid_from: DateTime<Utc>,
    pub valid_to: Option<DateTime<Utc>>,
    pub decay_rate: f32, // Rate at which relevance decays after valid_from
}

pub struct TemporalGraph {
    pub nodes: Vec<TemporalNode>,
    pub edges: Vec<TemporalEdge>,
}

impl TemporalGraph {
    pub fn new() -> Self {
        Self {
            nodes: Vec::new(),
            edges: Vec::new(),
        }
    }

    pub fn add_node(&mut self, node: TemporalNode) {
        self.nodes.push(node);
    }

    pub fn add_edge(&mut self, edge: TemporalEdge) {
        self.edges.push(edge);
    }

    /// Queries edges that are valid at the given timestamp.
    pub fn get_active_edges_at(&self, timestamp: DateTime<Utc>) -> Vec<&TemporalEdge> {
        self.edges
            .iter()
            .filter(|e| {
                e.valid_from <= timestamp
                    && e.valid_to.map_or(true, |end| timestamp <= end)
            })
            .collect()
    }
}
