# Validation evidence

Validation date: **2026-10-04 (Africa/Cairo)**.

## Current package checks (v1.3.2)

- Original author's attachment preserved byte-for-byte: 55,439 bytes, 2,397 lines,
  46 numbered sections (0–44 and 4A). SHA-256 and section index are in
  [PRESERVATION.md](PRESERVATION.md).
- `uv run python -m unittest discover -s tests -v`: **57 tests passed** on Linux.
- Skill Creator `quick_validate.py`: **passed**.
- Python compilation check: **passed**.
- Earlier independent review exercised the installer and read the complete skill. A
  state-directory collision defect was found, fixed, and covered by regression
  tests; ordinary I/O failure rollback was also added and tested.
- Earlier OpenCode native `debug skill` and `debug config` commands recognized the
  installed shared skill and `hard.implement` command in an isolated project.

The package suite covers install/reinstall/uninstall, selecting supported agents,
preserving unrelated and pre-existing identical files, refusing modified managed
files and conflicting destinations, parent/symlink checks, payload corruption,
record path validation, ordinary write-failure rollback, and honest task inventory.

## Realistic lion release (1.3.2)

- The lion source is a generated photorealistic transparent PNG, preserved with its
  built-in generation prompt in [BRANDING.md](BRANDING.md). Terminal compilation
  retains natural fur/face/mouth colors; ALAEEB is purple in full/compact layouts.
- Actual dark/light previews were inspected at 112 columns and the compact side-by-side
  layout at 80 columns. Rendering remains a terminal cell approximation of the image.
- Manual width checks covered 20, 23, 24, 40, 42, 60, 74, 75, 76, 87, 88, 103, 104,
  112 and 160 columns in truecolor, 256-color and monochrome output. ASCII, CP1252,
  UTF-8 and NO_COLOR remained printable; all compiled pixel buffers matched their
  declared dimensions and the source SHA-256 matched the preserved image.
- All 57 package tests passed locally. Security/system/native command behavior and
  original workflow bytes are unchanged; no new model execution was run for this
  decorative change. Pillow is needed only to regenerate artwork, not by users.
- The wheel includes compiled artwork without the PNG or Pillow. The source archive
  includes the preserved PNG, prompt documentation and compiler. Rendering from
  the installed wheel passed in an isolated environment.

## Lion branding release (1.3.1)

- The terminal renderer uses a roaring pixel-art lion with HARD and ALAEEB wordmarks.
  Actual Rich SVG exports were inspected on dark/light backgrounds and at medium width.
- A real terminal `hard init --dry-run` displayed the full color layout; another
  terminal run with NO_COLOR used its ASCII fallback. Both remained read-only.
- Manual width checks covered 20, 23, 24, 40, 42, 60, 75, 76, 80 and 160 columns,
  with/without color. ASCII, CP1252, UTF-8 and NO_COLOR output remained printable;
  the existing JSON test confirms decoration is absent from machine output.
- All 57 existing package tests passed locally, including legacy Windows encoding,
  setup/status, JSON and installer preservation. No new model execution was required
  for this visual change. Security controls, native invocations and original bytes
  are unchanged.
- The consistency checker additionally detects a stale version in the README's
  terminal SVG preview. Preview rendering dependencies are development-only;
  runtime still uses the same Rich/questionary dependencies.
- Wheel/source archives include the renderer; the source archive also includes the
  SVG and preview script. Rendering from the installed wheel passed in isolation.

## Security and consistency release (1.3.0)

- All ten hosts' project/global lifecycle fixtures include the required security
  companion in every full skill copy. Missing or corrupt gate payloads are rejected
  before destination writes; unchanged original bytes remain verified.
- A project installed with the published v1.2.1 CLI was upgraded to v1.3.0 with
  all ten agents selected. Status passed, every native copy included security.md,
  and the original workflow and user-owned file were unchanged.
- Consistency tests catch stale entrypoint/package/README versions, stale native
  commands, broken local references, missing security resources and outdated About
  descriptions/topics. Metadata preview is tested to remain read-only.
- Full-repository consistency checks and Skill Creator validation passed locally.
  AGENTS.md makes the manual full-file review a maintenance requirement; CI checks
  local facts and reads GitHub About on pushes to main.
