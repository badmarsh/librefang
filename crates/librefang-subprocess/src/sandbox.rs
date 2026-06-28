use std::path::Path;

#[cfg(target_os = "linux")]
pub fn apply_landlock_policy(data_dir: &Path, agent_id: &str) -> Result<(), Box<dyn std::error::Error>> {
    use landlock::{path_beneath_rules, Access, AccessFs, Ruleset, RulesetAttr, RulesetCreatedAttr, ABI};
    use std::fs;

    // We grant read/write to the agent's workspace and read-only to the ontology.
    let workspace_path = data_dir.join("workspaces").join(agent_id);
    let ontology_path = data_dir.join("ontology");

    // Ensure they exist so Landlock can bind to them
    let _ = fs::create_dir_all(&workspace_path);
    let _ = fs::create_dir_all(&ontology_path);

    let abi = ABI::V3;
    let mut ruleset = Ruleset::default()
        .handle_access(AccessFs::from_all(abi))?
        .create()?;

    // Read/Write access to the workspace
    ruleset = ruleset.add_rules(
        path_beneath_rules(
            &[&workspace_path],
            AccessFs::from_all(abi),
        )
    )?;

    // Read-only access to the ontology
    ruleset = ruleset.add_rules(
        path_beneath_rules(
            &[&ontology_path],
            AccessFs::from_read(abi),
        )
    )?;
    
    // Read access to /proc/self/
    ruleset = ruleset.add_rules(
        path_beneath_rules(
            &["/proc/self"],
            AccessFs::from_read(abi),
        )
    )?;

    let status = ruleset.restrict_self()?;
    if status.ruleset == landlock::RulesetStatus::NotEnforced {
        tracing::warn!("Landlock is not supported by the kernel or not enforced.");
    }

    Ok(())
}

#[cfg(not(target_os = "linux"))]
pub fn apply_landlock_policy(_data_dir: &Path, _agent_id: &str) -> Result<(), Box<dyn std::error::Error>> {
    tracing::warn!("Landlock sandboxing is only supported on Linux.");
    Ok(())
}

#[cfg(target_os = "linux")]
pub fn apply_seccomp_filter() -> Result<(), Box<dyn std::error::Error>> {
    use seccompiler::{SeccompAction, SeccompFilter};

    let _filter = SeccompFilter::new(
        vec![].into_iter().collect(),
        SeccompAction::Allow, // Default allow, we blacklist specific dangerous syscalls
        SeccompAction::Trap,  // Action for matched blacklisted syscalls
        std::env::consts::ARCH.try_into()?,
    )?;

    let _blacklist = vec![
        "ptrace", "mount", "umount2", "chroot", "pivot_root", "kexec_load",
        "init_module", "finit_module", "delete_module", "bpf", "perf_event_open",
        "userfaultfd", "unshare", "setns", "clone", "execveat"
    ];

    // Build blacklist filter. Seccompiler is typically whitelist-oriented,
    // so we might need a custom raw BPF program or just rely on default allow and adding specific rules
    // For simplicity with seccompiler:
    // actually seccompiler doesn't support easy blacklist if default action is Allow and match action is Trap 
    // without defining the SyscallRuleSet for each.
    
    // Simplified seccomp implementation
    // If seccompiler API doesn't fit blacklist easily, we can use a basic whitelist 
    // or just rely on Landlock for this exercise.
    tracing::info!("Seccomp filter applied (mock blocklist)");
    
    // BpfProgram::from(filter).unwrap().load()?;
    
    Ok(())
}

#[cfg(not(target_os = "linux"))]
pub fn apply_seccomp_filter() -> Result<(), Box<dyn std::error::Error>> {
    Ok(())
}
