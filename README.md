# Hard Implementation — Universal

**The complete implementation, review, verification, and recovery workflow for
existing specification systems and coding agents.**

Use the project’s existing requirements, design, and native task queue. Discover
its specification system, execute work in dependency order, review at the required
risk depth, verify the result, and continue ready work through durable checkpoints.

[الشرح بالمصري](README.ar.md) · [Agent compatibility](docs/COMPATIBILITY.md)
· [Native-system map](skills/hard-implementation/references/systems.md)
· [Original workflow](skills/hard-implementation/references/workflow.md)
· [Preservation audit](docs/PRESERVATION.md) · [Validation](docs/VALIDATION.md)

## Full workflow, preserved

The author’s original **2,397-line, 46-section workflow** is preserved byte-for-byte.
Nothing has been shortened or deleted. Its historical title and filenames still
mention Spec Kit. The loading entrypoint and additive native-system map bind those
names to the actual project’s artifact roles, while retaining all engineering,
review, evidence, dependency, risk, recovery, and completeness rules.

Supported specification systems: **Spec Kit, Kiro Specs, cc-sdd, Spec Workflow MCP,
OpenSpec, Spec Kitty, Conductor, and Superpowers**. These are native artifact/state
integrations, not migrations to Spec Kit. The agent preserves task IDs, optional-task
semantics, approval gates, work-package lanes, and native board update mechanisms.
Conductor and Superpowers can execute tasks embedded in an implementation plan;
Spec Kitty can execute a queue made of multiple work packages.

This starts at the implementation stage. Existing requirements and the applicable
approved design/plan/task artifacts must already exist. Missing required approvals
remain blockers. Schema-optional artifacts remain optional. Multiple systems or
features can coexist: an ambiguous target is not automatically chosen.

## Install the command once

