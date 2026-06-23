use serde::{Deserialize, Serialize};

/// A DPO/RLHF preference pair.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PreferencePair {
    /// The prompt presented to the model.
    pub prompt: String,
    /// The chosen (preferred) completion.
    pub chosen: String,
    /// The rejected completion.
    pub rejected: String,
}

/// A store for preference pairs.
#[async_trait::async_trait]
pub trait PreferenceStore: Send + Sync {
    /// Store a preference pair.
    async fn store_preference(&self, pair: PreferencePair) -> Result<(), crate::ExportError>;
}
