# Dezolator Workflow Migration & Best Practices

This document outlines the analysis of the Dezolator pipeline and proposes a set of best practices for using LibreFang Workflows. 

## User Review Required

Please review the analysis and best practices below. Let me know if you would like me to formally formalize this into a documentation file (e.g., `docs/workflows_best_practices.md`) or if you would like me to begin migrating specific parts of the `disinfo-pipeline.toml` into native LibreFang Workflows.

## Open Questions

1. **Migration Scope:** Do you want to migrate the `disinfo-pipeline.toml` to the native `/api/workflows` system, or should we keep it as a custom pipeline and just use this research for future workflows?
2. **Blackboard vs. Explicit Passing:** Dezolator relies heavily on shared MCP memory context keys. Native Workflows use explicit variable passing (`output_var` -> `{{var_name}}`). Are we open to refactoring the agents' prompts to accept explicit inputs, or should we extend Workflows to support implicit blackboard context?

## Proposed Changes

If approved, I will create a permanent documentation artifact `docs/workflows_best_practices.md` containing the following research and guidelines:

---

### 1. Analysis of Dezolator Pipeline

The **Dezolator** project is a complex Disinformation Detection Pipeline implementing advanced theoretical principles (arXiv:2508.10143).
**Core Characteristics:**
- **Blackboard Architecture:** Agents communicate implicitly via shared MCP context keys (`memory_store`/`memory_recall`).
- **Ensemble Aggregation:** 7-agent parallel scoring with a central orchestrator (`disinfo-orchestrator`) that applies Bayesian and F2-score adaptive weights.
- **Dynamic Routing:** Instance-hardness routing (Mixture-of-Depths) and Adversarial Mini-Debates triggered by epistemic uncertainty.
- **Continuous Execution:** Sweeps via `watchdog` and `longitudinal_tracker`.
- **Human-in-the-Loop (HITL):** Writer agent gates Tier 3 verdicts due to legal sensitivities.

### 2. LibreFang Workflows Capabilities

The native LibreFang Workflow Engine (`crates/librefang-kernel/src/workflow.rs`) provides:
- **Explicit DAGs:** `depends_on` topological ordering.
- **Control Flow Nodes:** `Branch`, `Conditional`, `Loop`, `Transform`.
- **Native HITL:** `Operator` node natively pauses execution, alerts channels (Telegram/Email), and awaits human input (Approve/Reject/Edit) without blocking agent threads.
- **Dashboard Observability:** Visualizing steps, dry runs, and execution state via `/api/workflows`.

### 3. Migration Suitability (Manageability, Observability, Editability)

#### Workflows HIGHLY Suited for Migration:
- **HITL Publishing (Writer Stage):** Currently, the Tier 3 block is managed implicitly by the `writer` agent. Moving this to a `StepMode::Operator` node makes the legal review process explicit, observable in the dashboard, and directly actionable by human reviewers.
- **Deterministic Routing (e.g., Deep Verify vs. Fast Path):** Using `StepMode::Branch` to route borderline claims to the `inquisitor` agent based on the orchestrator's output would remove hardcoded routing from the orchestrator's prompt, making the pipeline highly editable.
- **Linear Pre-processing:** The Ingest -> Extract -> Decompose -> Align stages are perfect for sequential Workflow steps, increasing observability for where a claim fails.

#### Workflows POORLY Suited for Migration:
- **Continuous Background Sweeps:** The `watchdog` and `longitudinal_tracker` require persistent execution and rolling windows. Workflows are designed for finite, discrete runs. These should remain as persistent Agent `Hand` sessions.
- **Token-Level Dynamic Routing (MoD):** The `disinfo-orchestrator`'s token-level routing is too granular for macro workflow steps and should remain within the agent's logic.
- **Adaptive Weight State:** Bayesian and F2 weight updates require global state across runs, which is best handled by the existing MCP memory store rather than isolated workflow parameters.

### 4. Best Practices for LibreFang Workflows

1. **Use Workflows for Macro-Routing, Agents for Micro-Routing:** Define the high-level business logic (e.g., "If confidence < 0.5, request human review") in Workflow `Branch` and `Operator` nodes. Leave granular logic (e.g., "Which LLM layer to use for this sentence") to the agents.
2. **Prefer Explicit Data Passing:** Use `output_var` and Tera templates (`StepMode::Transform`) to pass data between stages. This makes the data lineage observable in the dashboard, compared to opaque MCP memory reads.
3. **Isolate HITL in Operator Nodes:** Never ask an agent to "wait for human input" or "block publication". Use the `Operator` step mode to leverage native timeouts, channel notifications, and dashboard integration.
4. **Reserve Pipelines for Blackboard Scenarios:** If an ensemble requires 10+ agents writing and reading dynamically from a shared knowledge graph without a strict sequence, a custom pipeline or multi-agent session is better than a rigid Workflow DAG.

---

## Verification Plan

- No code changes will be made during this planning phase.
- Upon approval, I will create the `docs/workflows_best_practices.md` document and commit it.
- If directed, I will author a pilot migration of the `writer` stage into a native LibreFang workflow.
