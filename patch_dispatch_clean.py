import sys

with open("crates/librefang-runtime/src/tool_runner/dispatch.rs", "r") as f:
    code = f.read()

# For shell_exec
code = code.replace(
    """                if let Some(violation) = check_taint_shell_exec(command) {""",
    """                let tainted_command = librefang_types::taint::TaintedValue::new(
                    command,
                    { let mut s = std::collections::HashSet::new(); s.insert(librefang_types::taint::TaintLabel::UntrustedAgent); s },
                    "llm_tool_call"
                );
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

# For net_fetch
code = code.replace(
    """                if let Some(violation) = check_taint_net_fetch(url) {""",
    """                let tainted_url = librefang_types::taint::TaintedValue::new(
                    url,
                    { let mut s = std::collections::HashSet::new(); s.insert(librefang_types::taint::TaintLabel::UntrustedAgent); s },
                    "llm_tool_call"
                );
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
    """                    if let Some(violation) =
                        check_taint_outbound_text(body_text, &TaintSink::net_fetch())
                    {""",
    """                    let tainted_body = librefang_types::taint::TaintedValue::new(
                        body_text,
                        { let mut s = std::collections::HashSet::new(); s.insert(librefang_types::taint::TaintLabel::UntrustedAgent); s },
                        "llm_tool_call"
                    );
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

code = code.replace(
    """                            if let Some(violation) =
                                check_taint_outbound_header(name, vs, &TaintSink::net_fetch())
                            {""",
    """                            let tainted_vs = librefang_types::taint::TaintedValue::new(
                                vs,
                                { let mut s = std::collections::HashSet::new(); s.insert(librefang_types::taint::TaintLabel::UntrustedAgent); s },
                                "llm_tool_call"
                            );
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