- GitHub About description/topics were updated and read back successfully. Wheel
  and source archives contain the security gate; an isolated wheel installation
  with all ten agents passed status. Maintenance instructions, metadata and lockfile
  are included in the source archive.
- The new security instructions were checked for applicable threat modeling,
  control coverage, evidence and risk-based closure requirements. This verifies
  packaging/instruction coverage, not certification or a live security assessment
  of every supported host or target application. Earlier paid live-agent scenarios
  below predate this security companion and were not rerun for this release.

## v1.2.1 command adapters

- All five native command files install in project/global locations and route to
  the same complete skill. Reinstall, upgrade from the v1.2.0 ownership layout,
  command collisions, edited command protection, and unowned-identical command
  preservation are covered. VS Code default profile locations for Linux, macOS,
  and Windows and external configuration-path changes are covered.
- OpenCode's actual `--pure debug config` recognizes `hard.implement` and its
  complete-skill loading template in an isolated project.
- Pi **1.0.2** was installed under a temporary npm prefix. Its actual published
  `loadPromptTemplates` and `expandPromptTemplate` recognized `/hard.implement`,
  returned no diagnostics, and forwarded a quoted target with spaces and literal
  `$1` argument text without recursive substitution. No agent/model was started.
- Command Code **1.28.0**: its actual native `loadCommandsFromDirectory` function
  was extracted from the installed CLI bundle and exercised against the fixture
  through a filesystem adapter. It recognized the dotted filename and full-skill
  loading body. This checks native loading, not full interactive dispatch/model
  execution.
- Claude Code and VS Code prompt adapters use their official documented native
  formats. Their paths/payload/ownership are tested; a live chat execution has not
  been run for these new aliases. Hermes's optional config alias is documented,
  not automatically configured or claimed as an installed command.
- Wheel/source builds include every new adapter. The original workflow hash is
  unchanged. Exact `/hard.implement` registration is not claimed for Codex, ZCode,
  Antigravity, or Warp; [COMMANDS.md](COMMANDS.md) records the constraints.

## Real-agent scenario

The fixture is generated by `scripts/create_smoke_project.py`. It contains a Spec,
Plan, four dependent task IDs, a baseline test, and a user-owned file. The required
feature is a pure-Python invoice parser/total calculator with explicit invalid-input
boundaries. No external dependencies, databases, or production systems are involved.

Hosts tested:

- Codex CLI **0.153.4**.
- OpenCode **1.18.34**, using `--pure` to exclude external plugins.

Each host receives the complete installed skill, not an abbreviated substitute.
Subagents are explicitly disabled in this bounded evaluation. Results do not prove
multi-agent orchestration, large-feature execution, or independent review quality.

### Controlled pause

Each agent was explicitly asked to implement and verify T001 only, persist a
checkpoint, and stop. Both did so, leaving T002–T004 unchecked and recording an
interrupted state rather than reporting feature completion.

- Codex: **5 tests passed** after T001.
- OpenCode: **14 tests passed** after T001.

### Fresh-session resume

Both agents were invoked again in a new session against the same fixture, with the
pause revoked and the instruction to complete all remaining required work.

- OpenCode: all four tasks checked, **28 tests passed**, **32 independent behavior
  cases passed**, checkpoint and README present, user-owned file unchanged.
- Codex: all four tasks checked, **12 tests passed**, **32 independent behavior
  cases passed**, checkpoint and README present, user-owned file unchanged.
- Installed skill files stayed unchanged in both fixtures.
- Standard `npx skills add . --list` discovered the packaged skill successfully.

## Reproduce

```bash
python3 scripts/create_smoke_project.py /tmp/hard-implementation-evaluation
python3 install.py --project /tmp/hard-implementation-evaluation
```

Start the desired agent from that fixture and invoke the documented skill/command,
requesting T001 plus a checkpoint and explicit stop. Then start a fresh session and
invoke it again, revoking the pause and requesting completion. Finally run:

```bash
python3 scripts/verify_smoke_project.py /tmp/hard-implementation-evaluation
```

