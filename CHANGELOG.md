# Changelog

## 1.2.0

- Make the public entrypoint universal across Spec Kit, Kiro Specs, cc-sdd, Spec Workflow MCP, OpenSpec, Spec Kitty, Conductor, and Superpowers.
- Add native artifact-role discovery, queue/status/approval guidance, and a read-only `hard detect` command without migrating existing files.
- Add installation support for Claude Code, Hermes, Command Code, ZCode, Antigravity, Warp, Pi, and VS Code/Copilot alongside Codex and OpenCode.
- Add custom agent multi-selection and `--agent all`; retain `both` as the original Codex/OpenCode pair.
- Preserve the full original workflow byte-for-byte; native copies contain all resources.
- Add native Markdown task inventory including Conductor in-progress notation; keep strict Spec Kit inventory as the default.
- Respect Hermes profiles and protect external paths during updates/removal.

## 1.1.0

- Ship an installable `hard` command with the full workflow bundled in wheel and source distributions.
- Add a Rich terminal banner, guided agent/scope menus, verified progress, and usable next steps.
- Support project or global availability for Codex and OpenCode, including XDG configuration locations.
- Add `hard status`, guided removal, explicit automation options, and opt-in JSON output.
- Replace placeholder-led installation instructions with install-once and guided setup commands.
- Preserve the complete original workflow byte-for-byte and retain the minimal Python installer.

## 1.0.1

- Make distribution generation deterministic on Windows as well as Unix by sorting
  POSIX path strings explicitly and writing LF bytes. The complete original
  workflow and execution behavior are unchanged.
- Keep all platform validation jobs running when a different platform fails.

## 1.0.0

- Publish the complete original Hard Implementation workflow without deleting or
  shortening any original section, rule, or example.
- Add an Agent Skills entrypoint for Codex and OpenCode and `/hard.implement` for
  OpenCode, with a shared source of instructions.
- Add explicit ready-work continuation, durable checkpoints, and reconciliation on
  resume, with honest runtime and review limitations.
- Add a dependency-free project installer, ownership-aware removal, task inventory,
  preservation checks, installation tests, and reproducible live-agent fixtures.
- Include English and Egyptian Arabic installation and usage guides.
