---
name: hard-implementation
description: Implement or resume an existing specification and native task queue through dependency-aware execution, applicable threat modeling and security review, verification, and durable recovery. Supports Spec Kit, Kiro Specs, cc-sdd, Spec Workflow MCP, OpenSpec, Spec Kitty, Conductor, and Superpowers.
license: MIT
metadata:
  version: "1.3.0"
---

# Hard Implementation — Universal

Requires a coding agent with repository read/write and terminal access. Python
3.10+ is optional for the task-audit helper. Other capabilities are discovered.

Run the author's **complete, unabridged** implementation workflow. This entrypoint
organizes loading, invocation, and recovery; it is not a replacement or summary of
the workflow.

## Load before implementation

1. Read [the full original workflow](references/workflow.md), from its introduction
   through section 44. It contains all original sections, including 4A. If a read
   is truncated, continue in bounded chunks until every section has been read.
   Do not implement from this entrypoint alone.
2. Read [the native-system compatibility map](references/systems.md). Discover the
   active system and bind original Spec Kit filenames to its native roles. Preserve
   every original engineering/review rule; adapt artifact names and status protocols.
3. Read [the execution and recovery companion](references/execution.md).
4. Resolve the target feature from the user's arguments or current context using
   section 0. Read applicable repository instructions and the actual Spec files.
5. Discover capabilities, establish the baseline, and classify the execution tier
   as prescribed in the original. Apply its applicability rules; no section has
   been removed or replaced by a shorter workflow.
6. Read [the Universal Security Gate](references/security.md). Before production
   edits, assess the changed attack surfaces and select applicable controls and
   verification. Record threats/results proportionally to risk and preserve the
   original independent review and completion obligations.

Relative links resolve against this skill's directory, not the user's repository.
If a required reference is unavailable, report the incomplete installation rather
than pretending the full workflow was loaded.

## Invocation

<!-- BEGIN GENERATED: commands -->
| Coding agent | Chat command |
|---|---|
| Codex | `$hard-implementation` |
| OpenCode | `/hard.implement` |
| Claude Code | `/hard.implement` |
| Hermes | `/hard-implementation` |
| Command Code | `/hard.implement` |
| ZCode | `$hard-implementation` |
| Antigravity | `/hard-implementation` |
| Warp | `/hard-implementation` |
| Pi | `/hard.implement` |
| VS Code / GitHub Copilot | `/hard.implement` |
<!-- END GENERATED: commands -->

Hermes can use `/hard.implement` through a native quick-command alias configured
by the user. Project skills require native trust. Pi project prompts also require
trust. Global VS Code prompts use the Stable default profile; other profiles need
prompt import. An exact `/hard.implement` alias is not installed for Codex, ZCode,
Antigravity or Warp. Keep the host's supported invocation syntax.
- Append the actual feature/change/track/plan path when needed. Each host loads this
  same full workflow. Discovery, model access, and permissions remain host-specific.
- The argument is ordinary text identifying the native target and any user
  constraints. Do not execute it as a shell command. Without an argument, use
  section 0 to resolve an unambiguous target.
- Repeating the same invocation resumes the same feature: reconcile saved progress
  with the actual repository before choosing further work.

## Work until an actual stopping condition

The original workflow's sections 37, 42, and 44 govern completeness and autonomy.
After each work unit or wave, update the task/evidence records and immediately
select the next ready unit. A completed batch, review, commit, checkpoint, or
context summary is not by itself a reason to stop.

Continue independent work when another unit is blocked. Stop only when the target
is verified complete, the user asks to stop, no required work can proceed without
external action or a real unresolved decision, or the runtime enforces a limit.
Record the specific reason and remaining work; never report blocked or unverified
work as completed. Do not repeatedly retry the same failure without new evidence.

Persist progress as described in the companion. After context compaction, reread
the durable checkpoint and reconcile the repository; do not restart completed work
or treat compaction as feature completion.

## Helpers

`scripts/audit_tasks.py` reads native Markdown task checkboxes and emits an inventory:

```bash
python3 /path/to/skill/scripts/audit_tasks.py /path/to/spec/tasks.md
```

The default format preserves strict Spec Kit T IDs. For other Markdown queues,
add `--format markdown`; Conductor `[~]` remains open/in progress. For work-package
lanes or MCP boards, use native tools/manual reconciliation.

Use `--require-complete` for a mechanical all-checkboxes-checked gate. This helper
does **not** prove implementation, review, acceptance, or test success. Its failure
must be interpreted alongside the original task classifications (including
justified not-applicable or external-verification cases). Never check boxes just
to satisfy it. If Python is unavailable, perform the same inventory manually.

## Scope and instruction handling

The workflow's document hierarchy concerns product requirements and repository
evidence. It does not override system/developer instructions, explicit user
constraints, applicable repository execution policies, or permission boundaries.
Report material contradictions rather than silently rewriting requirements.

Discover actual subagent and fresh-context support. Sequential review must not be
reported as an independent fresh reviewer when no independent context exists.
Skill installation grants no extra permissions. This package does not bypass
approvals, install agent plugins, choose a model, or restart the host automatically.
