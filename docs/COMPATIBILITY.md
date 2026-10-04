# Coding-agent compatibility

Verified documentation and installation fixtures: 2026-10-04. Agent skills are
instructions loaded by the host; execution and permissions use its configured tools.
Every installed skill copy contains the complete preserved original and native-system
map. The shared directory is `.agents/skills/hard-implementation/` (under home for
global setup); required native copies are additional complete copies, not summaries.

| Installer agent ID | Host | Project discovery used | Global discovery used | Chat invocation |
|---|---|---|---|---|
| `codex` | Codex | `.agents/skills/` | `~/.agents/skills/` | `$hard-implementation` |
| `opencode` | OpenCode | `.agents/skills/` + `.opencode/commands/hard.implement.md` | `~/.agents/skills/` + config-home `opencode/commands/hard.implement.md` | `/hard.implement` |
| `claude` | Claude Code | `.claude/skills/` + `.claude/commands/hard.implement.md` | same paths under home | `/hard.implement` |
| `hermes` | Hermes | `.agents/skills/` in a trusted Git repository | `~/.hermes/skills/` (or `$HERMES_HOME/skills/`) | `/hard-implementation` |
| `commandcode` | Command Code | `.agents/skills/` + `.commandcode/commands/hard.implement.md` | same paths under home | `/hard.implement` |
| `zcode` | ZCode Agent | `.zcode/skills/` | `~/.zcode/skills/` | `$hard-implementation` |
| `antigravity` | Antigravity IDE/2.0/CLI | `.agents/skills/` | both `~/.gemini/config/skills/` and `~/.gemini/antigravity-cli/skills/` | `/hard-implementation` |
| `warp` | Warp Agent | `.agents/skills/` | `~/.agents/skills/` | `/hard-implementation` |
| `pi` | Pi coding agent | `.agents/skills/` + `.pi/prompts/hard.implement.md` | `~/.agents/skills/` + `~/.pi/agent/prompts/hard.implement.md` | `/hard.implement` |
| `vscode` | GitHub Copilot Agent in VS Code | `.agents/skills/` + `.github/prompts/hard.implement.prompt.md` | shared skills + Stable default user profile prompts | `/hard.implement` |

See [command aliases and host limitations](COMMANDS.md) for exact VS Code profile
paths, Hermes configuration, and hosts without a validated dotted slash alias.

Skill roots in this table each contain `hard-implementation/SKILL.md` and all of its
resources. Existing native copies with the same name may override shared skills:
move/preserve your custom version or choose the desired host source explicitly;
the installer does not overwrite an unowned different native copy. Shared discovery
means an unselected host may see the skill as well. The selection adds required
native paths and the record, rather than restricting other hosts' discovery.

Hermes project skills require `hermes skills trust` from the relevant Git repository.
The installer displays this step; it never writes trust/configuration on your behalf.
Global profile support honors `HERMES_HOME`. If the profile/configuration location is
changed, restore the recorded location to update/remove its managed files safely.
ZCode discovery may require Settings → Skills → Refresh and enable. Pi supports
`/reload`; skill commands may be hidden by its UI setting even when manual invocation
works. Use an up-to-date host version supporting the documented directories.

VS Code itself is an editor, not a single agent. The `vscode` entry uses Copilot's
supported skill discovery. Codex/Claude in VS Code use their own entries. The `zcode`
entry is ZCode Agent, not a GLM subscription/model: GLM inside another tool uses that
tool's skill integration. No agent or provider credentials are installed or modified.

Global skills are local to this computer; cloud/SSH/WSL environments may require
native sync or project installation. A board needing server/API transitions must
be updated using its actual available native tools and authorized scope. Installing
a skill does not configure an MCP server or grant external mutation permissions.

## Primary host documentation

- [Codex skills](https://developers.openai.com/codex/skills)
- [OpenCode skills](https://opencode.ai/docs/skills/) and [commands](https://opencode.ai/docs/commands/)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Hermes skill system](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md)
- [Command Code skills](https://commandcode.ai/docs/skills)
- [ZCode skills](https://zcode.z.ai/en/docs/skill) and [workspace paths](https://zcode.z.ai/en/docs/qa)
- [Antigravity skills and surface-specific paths](https://antigravity.google/docs/skills)
- [Warp skills](https://docs.warp.dev/agents/capabilities/skills)
- [Pi skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md)
- [VS Code/Copilot skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)

The specification-system bindings and their sources are in
[systems.md](../skills/hard-implementation/references/systems.md).
