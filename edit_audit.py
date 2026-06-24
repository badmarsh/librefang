import sys

with open("crates/librefang-runtime-audit/src/lib.rs", "r") as f:
    code = f.read()

old_action_enum = """    A2aTrusted,
}"""
new_action_enum = """    A2aTrusted,
    /// A tainted value attempted to cross an execution boundary into a sink
    /// that blocks one or more of its labels.
    TaintSinkBlocked,
}"""
code = code.replace(old_action_enum, new_action_enum)

old_match = """                        "A2aTrusted" => AuditAction::A2aTrusted,
                        _ => AuditAction::ToolInvoke, // fallback"""
new_match = """                        "A2aTrusted" => AuditAction::A2aTrusted,
                        "TaintSinkBlocked" => AuditAction::TaintSinkBlocked,
                        _ => AuditAction::ToolInvoke, // fallback"""
code = code.replace(old_match, new_match)

# Wait, the match arm in `with_db` might not have A2aTrusted exactly as written above.
# Let's check what it actually has.
# The code I saw:
#                         "RetentionTrim" => AuditAction::RetentionTrim,
#                         _ => AuditAction::ToolInvoke, // fallback

old_match_actual = """                        "RetentionTrim" => AuditAction::RetentionTrim,
                        _ => AuditAction::ToolInvoke, // fallback"""
new_match_actual = """                        "RetentionTrim" => AuditAction::RetentionTrim,
                        "A2aDiscovered" => AuditAction::A2aDiscovered,
                        "A2aTrusted" => AuditAction::A2aTrusted,
                        "TaintSinkBlocked" => AuditAction::TaintSinkBlocked,
                        _ => AuditAction::ToolInvoke, // fallback"""
code = code.replace(old_match_actual, new_match_actual)

with open("crates/librefang-runtime-audit/src/lib.rs", "w") as f:
    f.write(code)
