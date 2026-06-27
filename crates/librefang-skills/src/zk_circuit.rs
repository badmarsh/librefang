/// Mock Zero-Knowledge Circuit for CIB Score Attestation
/// Based on the Halo2 crate methodology (Wave 6-3, Gap 6).
pub struct CIBAttestationCircuit {
    pub score: f64,
    pub threshold: f64,
}

impl CIBAttestationCircuit {
    pub fn new(score: f64, threshold: f64) -> Self {
        Self { score, threshold }
    }

    /// Prove that `score` >= `threshold` without revealing the exact score.
    pub fn verify_proof(&self) -> bool {
        self.score >= self.threshold
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zk_attestation_pass() {
        let circuit = CIBAttestationCircuit::new(0.85, 0.75);
        assert!(
            circuit.verify_proof(),
            "Proof should be valid when score >= threshold"
        );
    }

    #[test]
    fn test_zk_attestation_fail() {
        let circuit = CIBAttestationCircuit::new(0.60, 0.75);
        assert!(
            !circuit.verify_proof(),
            "Proof should fail when score < threshold"
        );
    }

    #[test]
    fn test_zk_attestation_edge_case() {
        let circuit = CIBAttestationCircuit::new(0.75, 0.75);
        assert!(
            circuit.verify_proof(),
            "Proof should pass when score == threshold"
        );
    }
}
