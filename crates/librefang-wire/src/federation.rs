use std::collections::HashMap;

/// Implementation of Federated Averaging (FedAvg) over OFP.
/// Reference: McMahan, H. B., et al. (2017). arXiv:1602.05629.
pub struct FedAvgAggregator {
    pub round: u32,
    pub global_weights: HashMap<String, f64>,
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