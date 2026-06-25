//! Quantum Support Vector Machine (QSVM) mock implementation
//!
//! Provides a software-fallback CPU stub to bypass missing Google Willow
//! 105-qubit QPU constraints during local builds.

pub struct QsvmModelStub;

impl QsvmModelStub {
    pub fn new() -> Self {
        Self
    }
    
    pub fn predict(&self, _features: &[f32]) -> Result<i32, &'static str> {
        // Return a mock classification result
        Ok(1)
    }
}
