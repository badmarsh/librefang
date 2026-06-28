# LibreFang Workflows: Best Practices & Dezolator Migration Analysis

This document establishes best practices for utilizing LibreFang's native Workflow Engine (`crates/librefang-kernel/src/workflow.rs`), derived from a rigorous analysis of the **Mediálny Dezolator** disinformation detection pipeline.

## 1. Context: Dezolator Pipeline Architecture

The Dezolator project (v4.0.0, implementing arXiv:2508.10143) is an advanced multi-agent pipeline orchestrating 9 primary agents:
*   **Blackboard Pattern:** Agents communicate implicitly via shared MCP memory (`memory_store` / `memory_recall`).
*   **Parallel Execution:** 7 independent scoring agents (`ml-classifier`, `wiki-checker`, etc.) run concurrently.
*   **Dynamic Orchestration:** A central `disinfo-orchestrator` routes claims based on "instance hardness" (Mixture-of-Depths), triggers adversarial debates (when epistemic uncertainty is high), and applies adaptive Bayesian/F2-score weights.
*   **Continuous Sweeps:** Agents like `watchdog` and `longitudinal_tracker` run continuous loops or scheduled intervals.

## 2. LibreFang Workflows Engine

The native LibreFang Workflow Engine (`/api/workflows`) uses declarative JSON/TOML execution graphs:
*   **DAG Execution:** `depends_on` topological constraints.
*   **Control Flow:** Explicit `Branch`, `Conditional`, `Transform`, and `Loop` node types.
*   **Parallelism:** `FanOut` and `Collect` modes.
*   **Human-In-The-Loop (HITL):** First-class `Operator`, `Approval`, `Wait`, and `Gate` nodes capable of pausing runs indefinitely and sending notifications over multiple channels (Telegram, Email, etc.).
*   **State Passing:** Explicit templating (e.g., `{{input}}`, `{{var_name}}`) rather than implicit memory reads.

## 3. Migration Suitability Analysis

When migrating existing implicit pipelines (like Dezolator) into native LibreFang Workflows, observe the following fitness criteria:

### Highly Suited for Workflows

1.  **HITL & Compliance Gates (e.g., Dezolator's `writer` stage):**
    *   *Analysis:* Currently, Dezolator relies on the `writer` agent to "hard block" Tier 3 (high risk) verdicts.
    *   *Workflow Advantage:* Replacing this implicit agent logic with a native `StepMode::Operator` node ensures the workflow explicitly pauses. It integrates directly with the LibreFang dashboard (`/api/workflows/operator/pending`) and issues webhook/Telegram alerts without burning LLM tokens in a polling loop.
2.  **Macro-Level Deterministic Routing:**
    *   *Analysis:* Sending borderline claims to a "Deep Verify" path (`inquisitor` with 10 sources) instead of a "Fast Path".
    *   *Workflow Advantage:* Using `StepMode::Branch` makes the routing logic observable and editable in the dashboard UI, reducing prompt-engineering debt inside an orchestrator agent.
3.  **Linear Pre-Processing:**
    *   *Analysis:* Ingest -> Extract -> Decompose -> Align.
    *   *Workflow Advantage:* Sequential steps are highly observable. Failures map to specific, retry-able nodes.

### Poorly Suited for Workflows

1.  **Continuous / Unbounded Background Tasks:**
    *   *Analysis:* `watchdog` monitoring RSS feeds, or `longitudinal_tracker` 15-minute bursts.
    *   *Workflow Limitation:* Workflows are modeled as finite `WorkflowRun` instances. Infinite tasks should remain as persistent Agent `Hand` sessions (`session_mode = persistent`).
2.  **Micro-Routing / Token-Level Decisions (MoD):**
    *   *Analysis:* Mixture-of-Depths computing inside the `disinfo-orchestrator`.
    *   *Workflow Limitation:* Defining token-level routing as a DAG graph is unmanageable. Highly granular, algorithmic decisions should stay entirely within the agent's prompt or backend tool.
3.  **Complex Shared State (Blackboard pattern):**
    *   *Analysis:* 10+ agents reading/writing continuously to an adaptive knowledge graph without strict step boundaries.
    *   *Workflow Limitation:* Workflows enforce strict topological variable passing (`output_var`). A pure Blackboard architecture is better orchestrated via MCP and a standard `pipeline.toml` rather than a rigid workflow DAG.

## 4. Best Practices for Developing LibreFang Workflows

*   **Rule 1: Use Workflows for Macro-Routing, Agents for Micro-Routing.** Keep business logic ("if fake score > 0.5, require approval") in the Workflow. Keep semantic logic ("evaluate this text for fear-amplification") in the agent.
*   **Rule 2: Isolate HITL in Operator Nodes.** Do not ask LLM agents to "wait" or "pause for user input". Instead, output a structured status, and configure the next Workflow step as an `Operator` node to handle the human approval cycle.
*   **Rule 3: Prefer Explicit Data Passing.** When building Workflows, prefer `output_var` and `StepMode::Transform` Tera templates to pipe data. This grants full lineage observability on the LibreFang dashboard, making debugging significantly easier than tracking implicit state in a shared database.
*   **Rule 4: Leverage Branches over Conditionals for Complex Logic.** If a decision has more than 2 outcomes, use `StepMode::Branch` matching against JSON outputs rather than a series of brittle string-matching `Conditional` steps.