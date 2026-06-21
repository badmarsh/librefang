# Migration Report: OpenClaw -> LibreFang

## Summary

- Imported: 6 items
- Skipped: 4 items
- Warnings: 0

## Imported

| Type | Name | Destination |
|------|------|-------------|
| Config | openclaw.json | /home/ubuntu/.librefang/config.toml |
| Agent | orchestrator | /home/ubuntu/.librefang/agents/orchestrator/agent.toml |
| Agent | developer | /home/ubuntu/.librefang/agents/developer/agent.toml |
| Agent | research-analyst | /home/ubuntu/.librefang/agents/research-analyst/agent.toml |
| Agent | content-creator | /home/ubuntu/.librefang/agents/content-creator/agent.toml |
| Agent | reviewer-qa | /home/ubuntu/.librefang/agents/reviewer-qa/agent.toml |

## Skipped

| Type | Name | Reason |
|------|------|--------|
| Config | hooks | Webhook hooks not supported — use LibreFang's event system instead |
| Config | auth-profiles | Auth profiles (API keys, OAuth tokens) not migrated for security — set env vars manually |
| Skill | 1 skill entries | Skills must be reinstalled via `librefang skill install` |
| Config | session | Session scope config differs — LibreFang uses per-agent sessions by default |

## Next Steps

1. Review imported agent manifests in `/home/ubuntu/.librefang/agents/`
2. Review `/home/ubuntu/.librefang/secrets.env` — verify tokens were migrated correctly
3. Set any remaining API keys referenced in `/home/ubuntu/.librefang/config.toml`
4. Start the daemon: `librefang start`
5. Test your agents: `librefang agent list`
