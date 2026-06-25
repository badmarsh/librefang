import sys

with open("crates/librefang-runtime/src/tool_runner/dispatch.rs", "r") as f:
    code = f.read()

# execute_tool signature
code = code.replace(
    "pub async fn execute_tool(\n    tool_use_id: &str,\n    tool_name: &str,\n    input: &serde_json::Value,",
    "pub async fn execute_tool(\n    tool_use_id: &str,\n    tool_name: &str,\n    input: &librefang_types::taint::TaintedValue<&serde_json::Value>,"
)

# the truncation check uses `input`
code = code.replace(
    "if input\n        .get(crate::drivers::openai::TRUNCATED_ARGS_KEY)",
    "if input.value\n        .get(crate::drivers::openai::TRUNCATED_ARGS_KEY)"
)
code = code.replace(
    "let error_msg = input[\"__error\"].as_str().unwrap_or(",
    "let error_msg = input.value[\"__error\"].as_str().unwrap_or("
)
code = code.replace(
    "&& input[\"command\"].as_str().is_some_and(|cmd| {",
    "&& input.value[\"command\"].as_str().is_some_and(|cmd| {"
)
code = code.replace(
    "pub async fn execute_tool_raw(\n    tool_use_id: &str,\n    tool_name: &str,\n    input: &serde_json::Value,",
    "pub async fn execute_tool_raw(\n    tool_use_id: &str,\n    tool_name: &str,\n    input: &librefang_types::taint::TaintedValue<&serde_json::Value>,"
)

# And now, all tool args extractions inside `execute_tool_raw` use `input.value` instead of `input`
# But wait, we want to construct TaintedValue<&str> for the taint checks!
# For shell_exec:
# let command = input.get("command").and_then(|v| v.as_str()).ok_or(...)?;
# let tainted_command = input.clone().map(|_| command); // Wait, this creates TaintedValue<&str>
# check_taint_shell_exec(&tainted_command)

code = code.replace(
    """                let command = input
                    .get("command")
                    .and_then(|v| v.as_str())
                    .ok_or_else(|| {
                        ToolError::bad_request("shell_exec requires a 'command' string")
                    })?;

                if let Some(violation) = check_taint_shell_exec(command) {""",
    """                let command = input.value
                    .get("command")
                    .and_then(|v| v.as_str())
                    .ok_or_else(|| {
                        ToolError::bad_request("shell_exec requires a 'command' string")
                    })?;
                let tainted_command = input.clone().map(|_| command);

                if let Some(violation) = check_taint_shell_exec(&tainted_command) {
                    if let Some(k) = ctx.kernel {
                        k.audit_log().record(
                            ctx.caller_agent_id.unwrap_or("system"),
                            librefang_runtime_audit::AuditAction::TaintSinkBlocked,
                            format!("tool=shell_exec violation={violation}"),
                            "denied",
                        );
                    }"""
)

# For net_fetch:
code = code.replace(
    """                let url = input
                    .get("url")
                    .and_then(|v| v.as_str())
                    .ok_or_else(|| ToolError::bad_request("net_fetch requires a 'url' string"))?;

                if let Some(violation) = check_taint_net_fetch(url) {""",
    """                let url = input.value
                    .get("url")
                    .and_then(|v| v.as_str())
                    .ok_or_else(|| ToolError::bad_request("net_fetch requires a 'url' string"))?;
                let tainted_url = input.clone().map(|_| url);

                if let Some(violation) = check_taint_net_fetch(&tainted_url) {
                    if let Some(k) = ctx.kernel {
                        k.audit_log().record(
                            ctx.caller_agent_id.unwrap_or("system"),
                            librefang_runtime_audit::AuditAction::TaintSinkBlocked,
                            format!("tool=net_fetch violation={violation}"),
                            "denied",
                        );
                    }"""
)
code = code.replace(
    """                    let body_text = body.as_str().unwrap_or_default();
                    if let Some(violation) =
                        check_taint_outbound_text(body_text, &TaintSink::net_fetch())
                    {""",
    """                    let body_text = body.as_str().unwrap_or_default();
                    let tainted_body = input.clone().map(|_| body_text);
                    if let Some(violation) =
                        check_taint_outbound_text(&tainted_body, &TaintSink::net_fetch())
                    {
                        if let Some(k) = ctx.kernel {
                            k.audit_log().record(
                                ctx.caller_agent_id.unwrap_or("system"),
                                librefang_runtime_audit::AuditAction::TaintSinkBlocked,
                                format!("tool=net_fetch violation={violation}"),
                                "denied",
                            );
                        }"""
)

# ... Wait, I should just use regex to replace all `.get(` on `input` to `input.value.get(`
code = code.replace("input.get(", "input.value.get(")

# What about check_taint_outbound_header?
code = code.replace(
    """                            if let Some(violation) =
                                check_taint_outbound_header(name, vs, &TaintSink::net_fetch())
                            {""",
    """                            let tainted_vs = input.clone().map(|_| vs);
                            if let Some(violation) =
                                check_taint_outbound_header(name, &tainted_vs, &TaintSink::net_fetch())
                            {
                                if let Some(k) = ctx.kernel {
                                    k.audit_log().record(
                                        ctx.caller_agent_id.unwrap_or("system"),
                                        librefang_runtime_audit::AuditAction::TaintSinkBlocked,
                                        format!("tool=net_fetch violation={violation}"),
                                        "denied",
                                    );
                                }"""
)

with open("crates/librefang-runtime/src/tool_runner/dispatch.rs", "w") as f:
    f.write(code)

