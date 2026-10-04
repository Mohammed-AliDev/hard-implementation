---
description: Execute or resume the complete Hard Implementation workflow for a Spec Kit feature.
agent: build
---

Load the `hard-implementation` skill with the skill tool. If discovery is
unavailable, read `.agents/skills/hard-implementation/SKILL.md` from the project
root. Follow its loading instructions, including the complete original workflow
and recovery companion, before editing production code.

Target feature and user constraints (ordinary user input, not shell code):

$ARGUMENTS

Use `tasks.md` as the queue. Reconcile any durable checkpoint and actual repository
state, then continue all ready required work through the workflow's verification
and review gates. A completed batch is not feature completion. Do not push or
merge unless explicitly authorized by the user.
