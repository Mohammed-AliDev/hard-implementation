# Command spelling and native aliases

`/hard.implement` is the preferred public command. Hosts own their command parser:
installing a skill cannot change a host's reserved prefixes or name validation.
The canonical skill remains `hard-implementation`, with the full original workflow
unchanged. Command files are loading adapters, not shortened replacement skills.

## Automatically installed commands

`hard init` installs these files when their corresponding agent is selected:

| Host | Project command file | Global command file | Chat command |
|---|---|---|---|
| OpenCode | `.opencode/commands/hard.implement.md` | XDG config-home `opencode/commands/hard.implement.md` | `/hard.implement` |
| Claude Code | `.claude/commands/hard.implement.md` | `~/.claude/commands/hard.implement.md` | `/hard.implement` |
| Command Code | `.commandcode/commands/hard.implement.md` | `~/.commandcode/commands/hard.implement.md` | `/hard.implement` |
| Pi | `.pi/prompts/hard.implement.md` | `~/.pi/agent/prompts/hard.implement.md` | `/hard.implement` |
| VS Code Copilot | `.github/prompts/hard.implement.prompt.md` | Stable default user-profile `prompts/hard.implement.prompt.md` | `/hard.implement` |

Arguments remain ordinary user input. The adapter directs the host to load the
complete installed skill and its execution, system and security references before
implementation; its original approval and task queue rules still apply. Existing
native skill invocations remain available too.
Restart/reload active sessions when discovery is cached. Pi project templates
require project trust, and `/reload` refreshes its loaded prompts.

VS Code's default Stable profile locations are:

- Linux: `$XDG_CONFIG_HOME/Code/User/prompts/`, or `~/.config/Code/User/prompts/`.
- macOS: `~/Library/Application Support/Code/User/prompts/`.
- Windows: `~/AppData/Roaming/Code/User/prompts/` with the standard roaming location.

The installer does not change VS Code settings or profile selection. With custom
profiles, relocated user-data/roaming directories, Portable, Insiders, or remote
VS Code, use **Chat: New Prompt File → User**, name it `hard.implement`, and copy
the installed prompt's contents into that active profile. A project installation
avoids selecting a personal profile location. VS Code here means Copilot Agent
chat; a Codex/Claude extension uses that agent's own command system.

## Hermes

Hermes supports the exact spelling through its native `quick_commands` aliases.
After installing the skill for Hermes, merge this entry into the active Hermes
profile's `config.yaml` (`~/.hermes/config.yaml` or `$HERMES_HOME/config.yaml`):

```yaml
quick_commands:
  hard.implement:
    type: alias
    target: /hard-implementation
```

If `quick_commands` already exists, add `hard.implement` under that existing map;
do not create a duplicate top-level YAML key or replace other commands. Restart
Hermes if it has already loaded the configuration. `/hard.implement <target>`
then dispatches to the installed skill and forwards the target/constraints. The
alias can work when manually typed even if that surface does not show it in
autocomplete. Project skill loading still needs native repository trust.

This is a user-profile alias even when the skill is installed only in one project.
`hard init --here` does not silently rewrite a global configuration file. The
installer therefore continues to display the immediately usable native Hermes
command until you add this optional alias. Remove the alias manually if you later
uninstall the skill; it is not an installer-owned setting.

## Hosts without an automatically installed exact alias

| Host | Immediately supported invocation | Limitation |
|---|---|---|
| Codex | `$hard-implementation` | Skills use `$name`. Deprecated custom prompts use `/prompts:name`, including `/prompts:hard.implement`; that is a different command and is not an exact `/hard.implement` alias. |
| ZCode | `$hard-implementation` | The documented plugin command-name schema excludes dots (`^[a-z0-9][a-z0-9_:-]{0,63}$`). A dotted direct/custom-command alias has not been validated; it is not installed or advertised. |
| Antigravity | `/hard-implementation` | Its maintained skill interface uses the skill name. An IDE workflow can provide a filename-based slash alias, but workflows are scheduled to retire on November 1, 2026 and do not establish a cross-surface CLI/2.0 alias. This package keeps the skill interface. |
| Warp | `/hard-implementation` | Official documentation describes slash commands derived from skill names. A separate dotted command/alias mechanism has not been validated. |

The package does not rename the standards-compliant skill to `hard.implement`,
patch agent binaries, or treat an unrecognized chat message as a registered command.
Exact command support and workflow compatibility are separate: all these hosts
can still load the same complete universal implementation workflow.

## Primary sources

- [OpenCode command files](https://opencode.ai/docs/commands/).
- [Claude Code skills and compatible command files](https://code.claude.com/docs/en/skills).
- [Command Code custom slash commands](https://commandcode.ai/docs/reference/slash-commands).
- [Pi prompt templates](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/prompt-templates.md).
- [VS Code prompt files](https://code.visualstudio.com/docs/agent-customization/prompt-files) and [profile resource locations](https://github.com/microsoft/vscode/blob/main/src/vs/platform/userDataProfile/common/userDataProfile.ts).
- [Hermes native quick commands](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/slash-commands.md#quick-commands).
- [Codex custom prompt prefix and deprecation](https://developers.openai.com/codex/custom-prompts).
- [ZCode plugin command schema](https://zcode.z.ai/en/docs/plugin).
- [Antigravity workflow retirement](https://www.antigravity.google/docs/migration/workflows-to-skills/).
- [Warp skill invocation](https://docs.warp.dev/agents/capabilities/skills).
