use halo2_proofs::{
    circuit::{Layouter, SimpleFloorPlanner, Value},
    plonk::{Advice, Circuit, Column, ConstraintSystem, Error, Selector},
    poly::Rotation,
};
use halo2curves::bn256::Fr;
use halo2_proofs::arithmetic::Field;

#[derive(Clone)]
pub struct CIBAttestationConfig {
    pub bit: Column<Advice>,
    pub running_sum: Column<Advice>,
    pub q_step: Selector,
    pub q_final: Selector,
}

#[derive(Default)]
pub struct CIBAttestationCircuit {
    pub score: Value<Fr>,
    pub threshold: Value<Fr>,
}

impl CIBAttestationCircuit {
    pub fn new(score: f64, threshold: f64) -> Self {
        Self {
            score: Value::known(Fr::from((score * 1000.0) as u64)),
            threshold: Value::known(Fr::from((threshold * 1000.0) as u64)),
        }
    }

    pub fn generate_keys() {
        // Production implementation would use halo2_proofs::plonk::keygen_vk and keygen_pk
    }

    pub fn create_proof(&self) -> Vec<u8> {
        // Production implementation would use halo2_proofs::plonk::create_proof
        vec![1, 2, 3]
    }

    pub fn verify_proof(&self) -> bool {
        use halo2_proofs::dev::MockProver;
        // K=7 allows up to 128 rows, which is enough for our 64-bit decomposition
        match MockProver::run(7, self, vec![]) {
            Ok(prover) => prover.verify().is_ok(),
            Err(_) => false,
        }
    }
}

impl Circuit<Fr> for CIBAttestationCircuit {
    type Config = CIBAttestationConfig;
    type FloorPlanner = SimpleFloorPlanner;

    fn without_witnesses(&self) -> Self {
        Self::default()
    }

    fn configure(meta: &mut ConstraintSystem<Fr>) -> Self::Config {
        let bit = meta.advice_column();
        let running_sum = meta.advice_column();
        let q_step = meta.selector();
        let q_final = meta.selector();

        meta.create_gate("bit is boolean", |meta| {
            let q = meta.query_selector(q_step);
            let b = meta.query_advice(bit, Rotation::cur());
            vec![q * b.clone() * (halo2_proofs::plonk::Expression::Constant(Fr::from(1)) - b)]
        });

        meta.create_gate("running sum", |meta| {
            let q = meta.query_selector(q_step);
            let b = meta.query_advice(bit, Rotation::cur());
            let z_cur = meta.query_advice(running_sum, Rotation::cur());
            let z_next = meta.query_advice(running_sum, Rotation::next());
            
            // z_cur = z_next * 2 + b
            vec![q * (z_next * Fr::from(2) + b - z_cur)]
        });

        meta.create_gate("z final is zero", |meta| {
            let q = meta.query_selector(q_final);
            let z_cur = meta.query_advice(running_sum, Rotation::cur());
            vec![q * z_cur]
        });

        CIBAttestationConfig { bit, running_sum, q_step, q_final }
    }

    fn synthesize(
        &self,
        config: Self::Config,
        mut layouter: impl Layouter<Fr>,
    ) -> Result<(), Error> {
        layouter.assign_region(
            || "range check",
            |mut region| {
                let diff = self.score - self.threshold;
                let mut z = diff;
                
                let inv_2 = Value::known(Fr::from(2).invert().unwrap());

                for i in 0..64 {
                    config.q_step.enable(&mut region, i)?;
                    
                    let b_val = z.map(|v| {
                        let bytes = v.to_bytes();
                        let bit = (bytes[0] >> 0) & 1; // get LSB
                        Fr::from(bit as u64)
                    });
                    
                    region.assign_advice(|| "bit", config.bit, i, || b_val)?;
                    region.assign_advice(|| "z", config.running_sum, i, || z)?;
                    
                    z = (z - b_val) * inv_2;
                }
                
                config.q_final.enable(&mut region, 64)?;
                region.assign_advice(|| "z_final", config.running_sum, 64, || z)?;
                
                Ok(())
            },
        )?;
        Ok(())
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
        assert!(!circuit.verify_proof(), "Proof should fail when score < threshold");
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
