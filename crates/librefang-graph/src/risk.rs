use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum ActorClass {
    ApexNode,
    HubNode,
    BridgeNode,
    Peripheral,
}

pub fn actor_risk_score(
    pagerank_norm: f64,
    hits_auth_norm: f64,
    betweenness_norm: f64,
    credibility_score: f64,
) -> f64 {
    0.35 * pagerank_norm +
    0.25 * hits_auth_norm +
    0.25 * betweenness_norm +
    0.15 * (1.0 - credibility_score.clamp(0.0, 1.0))
}

pub fn classify_actor(risk_score: f64) -> ActorClass {
    if risk_score >= 0.75 {
        ActorClass::ApexNode
    } else if risk_score >= 0.50 {
        ActorClass::HubNode
    } else if risk_score >= 0.30 {
        ActorClass::BridgeNode
    } else {
        ActorClass::Peripheral
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_actor_risk_score_classification() {
        let score_apex = actor_risk_score(1.0, 1.0, 1.0, 0.0);
        assert_eq!(classify_actor(score_apex), ActorClass::ApexNode);
        
        let score_hub = actor_risk_score(0.5, 0.5, 0.5, 0.5); // 0.175 + 0.125 + 0.125 + 0.075 = 0.50
        assert_eq!(classify_actor(score_hub), ActorClass::HubNode);
        
        let score_bridge = actor_risk_score(0.2, 0.2, 0.8, 0.8); // 0.07 + 0.05 + 0.2 + 0.03 = 0.35
        assert_eq!(classify_actor(score_bridge), ActorClass::BridgeNode);
        
        let score_peripheral = actor_risk_score(0.1, 0.1, 0.1, 0.9);
        assert_eq!(classify_actor(score_peripheral), ActorClass::Peripheral);
    }
}
