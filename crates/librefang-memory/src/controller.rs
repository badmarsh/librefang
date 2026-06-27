use std::sync::Arc;
use tokio::sync::Mutex;
use crate::temporal_kg::TemporalGraph;
use serde_json::Value;

pub struct MemoryController {
    pub kg: Arc<Mutex<TemporalGraph>>,
}

impl MemoryController {
    pub fn new(kg: Arc<Mutex<TemporalGraph>>) -> Self {
        Self { kg }
    }

    /// Letta/MemGPT pattern: centralised arbitration prevents conflicting KG writes.
    /// This handles the `memory.write.requested` events from all agents.
    pub async fn arbitrate_and_write(&self, agent_id: &str, operation: &str, data: Value) -> Result<(), String> {
        let kg = self.kg.lock().await;

        // Arbitration logic: only specific agents can write certain fields
        // e.g., 'archivist' has sole ownership of source credibility.
        if operation == "update_source_credibility" && agent_id != "archivist" {
            return Err("Permission denied: Only archivist can update source credibility".to_string());
        }

        // Apply mutation
        match operation {
            "node_upsert" => {
                if let Some(id) = data.get("id").and_then(|v| v.as_str()) {
                    let _ = kg.update_node_properties(id, data.clone());
                } else {
                    return Err("Missing node id".into());
                }
            }
            "edge_upsert" => {
                // Assuming data contains source_id, target_id, relation, new_decay
                if let (Some(s), Some(t), Some(r), Some(d)) = (
                    data.get("source_id").and_then(|v| v.as_str()),
                    data.get("target_id").and_then(|v| v.as_str()),
                    data.get("relation").and_then(|v| v.as_str()),
                    data.get("new_decay").and_then(|v| v.as_f64()),
                ) {
                    let _ = kg.update_edge_decay(s, t, r, d as f32);
                } else {
                    return Err("Missing edge parameters".into());
                }
            }
            _ => return Err("Unknown operation".into()),
        }

        Ok(())
    }
}