The verifier runs **32 independent public-behavior cases**, checks all four task
boxes, the checkpoint, documentation, preservation of the user-owned file, the
agent-created test suite, and `git diff --check`. Agent claims alone are not used
as proof of completion.

## Limits

These are bounded local behavioral tests. They do not guarantee that every model,
feature, platform, or runtime will behave identically. The recovery scenario is a
user-requested pause followed by a fresh session, not a kill-at-every-instruction
crash test. Skills do not restart the host automatically or bypass quota/approvals.

The machine reported file-watcher exhaustion during initial runs; the OpenCode
resume run disabled its optional watcher for that process only. A first Codex
resume attempt was rejected before execution because the then-selected model was
not supported for the account. It was retried using the same `gpt-6-astra` model
that successfully ran the first stage, without editing global configuration.

The published GitHub Actions workflow also tests the package across Linux, Windows,
and macOS with Python 3.10 and 3.13. A workflow file alone is not evidence of a passed
remote run; consult the actual repository Actions results.

## Published distribution checks

The public v1.0.0 URL installed all eight expected files in a clean directory;
the full original workflow matched byte-for-byte. Initial CI found a development
generator ordering difference on Windows (case-insensitive Path sorting), not a
failed installation or changed payload. Version 1.0.1 sorts POSIX path strings and
writes deterministic LF bytes. The original workflow content is unchanged.

## Guided CLI release (1.1.0)

- All 28 package/CLI tests passed locally, including global installation with an
  isolated home/configuration directory, changed-file status reporting, scope
  selection, cancellation, JSON output, dry-run, and non-interactive safeguards.
- Built both wheel and source distribution with `uv build`.
- Installed from the wheel in a separate uv environment and initialized a clean
  project without a source-checkout argument. `hard status` reported version 1.1.0
  and verified Codex/OpenCode installation; resources came from the bundled package.
- A real terminal session exercised the arrow-key agent selection and confirmation,
  then completed installation. The numeric fallback and cancellation were also
  exercised in a terminal reporting `TERM=dumb`.
- The original workflow remains byte-for-byte unchanged. The earlier live-agent
  implementation/resume results apply to the preserved workflow; this CLI release
  did not repeat those paid model runs.

## Universal compatibility release (1.2.0)

- 41 local tests passed. Per-host installation lifecycle subcases cover all ten
  agent IDs in both project/global scope, with full original bytes in every native
  copy, idempotent setup, safe removal, unchanged user files, collision protection,
  and rollback across shared/native copies.
- Eight native-system fixture layouts map requirements, design, and queues without
  creating a Spec Kit scaffold. Conductor uses its embedded plan queue; Spec Kitty
  uses work packages; Superpowers resolves the linked approved Spec. Detection is
  read-only, does not select ambiguous targets, excludes archives/outside symlinks,
  and reports missing roles instead of claiming readiness.
- Markdown task inventories retain numbered tasks and Conductor in-progress status;
  Superpowers steps need no invented T001 names. Native lane/approval semantics
  remain the responsibility of the actual system tools and agent reconciliation.
- Built wheel/source distributions and exercised the wheel in an isolated uv
  environment with all ten agents selected. `hard status` verified the installation.
- A real terminal wizard selected all agents and completed setup. Custom
  multi-selection is covered by a CLI test.
- Hermes native `skills list` recognized the installed skill in an isolated
  `HERMES_HOME` profile, without a model call or real profile/trust modification.
- Command Code native `cmd skills list` recognized the complete installed project
  skill in an isolated workspace, without a model call.
- Upgrading a published v1.1.0 project installation to v1.2.0 with all ten hosts
  selected succeeded and passed status verification.
- Skill Creator validation passed with an isolated PyYAML dependency.
- The full original workflow remains byte-for-byte unchanged. The earlier live
  implementation/resume tests were performed for Codex/OpenCode before universal
  bindings; they are not evidence of end-to-end execution of every new integration.

Host paths and invocation methods were checked against primary documentation in
[COMPATIBILITY.md](COMPATIBILITY.md). Fixture/path validation does not establish
that every host version, custom schema, board transition, or multi-agent execution
will behave identically. Native approval, review, acceptance and remote-action
boundaries still apply.
