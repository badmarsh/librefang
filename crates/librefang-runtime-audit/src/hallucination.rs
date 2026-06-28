use serde::{Deserialize, Serialize};

/// Represents a multi-agent verification event for hallucination auditing.
/// This structure tracks the consensus or disagreement between multiple LLMs
/// acting as judges, mitigating the "single-LLM-as-judge" failure mode.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VerificationLog {
    pub task_id: String,
    pub original_claim: String,
    pub primary_agent_id: String,
    pub verifier_agent_ids: Vec<String>,
    pub consensus_reached: bool,
    pub confidence_score: f64,
    pub logic_gaps_identified: Vec<String>,
}

impl VerificationLog {
    pub fn new(
        task_id: impl Into<String>,
        original_claim: impl Into<String>,
        primary_agent_id: impl Into<String>,
    ) -> Self {
        Self {
            task_id: task_id.into(),
            original_claim: original_claim.into(),
            primary_agent_id: primary_agent_id.into(),
            verifier_agent_ids: Vec::new(),
            consensus_reached: false,
            confidence_score: 0.0,
            logic_gaps_identified: Vec::new(),
        }
    }

    pub fn add_verifier_result(
        &mut self,
        verifier_id: String,
        agreed: bool,
        logic_gaps: Vec<String>,
    ) {
        self.verifier_agent_ids.push(verifier_id);
        if !agreed {
            self.logic_gaps_identified.extend(logic_gaps);
        }

        // Simple consensus recalculation
        let total_verifiers = self.verifier_agent_ids.len();
        if total_verifiers > 0 {
            let disagreement_count = self.logic_gaps_identified.len();
            self.confidence_score =
                1.0 - (disagreement_count as f64 / total_verifiers as f64).min(1.0);
            self.consensus_reached = self.confidence_score > 0.6;
        }
    }
}
