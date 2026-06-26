use crate::graph::ActorGraph;
use petgraph::visit::{IntoNodeReferences, EdgeRef};
use petgraph::Direction;
use std::collections::HashMap;

/// Compute PageRank (α=0.85, max_iter=100)
/// Reference: Page, L. et al. (1999). "The PageRank citation ranking: Bringing order to the web."
pub fn pagerank(graph: &ActorGraph, alpha: f64, max_iter: usize) -> HashMap<String, f64> {
    let n = graph.graph.node_count();
    let mut ranks = HashMap::new();
    if n == 0 {
        return ranks;
    }

    let initial_rank = 1.0 / (n as f64);
    for node in graph.graph.node_references() {
        ranks.insert(node.1.clone(), initial_rank);
    }

    // pre-calculate out degrees
    let mut out_degrees = HashMap::new();
    for node in graph.graph.node_references() {
        let out_deg = graph.graph.edges_directed(node.0, Direction::Outgoing).count();
        out_degrees.insert(node.0, out_deg);
    }

    for _ in 0..max_iter {
        let mut new_ranks = HashMap::new();
        let mut sum_sink = 0.0;

        for node in graph.graph.node_references() {
            if out_degrees[&node.0] == 0 {
                sum_sink += ranks[node.1];
            }
        }

        for node in graph.graph.node_references() {
            let mut rank_sum = 0.0;
            for edge in graph.graph.edges_directed(node.0, Direction::Incoming) {
                let u = edge.source();
                let u_name = graph.graph.node_weight(u).unwrap();
                let out_deg = out_degrees[&u] as f64;
                if out_deg > 0.0 {
                    rank_sum += ranks[u_name] / out_deg;
                }
            }

            let new_rank = ((1.0 - alpha) / (n as f64)) + alpha * (rank_sum + sum_sink / (n as f64));
            new_ranks.insert(node.1.clone(), new_rank);
        }

        ranks = new_ranks;
    }

    ranks
}

pub struct HitsResult {
    pub authority: HashMap<String, f64>,
    pub hub: HashMap<String, f64>,
}

/// Compute HITS Authority + Hub scores
/// Reference: Kleinberg, J. (1999). "Authoritative sources in a hyperlinked environment."
pub fn hits(graph: &ActorGraph, tolerance: f64) -> HitsResult {
    let mut auth = HashMap::new();
    let mut hub = HashMap::new();

    if graph.graph.node_count() == 0 {
        return HitsResult { authority: auth, hub };
    }

    for node in graph.graph.node_references() {
        auth.insert(node.1.clone(), 1.0);
        hub.insert(node.1.clone(), 1.0);
    }

    loop {
        let mut new_auth = HashMap::new();
        let mut new_hub = HashMap::new();

        let mut auth_norm = 0.0;
        let mut hub_norm = 0.0;

        for node in graph.graph.node_references() {
            let mut a = 0.0;
            for edge in graph.graph.edges_directed(node.0, Direction::Incoming) {
                let u = edge.source();
                let u_name = graph.graph.node_weight(u).unwrap();
                a += hub[u_name];
            }
            new_auth.insert(node.1.clone(), a);
            auth_norm += a * a;

            let mut h = 0.0;
            for edge in graph.graph.edges_directed(node.0, Direction::Outgoing) {
                let v = edge.target();
                let v_name = graph.graph.node_weight(v).unwrap();
                h += auth[v_name];
            }
            new_hub.insert(node.1.clone(), h);
            hub_norm += h * h;
        }

        auth_norm = auth_norm.sqrt();
        hub_norm = hub_norm.sqrt();

        if auth_norm == 0.0 { auth_norm = 1.0; }
        if hub_norm == 0.0 { hub_norm = 1.0; }

        let mut max_delta = 0.0_f64;
        for node in graph.graph.node_references() {
            let a = new_auth[node.1] / auth_norm;
            let h = new_hub[node.1] / hub_norm;

            let delta_a = (a - auth[node.1]).abs();
            let delta_h = (h - hub[node.1]).abs();

            max_delta = max_delta.max(delta_a).max(delta_h);

            new_auth.insert(node.1.clone(), a);
            new_hub.insert(node.1.clone(), h);
        }

        auth = new_auth;
        hub = new_hub;

        if max_delta < tolerance {
            break;
        }
    }

    HitsResult { authority: auth, hub }
}

