# Hard Implementation

**The complete Spec Kit implementation workflow for Codex and OpenCode.**

Execute an existing feature through dependency-aware implementation, risk-based
review, local verification, and durable progress checkpoints. Continue ready work
instead of treating the end of a task batch as the end of the feature.

[الشرح بالمصري](README.ar.md) · [Original workflow](skills/hard-implementation/references/workflow.md)
· [Preservation audit](docs/PRESERVATION.md) · [Validation](docs/VALIDATION.md)

## Full workflow, preserved

The author's original **2,397-line, 46-section workflow** is included byte-for-byte.
Nothing has been shortened, deleted, or replaced with an abbreviated workflow.
The skill entrypoint requires the agent to read the complete original before
implementation. A separate companion adds durable checkpoints and host-specific
loading guidance. Applicability and execution tiers come from the original itself.

The original covers repository/technology discovery, dependency DAGs, explicit file
ownership, adaptive parallelism, risk classification, specialist reviews, root-cause
fixes, contracts, persistence, security, UI/platform behavior, concurrency/recovery,
test validity, clean local gates, task reconciliation, local commits, and evidence.

This package starts at the **implementation** stage. Prepare an existing Spec Kit
feature with `spec.md`, `plan.md`, and `tasks.md` first.

## Install into your project

Requirements: Codex or OpenCode, repository editing/terminal access, and either
[uv](https://docs.astral.sh/uv/getting-started/installation/) or Python 3.10+.
The installer has no third-party Python dependencies. Model access is provided by
your existing agent account/configuration; the package does not supply a model.

Run from your **target project's root**:

```bash
uv run --no-project https://raw.githubusercontent.com/Mohammed-AliDev/hard-implementation/v1.0.0/install.py
```

This installs support for **both** Codex and OpenCode. To select one:

```bash
uv run --no-project https://raw.githubusercontent.com/Mohammed-AliDev/hard-implementation/v1.0.0/install.py --agent codex
uv run --no-project https://raw.githubusercontent.com/Mohammed-AliDev/hard-implementation/v1.0.0/install.py --agent opencode
```

You can inspect the [installer](install.py) or preview destinations by appending
`--dry-run`. Use `--project /path/to/project` to choose a different project directory.
The command uses the pinned release, not a moving branch.

### Without uv

Clone the release into a separate tools directory, then run Python against your
target project:

```bash
git clone --branch v1.0.0 --depth 1 https://github.com/Mohammed-AliDev/hard-implementation.git
python3 hard-implementation/install.py --project /path/to/your/project
```

On Windows, `py -3` can replace `python3` when that is your Python launcher.
A downloaded checkout can install offline with `--source /path/to/checkout`.

## Run in your coding agent

Start the agent from the target project. Replace `specs/001-your-feature` with the
actual feature directory. These commands go in the **agent chat**, not the shell.

**Codex**

```text
$hard-implementation specs/001-your-feature
```

**OpenCode**

```text
/hard.implement specs/001-your-feature
```

If the new skill/command is not visible, restart the agent session. The installer
does not change your selected model, permission settings, or existing agent config.

The argument can include a feature path and ordinary user constraints. If omitted,
the workflow discovers the target and asks only when the choice is genuinely
ambiguous. A missing or contradictory Spec is not permission to invent a feature.

## Resume after interruption

Run the same command with the same feature path. The agent reads the checkpoint,
checks the actual branch, code, task states, and evidence, and continues the ready
work. It does not assume every checked box or earlier summary is valid.

The default checkpoint is:

```text
specs/001-your-feature/evidence/implementation-state.md
```

Repository policy may select an equivalent location. `tasks.md` remains the
authoritative work queue. The checkpoint records progress and the next action;
it does not authorize additional scope or replace verification.

**A skill cannot restart a closed host, override permission limits, replenish model
quota, or guarantee any model's behavior.** It instructs the running agent to keep
working and preserves enough state for a later invocation. A real external blocker
or user stop remains a valid stopping condition. Multi-agent execution is used only
when available and useful; same-context review is labeled honestly.

## Installed files and ownership

```text
your-project/
├── .agents/skills/hard-implementation/   # shared complete skill
├── .opencode/commands/hard.implement.md  # only with OpenCode selected
└── .hard-implementation/install.json    # installer ownership and hashes
```

The installer refuses conflicting files and locally modified managed files. An
identical pre-existing file is usable but is not claimed for later deletion. It
does not edit `AGENTS.md`, `opencode.json`, Codex config, or your Spec files. File
hashes detect payload corruption; they are not a signed publisher identity system.

Repeat the same install to repair missing managed files or confirm an unchanged
installation. Selecting another agent adds its support; it does not remove support
previously installed. For future releases, use that release's installer. Save local
customizations elsewhere before updating; there is deliberately no overwrite flag.

Uninstall with the same script and `--uninstall`:

```bash
uv run --no-project https://raw.githubusercontent.com/Mohammed-AliDev/hard-implementation/v1.0.0/install.py --uninstall
```

Uninstall removes only unchanged installer-owned files for both agents. Unrelated
files, pre-existing identical files, and feature checkpoints remain. Empty folders
may remain. Ordinary write failures are rolled back; abrupt process termination is
not a transaction guarantee. Avoid simultaneous installers in the same project.

## Alternative: standard skills installer

For the shared skill itself, the repository also supports:

```bash
npx skills add Mohammed-AliDev/hard-implementation --skill hard-implementation --agent codex --agent opencode
```

This third-party route installs the **skill**, not our OpenCode slash-command
adapter or ownership record. In OpenCode, request “Use the hard-implementation
skill for specs/001-your-feature”, or use our installer for `/hard.implement`.
Manage installations with the same installer that created them.

## Validation and development

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_distribution.py
git diff --exit-code
```

The tests verify preservation, distribution integrity, installation lifecycle,
conflict protection, rollback, and task inventory. See [validation evidence](docs/VALIDATION.md)
for the separate real-agent completion and controlled pause/resume checks. Those
checks are smoke tests, not a guarantee for every feature, model, or platform.

Create an isolated scenario for another live evaluation:

```bash
python3 scripts/create_smoke_project.py /tmp/my-hard-implementation-test
python3 install.py --project /tmp/my-hard-implementation-test
```

The fixture uses a small standard-library Python invoice module so dependency order,
invalid inputs, task completion, user-file preservation, and resume are observable.
Production use still follows the **full** workflow, adapting depth to actual risk.

## Compatibility references

- [Codex local skills](https://developers.openai.com/codex/skills)
- [OpenCode skills](https://opencode.ai/docs/skills/)
- [OpenCode commands](https://opencode.ai/docs/commands/)
- [Agent Skills format](https://agentskills.io/specification)
- [Spec Kit](https://github.com/github/spec-kit)

Independent community project; not an official GitHub, OpenAI, or OpenCode release.
Distributed under the [MIT license](LICENSE). Issues and focused pull requests are
welcome. Preserve the original workflow: propose substantive revisions explicitly
instead of silently shortening it. Never include credentials in issue reports.
