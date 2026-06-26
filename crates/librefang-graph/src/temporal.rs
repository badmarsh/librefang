use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use crate::graph::ActorGraph;
use petgraph::visit::EdgeRef;

#[derive(Debug, Serialize, Deserialize, PartialEq)]
pub enum TemporalEvent {
    NewEdge { source: String, target: String },
    CommunityMerge { comm_a: usize, comm_b: usize },
    ActorSurge { actor: String, current_pr: f64, mean_pr: f64 },
    BridgeEmergence { actor: String, betweenness: f64 },
}

#[derive(Debug, Serialize, Deserialize)]
pub struct GraphDelta {
    pub events: Vec<TemporalEvent>,
}

pub struct HistoricalGraphData {
    pub edges: Vec<(String, String)>,
    pub pagerank: HashMap<String, f64>,
    pub betweenness: HashMap<String, f64>,
}

/// Detects temporal events given current graph and historical graph summaries
/// 
/// Note: Rossi et al. (2020) TGN is already implemented in cib-detector.
/// This reads its output + historical KG events to emit deltas.
pub fn detect_temporal_events(
    current: &ActorGraph,
    current_pr: &HashMap<String, f64>,
    current_betweenness: &HashMap<String, f64>,
    history: &[HistoricalGraphData]
) -> GraphDelta {
    let mut events = Vec::new();

    // Collect historical edges
    let mut historical_edges = std::collections::HashSet::new();
    for h in history {
        for (u, v) in &h.edges {
            historical_edges.insert((u.clone(), v.clone()));
        }
    }

    // Detect NEW_EDGE
    for edge in current.graph.edge_references() {
        let u_name = current.graph.node_weight(edge.source()).unwrap().clone();
        let v_name = current.graph.node_weight(edge.target()).unwrap().clone();
        if !historical_edges.contains(&(u_name.clone(), v_name.clone())) {
            events.push(TemporalEvent::NewEdge {
                source: u_name,
                target: v_name,
            });
        }
    }

    // Detect ACTOR_SURGE (simplified std-dev)
    for (actor, &pr) in current_pr {
        let mut sum = 0.0;
        let mut count = 0;
        let mut vals = Vec::new();
        for h in history {
            if let Some(&hist_pr) = h.pagerank.get(actor) {
                sum += hist_pr;
                vals.push(hist_pr);
                count += 1;
            }
        }

        if count > 0 {
            let mean = sum / (count as f64);
            let mut variance = 0.0;
            for v in &vals {
                variance += (v - mean) * (v - mean);
            }
            let std_dev = (variance / (count as f64)).sqrt();
            let threshold = if std_dev > 0.0 { std_dev * 2.0 } else { mean * 0.5 }; // fallback if std_dev is 0

            if pr > mean + threshold {
                events.push(TemporalEvent::ActorSurge {
                    actor: actor.clone(),
                    current_pr: pr,
                    mean_pr: mean,
                });
            }
        }
    }

    // Detect BRIDGE_EMERGENCE
    for (actor, &bc) in current_betweenness {
        if bc > 0.5 {
            // Check if peripheral in ALL histories
            let mut was_peripheral = true;
            for h in history {
                if let Some(&hist_bc) = h.betweenness.get(actor) {
                    if hist_bc > 0.1 { // heuristic threshold for "not peripheral"
                        was_peripheral = false;
                        break;
                    }
                }
            }
            if was_peripheral && !history.is_empty() {
                events.push(TemporalEvent::BridgeEmergence {
                    actor: actor.clone(),
                    betweenness: bc,
                });
            }
        }
    }

    GraphDelta { events }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_detect_temporal_events() {
        let mut current = ActorGraph::new();
        current.add_amplification_edge("A", "B", 1.0, 1.0, 0.0, 1);
        
        let mut current_pr = HashMap::new();
        current_pr.insert("A".to_string(), 0.8);
        current_pr.insert("B".to_string(), 0.1);
        
        let mut current_bc = HashMap::new();
        current_bc.insert("A".to_string(), 0.6);
        current_bc.insert("B".to_string(), 0.0);

        let mut h1 = HistoricalGraphData {
            edges: vec![("C".to_string(), "D".to_string())],
            pagerank: HashMap::new(),
            betweenness: HashMap::new(),
        };
        h1.pagerank.insert("A".to_string(), 0.1);
        h1.betweenness.insert("A".to_string(), 0.0);
        
        let mut h2 = HistoricalGraphData {
            edges: vec![],
            pagerank: HashMap::new(),
            betweenness: HashMap::new(),
        };
        h2.pagerank.insert("A".to_string(), 0.1);
        h2.betweenness.insert("A".to_string(), 0.0);

        let delta = detect_temporal_events(&current, &current_pr, &current_bc, &[h1, h2]);
        
        assert!(delta.events.contains(&TemporalEvent::NewEdge { source: "A".to_string(), target: "B".to_string() }));
        assert!(delta.events.iter().any(|e| matches!(e, TemporalEvent::ActorSurge { actor, .. } if actor == "A")));
        assert!(delta.events.iter().any(|e| matches!(e, TemporalEvent::BridgeEmergence { actor, .. } if actor == "A")));
    }
}
