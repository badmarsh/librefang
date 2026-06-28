//! Temporal Graph Networks (TGN) mock implementation
//!
//! Provides a software-fallback CPU stub to bypass missing GPU constraints
//! during local builds.

pub struct TgnModelStub;

impl TgnModelStub {
    pub fn new() -> Self {
        Self
    }
    
    pub fn predict(&self, _graph_data: &[u8]) -> Result<f32, &'static str> {
        // Return a mock risk score or inference output
        Ok(0.5)
    }
}
