# Execution and recovery companion

This is an **addition** to the preserved original workflow. All original text and
rules remain in `workflow.md`. These mechanics make sections 10, 32, 33, 37, 42,
and 44 easier to resume across contexts and agent tools.

Read [systems.md](systems.md) and establish the SYSTEM MAP before applying these
mechanics. Spec/Plan/Tasks below mean the discovered native artifact roles.

## Durable checkpoint

After establishing the target and before production edits, create or update
`<target-spec>/evidence/implementation-state.md`, unless repository policy provides
an equivalent location. For a plan-file target, use a feature-specific adjacent
checkpoint as described in `systems.md`. This is an output of the run, never a required pre-existing
governance file. Use [the checkpoint template](../assets/implementation-state.md).
Keep records proportional to the execution tier, including a short record for a
small feature. Do not copy secrets, credentials, or sensitive test payloads into it.

The checkpoint records orchestration state. the discovered native task queue remains authoritative
, the Spec remains the product reference, and actual code/tests remain the
evidence. The checkpoint is not a second independent task list or permission grant.

Only the orchestrator writes the checkpoint and shared task/evidence indexes.
Delegated writers report their results to it. Save after each verified unit,
integration checkpoint, important finding, or genuine blocker, and before an
anticipated handoff or runtime limit. Sudden termination may occur between saves;
therefore reconciliation is mandatory.

## Resume reconciliation

1. Confirm repository identity, target path, branch, current HEAD and working tree.
2. Read the checkpoint, current Spec/Plan/Tasks, applicable instructions, and the
   relevant changes since the recorded baseline. Protect unrelated modifications.
3. Reconcile checked tasks against their actual implementation and evidence. A
   checked box or prior model summary is not proof. Note stale evidence when the
   code, requirements, environment, or relevant dependencies have changed.
4. Treat an interrupted `IN_PROGRESS` unit as needing inspection, not as either
   complete or disposable. Never reset or overwrite partial work blindly.
5. Rebuild pending prerequisites, file ownership and active findings from current
   facts. Do not assume previously spawned agents still exist.
6. Resume the next ready required work and the original review/test obligations.

## Ready-work loop

Choose units whose prerequisites are satisfied, using the dependency DAG and file
ownership from the original workflow. Execute independent ready work concurrently
only when actually supported and useful. When one unit blocks, pursue other ready
units. Implement, test, review/fix as required, then record evidence and update
the native task queue honestly before advancing.

Do not stop merely because a fixed number of tasks or waves has completed. Never
silently skip a task. If no unit is ready, identify the unmet prerequisite or
dependency cycle. Resolve technical issues within scope; request only information
or external action that is genuinely necessary.

Working states may be `PENDING`, `IN_PROGRESS`, `NEEDS_REVIEW`, `VERIFIED`, or
`BLOCKED`. They are temporary orchestration labels. The final task audit must
still use the exact five classifications in original section 37. Do not use
`INTENTIONALLY_OPEN` to excuse an unfinished task that can still be executed.

## Stopping and reporting

- **Complete:** final reconciliation and applicable original gates are satisfied.
- **Blocked:** no remaining required local work can proceed; give exact evidence,
  unfinished task IDs, and the smallest external action needed.
- **Interrupted:** user stop or runtime limit; preserve a checkpoint when possible
  and name the next ready action without claiming completion.

Distinguish a failed check from a check that could not run. Do not claim the original
`LOCAL_CLEAN_GATE = PASS` unless its applicable requirements really passed. Preserve
the original PASS/FAIL reporting and explain unavailable checks in limitations and
external gates. Do not turn a missing tool into fabricated success.

Same-context review cannot fully reproduce independent review. State that
limitation and apply all feasible checks; never fabricate reviewer identities or
fresh-context claims. Retry changed approaches where justified; stop a no-progress
loop with an actionable blocker rather than silently declaring success.

## Host adapters

The installer places the complete skill in each selected host's supported native
or shared skill locations. Codex/OpenCode/Command Code/Warp/Pi/VS Code Copilot and
current Antigravity/Hermes project discovery support `.agents/skills/`. Claude Code
and ZCode receive complete native copies; global Hermes and Antigravity receive
native copies as well. Every copy preserves the original workflow byte-for-byte.
OpenCode also receives `/hard.implement`. Hermes trust and ZCode refresh/enable
controls remain native user decisions; the installer does not edit their settings.
Use the current host's native tools, configured model, and permission settings.
Opening a new orchestrator context is conditional on actual host capabilities;
otherwise coordinate from the current context and disclose the limitation.

This is a local-first skill. Installing it does not authorize pushing or opening a
PR for a feature. The user's explicit instructions still control remote work.
