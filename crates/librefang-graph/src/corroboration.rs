use crate::risk::ActorClass;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, PartialEq)]
pub enum CorroborationSignal {
    IndependentConvergence,
    PartialPresence,
    NotObserved,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct CorroborationResult {
    pub actor_id: String,
    pub signal: CorroborationSignal,
    pub notes: String,
}

/// Run Gerulata Corroboration Protocol
/// 
/// This does NOT constitute an independent attribution verdict.
/// It is cross-methodology signal only.
pub fn gerulata_corroboration_protocol(
    actor_id: &str,
    is_known_gerulata: bool,
    actor_class: Option<&ActorClass>,
) -> CorroborationResult {
    if !is_known_gerulata {
        return CorroborationResult {
            actor_id: actor_id.to_string(),
            signal: CorroborationSignal::NotObserved,
            notes: "Actor not found in Gerulata public reports.".to_string(),
        };
    }

    match actor_class {
        Some(ActorClass::ApexNode) | Some(ActorClass::HubNode) => {
            CorroborationResult {
                actor_id: actor_id.to_string(),
                signal: CorroborationSignal::IndependentConvergence,
                notes: format!("{:?} confirmed via structural centrality.", actor_class.unwrap()),
            }
        }
        Some(ActorClass::Peripheral) => {
            CorroborationResult {
                actor_id: actor_id.to_string(),
                signal: CorroborationSignal::PartialPresence,
                notes: "Presence without structural centrality.".to_string(),
            }
        }
        _ => {
            CorroborationResult {
                actor_id: actor_id.to_string(),
                signal: CorroborationSignal::NotObserved,
                notes: "Absent from this claim's propagation graph.".to_string(),
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gerulata_corroboration_independent_convergence() {
        let result = gerulata_corroboration_protocol("test_actor", true, Some(&ActorClass::ApexNode));
        assert_eq!(result.signal, CorroborationSignal::IndependentConvergence);
    }

    #[test]
    fn test_gerulata_corroboration_not_observed() {
        let result = gerulata_corroboration_protocol("test_actor", true, None);
        assert_eq!(result.signal, CorroborationSignal::NotObserved);
    }
    
    #[test]
    fn test_gerulata_corroboration_partial() {
        let result = gerulata_corroboration_protocol("test_actor", true, Some(&ActorClass::Peripheral));
        assert_eq!(result.signal, CorroborationSignal::PartialPresence);
    }
}