/// Compute Betweenness centrality
/// Reference: Brandes, U. (2001). "A faster algorithm for betweenness centrality."
pub fn betweenness_top_k(graph: &ActorGraph, top_k: usize) -> HashMap<String, f64> {
    // simplified exact Brandes algorithm
    let mut cb = HashMap::new();
    
    for node in graph.graph.node_references() {
        cb.insert(node.0, 0.0);
    }
    
    for s in graph.graph.node_references() {
        let mut stack = Vec::new();
        let mut paths = HashMap::new();
        let mut sigma = HashMap::new();
        let mut dist = HashMap::new();
        
        for v in graph.graph.node_references() {
            paths.insert(v.0, Vec::new());
            sigma.insert(v.0, 0.0);
            dist.insert(v.0, -1);
        }
        
        sigma.insert(s.0, 1.0);
        dist.insert(s.0, 0);
        
        let mut queue = std::collections::VecDeque::new();
        queue.push_back(s.0);
        
        while let Some(v) = queue.pop_front() {
            stack.push(v);
            let dv = dist[&v];
            
            for edge in graph.graph.edges_directed(v, Direction::Outgoing) {
                let w = edge.target();
                
                if dist[&w] < 0 {
                    queue.push_back(w);
                    dist.insert(w, dv + 1);
                }
                
                if dist[&w] == dv + 1 {
                    let sig_w = sigma[&w] + sigma[&v];
                    sigma.insert(w, sig_w);
                    paths.get_mut(&w).unwrap().push(v);
                }
            }
        }
        
        let mut delta = HashMap::new();
        for v in graph.graph.node_references() {
            delta.insert(v.0, 0.0);
        }
        
        while let Some(w) = stack.pop() {
            for &v in &paths[&w] {
                let d = (sigma[&v] / sigma[&w]) * (1.0 + delta[&w]);
                *delta.get_mut(&v).unwrap() += d;
            }
            if w != s.0 {
                *cb.get_mut(&w).unwrap() += delta[&w];
            }
        }
    }
    
    let mut results: Vec<(String, f64)> = cb.into_iter()
        .map(|(idx, score)| (graph.graph.node_weight(idx).unwrap().clone(), score))
        .collect();
        
    results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
    results.truncate(top_k);
    
    results.into_iter().collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::graph::ActorGraph;

    #[test]
    fn test_pagerank_convergence() {
        let mut g = ActorGraph::new();
        g.add_amplification_edge("A", "B", 1.0, 1.0, 0.0, 1);
        g.add_amplification_edge("B", "C", 1.0, 1.0, 0.0, 1);
        g.add_amplification_edge("C", "A", 1.0, 1.0, 0.0, 1);
        g.add_amplification_edge("D", "C", 1.0, 1.0, 0.0, 1);
        
        let pr = pagerank(&g, 0.85, 100);
        assert!(pr.contains_key("C"));
        assert!(pr["C"] > pr["D"]);
    }

    #[test]
    fn test_hits_convergence() {
        let mut g = ActorGraph::new();
        // Hub-and-spoke
        g.add_amplification_edge("Hub", "Auth1", 1.0, 1.0, 0.0, 1);
        g.add_amplification_edge("Hub", "Auth2", 1.0, 1.0, 0.0, 1);
        g.add_amplification_edge("Hub", "Auth3", 1.0, 1.0, 0.0, 1);
        
        let h = hits(&g, 1e-6);
        assert!(h.hub["Hub"] > h.hub["Auth1"]);
        assert!(h.authority["Auth1"] > h.authority["Hub"]);
    }
}
