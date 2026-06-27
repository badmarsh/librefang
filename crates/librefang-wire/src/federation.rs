use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;
use tokio::time::{interval, Duration};

/// Implementation of Federated Averaging (FedAvg) over OFP.
/// Reference: McMahan, H. B., et al. (2017). arXiv:1602.05629.
#[derive(Clone)]
pub struct FedAvgAggregator {
    pub round: u32,
    pub global_weights: HashMap<String, f64>,
}

pub struct FederationServer {
    pub aggregator: Arc<Mutex<FedAvgAggregator>>,
    pub incoming_gradients: Arc<Mutex<Vec<HashMap<String, f64>>>>,
}

impl FedAvgAggregator {
    pub fn new(initial_weights: HashMap<String, f64>) -> Self {
        Self {
            round: 0,
            global_weights: initial_weights,
        }
    }

    /// Aggregate gradients from multiple nodes
    pub fn aggregate(&mut self, node_gradients: Vec<HashMap<String, f64>>) {
        if node_gradients.is_empty() {
            return;
        }

        let num_nodes = node_gradients.len() as f64;
        let mut sum_gradients: HashMap<String, f64> = HashMap::new();

        for gradients in node_gradients {
            for (key, val) in gradients {
                *sum_gradients.entry(key).or_insert(0.0) += val;
            }
        }

        for (key, sum_val) in sum_gradients {
            let avg_grad = sum_val / num_nodes;
            if let Some(weight) = self.global_weights.get_mut(&key) {
                *weight += avg_grad;
            }
        }
        self.round += 1;
    }
}

impl FederationServer {
    pub fn new(initial_weights: HashMap<String, f64>) -> Self {
        Self {
            aggregator: Arc::new(Mutex::new(FedAvgAggregator::new(initial_weights))),
            incoming_gradients: Arc::new(Mutex::new(Vec::new())),
        }
    }

    /// RPC Endpoint to receive gradients from peers
    pub async fn sync_gradients(&self, peer_id: &str, signature: &str, gradients: HashMap<String, f64>) -> Result<(), String> {
        // Cryptographic verification placeholder
        if signature.is_empty() || peer_id.is_empty() {
            return Err("Invalid signature".to_string());
        }
        let mut queue = self.incoming_gradients.lock().await;
        queue.push(gradients);
        Ok(())
    }

    /// Spawns a background task that aggregates gradients every 6 hours
    pub fn spawn_background_task(self: Arc<Self>) {
        tokio::spawn(async move {
            let mut ticker = interval(Duration::from_secs(6 * 3600)); // 6 hours
            loop {
                ticker.tick().await;
                let mut queue = self.incoming_gradients.lock().await;
                let batch = std::mem::take(&mut *queue);
                if !batch.is_empty() {
                    let mut agg = self.aggregator.lock().await;
                    agg.aggregate(batch);
                    // Write the new updated weights to config.toml or DB here in production
                }
            }
        });
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fedavg_aggregation() {
        let mut initial = HashMap::new();
        initial.insert("layer1.weight".to_string(), 0.5);
        initial.insert("layer2.weight".to_string(), 1.0);

        let mut aggregator = FedAvgAggregator::new(initial.clone());

        let mut node1 = HashMap::new();
        node1.insert("layer1.weight".to_string(), 0.1);
        node1.insert("layer2.weight".to_string(), -0.2);

        let mut node2 = HashMap::new();
        node2.insert("layer1.weight".to_string(), 0.3);
        node2.insert("layer2.weight".to_string(), 0.0);

        aggregator.aggregate(vec![node1, node2]);

        assert_eq!(aggregator.round, 1);

        let w1 = aggregator.global_weights.get("layer1.weight").unwrap();
        // 0.5 + ((0.1 + 0.3) / 2) = 0.5 + 0.2 = 0.7
        assert!((*w1 - 0.7).abs() < f64::EPSILON);

        let w2 = aggregator.global_weights.get("layer2.weight").unwrap();
        // 1.0 + ((-0.2 + 0.0) / 2) = 1.0 - 0.1 = 0.9
        assert!((*w2 - 0.9).abs() < f64::EPSILON);
    }

    #[test]
    fn test_fedavg_empty_nodes() {
        let mut initial = HashMap::new();
        initial.insert("l1".to_string(), 0.5);
        let mut aggregator = FedAvgAggregator::new(initial);
        aggregator.aggregate(vec![]);
        assert_eq!(aggregator.round, 0);
    }
}
