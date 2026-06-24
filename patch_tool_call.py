import sys

with open("crates/librefang-runtime/src/agent_loop/tool_call.rs", "r") as f:
    code = f.read()

code = code.replace(
    "&tool_call.input,",
    """&librefang_types::taint::TaintedValue::new(
                tool_call.input.clone(),
                {
                    let mut l = std::collections::HashSet::new();
                    l.insert(librefang_types::taint::TaintLabel::UntrustedAgent);
                    l
                },
                "llm_tool_call"
            ),"""
)

with open("crates/librefang-runtime/src/agent_loop/tool_call.rs", "w") as f:
    f.write(code)