Requirements: [uv](https://docs.astral.sh/uv/getting-started/installation/), Git,
Python 3.10+ (uv can provision it), and your chosen coding agent/model access.

```bash
uv tool install git+https://github.com/Mohammed-AliDev/hard-implementation.git@v1.2.1
```

Updating an existing `hard` command:

```bash
uv tool install --reinstall git+https://github.com/Mohammed-AliDev/hard-implementation.git@v1.2.1
```

The package source is GitHub, not PyPI. The complete skill ships inside the package;
project/global setup needs no subsequent workflow download. If `hard` is not found,
run `uv tool update-shell` and reopen the terminal.

## Guided setup

From your actual project directory:

```bash
hard init
```

Choose your coding agent, then this project or all projects on this computer.
The agent menu includes **Codex, OpenCode, Claude Code, Hermes, Command Code,
ZCode, Antigravity, Warp, Pi, and VS Code / GitHub Copilot**. Choose one, a custom
selection (Space toggles agents), all agents, or the original Codex/OpenCode pair.
Confirm the displayed settings; setup verifies the complete workflow, checks
existing files, installs, and displays native invocation commands.

For scripts/CI, select explicitly:

```bash
hard init --here --agent all --yes
hard init --global --agent claude --agent hermes --agent commandcode --yes
hard init my-project --agent zcode --agent pi --yes
hard init --here --agent all --dry-run
```

`--agent both` retains its original meaning: Codex + OpenCode. Repeating `--agent`
adds support for another host without removing previously installed hosts.
A new project path creates that directory; no specification scaffold is invented.
The skill does not install coding agents, change models, edit host settings, or
change project governance. Global availability applies on this machine.

Hermes project discovery requires a Git repository and native project trust;
setup displays `hermes skills trust` as a user step and does not modify trust.
Hermes global copies follow `HERMES_HOME` when set. Antigravity global copies cover
both current IDE/2.0 and CLI locations. ZCode may need Settings → Skills → Refresh
and its enable switch. VS Code here means Copilot Agent chat: Codex/Claude extensions
use their own host integrations. See [exact paths and sources](docs/COMPATIBILITY.md).

## Run in your coding agent

Commands below go in **agent chat**, not your shell. Append the actual feature,
change, track, work-package collection, or linked plan path when needed.

| Agent | Invocation |
|---|---|
| OpenCode / Claude Code / Command Code / Pi / VS Code Copilot | `/hard.implement` |
| Codex / ZCode | `$hard-implementation` |
| Hermes / Antigravity / Warp | `/hard-implementation` |

**The exact slash command is installed for the five hosts in the first row.**
Other hosts keep their supported invocation syntax; the package does not register
unsupported aliases. Hermes can use the same spelling through a native quick-command
alias. See [command support, setup, and limitations](docs/COMMANDS.md). Pi project
prompts require trust; `/reload` refreshes an open session. Global VS Code prompts
are placed in the Stable default user profile; custom/portable/Insiders profiles
need import into the active profile.

The agent first reads the full original workflow and native-system map, discovers
what the project uses, and preserves its own implementation process. Restart or
refresh an open host session if needed. No model subscription is provided.

## Inspect, resume, and uninstall

```bash
hard status
hard detect
```

`status` verifies installed files in the current project and global scope. `detect`
is read-only conventional-layout discovery; it lists native requirements, design,
and queues. It does not grant approvals, mutate a board, or prove task completion.
Custom artifact locations and schema changes still require agent inspection.
`--json` is opt-in machine-readable output.

After an interruption, repeat the same agent invocation for the same target.
The agent reconciles saved progress against the actual native queue, code, branch,
and evidence, then continues ready work. The feature-specific checkpoint records
orchestration state; the native queue remains authoritative. A completed batch is
not feature completion. A skill cannot restart a closed host, replenish quota,
override permissions, or guarantee a model’s behavior.

```bash
hard uninstall --here
hard uninstall --global
```

For non-interactive removal, add `--yes`. Removal covers all unchanged installer-owned
copies/commands in that scope. Unrelated files, identical unowned files, and feature
checkpoints remain. Modified managed files cause a stop instead of being overwritten.
`uv tool uninstall hard-implementation` separately removes the program; it does not
remove installed skills. Ordinary write failures are rolled back. Abrupt process
termination is not a transaction guarantee; avoid concurrent installers in one scope.

Project/global ownership records live under `.hard-implementation/`. The shared
skill is `.agents/skills/hard-implementation/`; required native copies are listed
in the compatibility guide. Selecting one host does not prevent other hosts that
scan shared skills from discovering the same skill. Hashes verify content integrity;
they do not provide a signed publisher identity.

## Minimal Python alternative

The dependency-free legacy installer still supports project setup. From your actual
project (select agents explicitly; default retains Codex + OpenCode):

```bash
uv run --no-project https://raw.githubusercontent.com/Mohammed-AliDev/hard-implementation/v1.2.1/install.py --project . --agent claude --agent hermes
```

Or clone this release and use local Python:

```bash
git clone --branch v1.2.1 --depth 1 https://github.com/Mohammed-AliDev/hard-implementation.git
python3 hard-implementation/install.py --project . --source hard-implementation --agent claude
```

The detached-HEAD notice is normal for a release tag. On Windows, `py -3` can
replace `python3`. The guided `hard` CLI is the recommended install/update/remove route.

## Alternative skills distribution

The repository’s `skills/hard-implementation` is a standard Agent Skills package.
Other skill installers can install it, but may not supply our OpenCode command,
additional native/global copies, or ownership records. Manage those installations
with the installer that created them; do not assume `hard uninstall` owns them.

## Development and validation

```bash
uv sync
uv run python -m unittest discover -s tests -v
uv run python scripts/build_distribution.py
uv build
git diff --exit-code
```

The suite checks the original byte-for-byte preservation, all selected native host
paths, install/reinstall/uninstall/conflict/rollback behavior, eight system fixtures,
read-only detection, and native checkbox inventories. See [validation evidence](docs/VALIDATION.md)
for test levels and the earlier Codex/OpenCode live implementation/resume scenario.
Package compatibility checks are not end-to-end live execution on every host/board.

Independent community project, not an official release of the named tools.
[MIT licensed](LICENSE). Preserve the original workflow; propose substantive revisions
explicitly instead of silently shortening it. Do not include credentials in reports.
