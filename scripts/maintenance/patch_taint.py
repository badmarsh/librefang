import sys

with open("crates/librefang-runtime/src/tool_runner/taint.rs", "r") as f:
    code = f.read()

# Replace `check_taint_shell_exec(command: &str)`
code = code.replace(
    "pub(super) fn check_taint_shell_exec(command: &str) -> Option<String> {",
    "pub(super) fn check_taint_shell_exec(command: &TaintedValue<&str>) -> Option<String> {"
)
# Update uses of `command` inside `check_taint_shell_exec`
code = code.replace(
    "if let Some(reason) = crate::subprocess_sandbox::contains_shell_metacharacters(command) {",
    "if let Some(reason) = crate::subprocess_sandbox::contains_shell_metacharacters(command.value) {"
)
code = code.replace(
    "for pattern in &suspicious_patterns {\n        if command.contains(pattern) {",
    "for pattern in &suspicious_patterns {\n        if command.value.contains(pattern) {"
)
code = code.replace(
    "let mut labels = HashSet::new();",
    "let mut labels = command.labels.clone();"
)
code = code.replace(
    "let tainted = TaintedValue::new(command, labels, \"llm_tool_call\");",
    "let tainted = TaintedValue { value: command.value, labels, sources: command.sources.clone() };"
)
code = code.replace(
    "warn!(command = crate::str_utils::safe_truncate_str(command, 80), %violation, \"Shell taint check failed\");",
    "warn!(command = crate::str_utils::safe_truncate_str(command.value, 80), %violation, \"Shell taint check failed\");"
)

# Replace `check_taint_net_fetch(url: &str)`
code = code.replace(
    "pub(super) fn check_taint_net_fetch(url: &str) -> Option<String> {",
    "pub(super) fn check_taint_net_fetch(url: &TaintedValue<&str>) -> Option<String> {"
)
code = code.replace(
    "let url_lower = url.to_lowercase();",
    "let url_lower = url.value.to_lowercase();"
)
code = code.replace(
    "if let Ok(parsed) = url::Url::parse(url) {",
    "if let Ok(parsed) = url::Url::parse(url.value) {"
)
code = code.replace(
    "labels.insert(TaintLabel::Secret);\n        let tainted = TaintedValue::new(url, labels, \"llm_tool_call\");",
    "labels.insert(TaintLabel::Secret);\n        let tainted = TaintedValue { value: url.value, labels, sources: url.sources.clone() };"
)
code = code.replace(
    "warn!(url = crate::str_utils::safe_truncate_str(url, 80), %violation, \"Net fetch taint check failed\");",
    "warn!(url = crate::str_utils::safe_truncate_str(url.value, 80), %violation, \"Net fetch taint check failed\");"
)

# Replace `check_taint_outbound_header`
code = code.replace(
    "pub(super) fn check_taint_outbound_header(\n    name: &str,\n    value: &str,\n    sink: &TaintSink,\n) -> Option<String> {",
    "pub(super) fn check_taint_outbound_header(\n    name: &str,\n    value: &TaintedValue<&str>,\n    sink: &TaintSink,\n) -> Option<String> {"
)
code = code.replace(
    "let tainted = TaintedValue::new(value, labels, \"llm_tool_call\");",
    "let tainted = TaintedValue { value: value.value, labels, sources: value.sources.clone() };"
)
code = code.replace(
    "value_len = value.len(),",
    "value_len = value.value.len(),"
)

# Replace `check_taint_outbound_text`
code = code.replace(
    "pub(super) fn check_taint_outbound_text(payload: &str, sink: &TaintSink) -> Option<String> {",
    "pub(super) fn check_taint_outbound_text(payload: &TaintedValue<&str>, sink: &TaintSink) -> Option<String> {"
)
code = code.replace(
    "let lower = payload.to_lowercase();",
    "let lower = payload.value.to_lowercase();"
)
code = code.replace(
    "let trimmed = payload.trim();",
    "let trimmed = payload.value.trim();"
)
code = code.replace(
    "let tainted = TaintedValue::new(payload, labels, \"llm_tool_call\");",
    "let tainted = TaintedValue { value: payload.value, labels, sources: payload.sources.clone() };"
)
code = code.replace(
    "payload_len = payload.len(),",
    "payload_len = payload.value.len(),"
)

with open("crates/librefang-runtime/src/tool_runner/taint.rs", "w") as f:
    f.write(code)

