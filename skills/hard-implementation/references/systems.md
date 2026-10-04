# Native specification systems

This is an additive compatibility map for the complete preserved workflow.
The original uses Spec Kit terminology. For other systems, bind those terms to
**native roles**, not invented files. Do not rename, convert, duplicate, or migrate
existing requirements, plans, tasks, IDs, approvals, branches, or boards to Spec Kit.
All original engineering, review, evidence, risk, dependency, autonomy, and completion
requirements still apply. Naming compatibility does not lower correctness gates.

## Discover before implementing

1. Inspect applicable repository instructions, the explicit user target, current
   branch/worktree, existing checkpoints, and native feature indexes/boards. Discover
   the active system from actual artifacts and available native tools. Multiple
   systems may coexist. Prefer explicit target and established project conventions;
   do not pick the most recently modified file or whichever directory appears first.
2. `scripts/discover_system.py` can list conventional candidates read-only. Its output
   is a starting inventory, not an authoritative approval/readiness decision. Inspect
   custom paths, schema configuration, and metadata when the helper finds nothing or
   misidentifies an ambiguous Kiro-compatible layout. Kiro and cc-sdd can share files;
   check installed instructions/commands rather than treating a filename as proof.
3. Record a compact SYSTEM MAP in the checkpoint: system/version if discoverable,
   exact target, requirements sources, design/plan sources, native task queue/IDs,
   dependencies, current status/approval gates, allowed status-update mechanism,
   board/index locations, and checkpoint location. This is a role map, not a second
   task backlog. Read the relevant native artifacts completely before production edits.
4. When requirements/design/tasks from that system are missing, contradictory, or
   awaiting required approval, do not invent approved artifacts or bypass the gate.
   Optional artifacts remain optional if the active schema explicitly permits it.
   Ask one concise clarification only when a real target/scope decision is unresolved;
   continue independent authorized work when possible.

## Role binding

| System | Native target and requirements (examples; discover actual paths) | Design / execution queue | Preserve native behavior |
|---|---|---|---|
| Spec Kit | `specs/<feature>/spec.md` | `plan.md`; `tasks.md` with T IDs | Constitution, dependency/parallel markers, task IDs and checkboxes |
| Kiro Specs | `.kiro/specs/<feature>/requirements.md` | `design.md`; `tasks.md` (hierarchical numbered tasks) | EARS/acceptance references, optional task semantics and required spec approvals |
| cc-sdd | Kiro-compatible `.kiro/specs/<feature>/requirements.md` | `design.md`; `tasks.md`; phase/approvals in `spec.json` | Installed steering/rules, phase and approval protocol; distinguish from native Kiro via project evidence |
| Spec Workflow MCP | `.spec-workflow/specs/<feature>/requirements.md` | `design.md`; `tasks.md` | MCP approval gates and native task/progress/log tools; record implementation evidence through the project's protocol |
| OpenSpec | `openspec/changes/<change>/proposal.md`, delta `specs/*/spec.md`, applicable baseline `openspec/specs/*/spec.md` | Schema-dependent `design.md`; `tasks.md` | Inspect configured schema/artifact dependencies; proposal gives intent, deltas define approved changes; no automatic archive/spec sync |
| Spec Kitty | `kitty-specs/<feature>/spec.md` | `plan.md`; `tasks/WP*.md` (possibly lane subdirectories) plus task index | Work-package IDs/dependencies, worktrees, ownership and native lanes; use installed transition/review/acceptance commands, never fabricate `done` by editing metadata |
| Conductor | `conductor/tracks/<track>/spec.md` plus project context | `plan.md` contains phases/tasks and their statuses | `conductor/workflow.md`, track metadata/index, native in-progress/completed notation, test/commit/checkpoint requirements; no extra `tasks.md` |
| Superpowers | Existing approved design/spec, often `docs/superpowers/specs/` (older `docs/plans/`) | Linked implementation plan in `docs/superpowers/plans/` or project-selected path; Task N/step checkboxes | Read the plan's linked Spec and installed execution skills; preserve TDD, review and native task semantics; do not stop merely because an execution batch ended |

Treat original references to `spec.md`, `plan.md`, and `tasks.md` throughout **all**
sections as their SYSTEM MAP roles. Conductor/Superpowers may use one plan as both
design and task queue; Spec Kitty may use multiple work packages. Original task
reconciliation applies to every native queue item and applicable acceptance case.
The native system's documented product-artifact hierarchy governs which requirement
is authoritative; never infer semantic equivalence from filenames alone. Explicit
user constraints and applicable repository/runtime instructions still take precedence.

## State, boards, and completion

Use native IDs and update native task/status records after verified work using the
project's supported mechanism. A dashboard may depend on more than checkbox edits
(e.g. MCP implementation logs or Spec Kitty lane transitions). Discover and use its
native interface when available and authorized. If required tooling is unavailable,
record the missing transition as blocked; do not silently claim the board is updated.
Do not install a server, alter host configuration, or perform remote board mutations
without authorization. Read-only/local discovery is not authorization for remote work.

Keep recovery state near the target when appropriate, or at a project-approved
location. For a plan file target, a suitable default is an adjacent
`evidence/<plan-stem>/implementation-state.md`; avoid sharing one checkpoint across
unrelated plans. Reconcile with the native queue on every resume.

`audit_tasks.py --format markdown` inventories ordinary task checkboxes without
requiring T001 names, and recognizes Conductor `[~]` as in progress. It does not
interpret work-package lanes, approvals, skipped/optional tasks, acceptance evidence,
or a board's complete lifecycle. Use native task tools/manual reconciliation for
those. Never treat an empty inventory, unchecked optional task, or stale `done` lane
as proof of implementation success. Apply the original section 37 classifications
with explicit evidence, preserving each system's optional-task policy.

Completion requires the original applicable review/test/local gates and the native
workflow's required implementation/review transitions. Archive, publish, merge,
push, or external acceptance are separate actions requiring applicable authorization.
A workflow command with those side effects must not be invoked merely to finish
implementation. Report the remaining transition honestly.

## Primary references

- [Spec Kit](https://github.com/github/spec-kit)
- [Kiro Specs](https://kiro.dev/docs/specs/)
- [cc-sdd](https://github.com/gotalab/cc-sdd)
- [Spec Workflow MCP](https://github.com/Pimzino/spec-workflow-mcp)
- [OpenSpec](https://github.com/Fission-AI/OpenSpec)
- [Spec Kitty](https://github.com/spec-kitty/spec-kitty)
- [Conductor](https://github.com/gemini-cli-extensions/conductor)
- [Superpowers](https://github.com/obra/superpowers)

These are role-level integrations with observable fixtures, not a claim that every
version/schema or every live board has been exercised end to end. Never quote
unmeasured similarity percentages as compatibility evidence.
