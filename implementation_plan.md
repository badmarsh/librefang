# Implement Missing QA Audit Tests

This plan addresses the missing integration and end-to-end tests identified in the recent LibreFang QA audit, alongside the required architectural changes for the Graph DB abstraction.

## User Review Required
No breaking changes or significant design shifts outside of the requested abstraction of the Neo4j graph storage. We will use the standard `MockKernelBuilder` for the integration tests.

## Open Questions
None at this time. The objectives are clear and well-scoped.

## Proposed Changes

### crates/librefang-runtime-mcp

#### [MODIFY] lib.rs
- Make `scan_mcp_arguments_for_taint_with_policy` visible by changing it to `pub fn scan_mcp_arguments_for_taint_with_policy`.

#### [NEW] tests/taint_integration.rs
- Create `test_external_network_taint_blocked_at_mcp_sink` to verify `ExternalNetwork` taint is blocked.
- Create `test_untrusted_agent_taint_blocked_at_mcp_sink` to verify `UntrustedAgent` taint is blocked.
- Create `test_mcp_scanner_rejects_external_network_shaped_argument` using a dummy IP/payload to directly call `scan_mcp_arguments_for_taint_with_policy`.

---

### crates/librefang-graph

#### [MODIFY] Cargo.toml
- Add `testcontainers = "0.15"` and `testcontainers-modules = { version = "0.3", features = ["neo4j"] }` to `[dev-dependencies]`.
- Add `async-trait = "0.1"` if not already present, though native `async fn` in traits is supported on Rust 1.75+.

#### [MODIFY] src/lib.rs
- Introduce `GraphStore` trait with `async fn add_actor(&self, actor: &Actor) -> Result<(), GraphError>`.
- Refactor `NetworkMapperGraph` to hold `Box<dyn GraphStore + Send + Sync>`.
- Implement `Neo4jGraphStore` mapping to the existing Neo4j implementation.
- Introduce a local `MockGraphStore` utilizing a `Mutex<Vec<Actor>>`.
- Add unit tests verifying `add_actor` using the mock.

#### [NEW] tests/neo4j_integration.rs
- Add `test_merge_is_idempotent_against_real_neo4j` behind the `#[cfg(feature = "integration")]` feature flag using `testcontainers`.

---

### crates/librefang-testing

#### [MODIFY] src/tests.rs
- Add `test_cib_detector_reads_claim_extractor_memory`.
- Spin up `MockKernelBuilder`.
- Spawn `claim_extractor` (write access: `claim_extractor.*`) and `cib_detector` (read access: `claim_extractor.*`, write access: `cib_detector.*`).
- Simulate memory writes by `claim_extractor`.
- Assert `cib_detector` successfully recalls `claim_extractor.claim_001`.
- Assert `cib_detector` receives an error when writing to `claim_extractor.*`.

---

### crates/librefang-kernel

#### [MODIFY] src/kernel/tests.rs
- Add `test_cron_session_mode_new_produces_unique_sessions_per_fire`.
- We will directly test the session generation logic used by the cron dispatcher, primarily `crate::cron::cron_fire_session_override` and verify that `session_mode = "new"` yields unique `SessionId`s per fire, avoiding context saturation.

## Verification Plan

### Automated Tests
We will verify the implementation by running:
- `cargo test -p librefang-runtime-mcp`
- `cargo test -p librefang-graph`
- `cargo test -p librefang-graph --features integration`
- `cargo test -p librefang-testing`
- `cargo test -p librefang-kernel`

### Manual Verification
The automated test suite provides comprehensive coverage for these changes.
