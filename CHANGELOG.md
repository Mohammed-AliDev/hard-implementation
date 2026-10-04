# Changelog

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
