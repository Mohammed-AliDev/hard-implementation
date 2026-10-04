# Keeping package facts current

Every substantive update requires a full repository review, including GitHub About.
[AGENTS.md](../AGENTS.md) records this requirement for future coding sessions.

The installer registry owns supported agents and native invocation strings.
`src/hard_implementation/__init__.py` supplies the release version for documentation
and distribution generation; the static installer and pyproject versions must match.
[project-metadata.json](../project-metadata.json) records specification systems and
topic assignments. [CURRENT-STATE.md](CURRENT-STATE.md) is the generated snapshot.

After changing behavior/facts and updating both README languages:

```bash
uv sync
python scripts/check_consistency.py --write
python scripts/check_consistency.py
uv run python -m unittest discover -s tests -v
uv build
git diff --check
```

`--write` regenerates command tables in both READMEs and SKILL.md, current release
facts, README installation links, skill version metadata and distribution hashes.
It never rewrites the original workflow, old changelog entries or historical test
results. The default check reads repository files, verifies local Markdown links,
command tables, release versions, payload coverage/hashes and supported-system claims.
It cannot establish every prose statement or external tool capability; review those
against the implementation and relevant primary documentation.

When the user has authorized GitHub publication, preview and then apply About:

```bash
python scripts/sync_github_metadata.py
python scripts/sync_github_metadata.py --apply
python scripts/check_consistency.py --github
```

Preview is read-only. `--apply` changes the repository description and full topic
list, then verifies the result. It does not create a release, push code, alter a
homepage, change visibility, modify branch rules or choose a model. It requires
authenticated `gh` access with permission to edit that repository. GitHub Actions
checks About read-only against the same facts; its built-in token is not used to
edit repository metadata. About must be synchronized before publishing a change
whose metadata differs, so the new CI check sees matching public facts.

Keep actual live test records dated and scoped. Historical versions in the
changelog/validation guide and Spec Kit names in the preserved original are valid
history; current installation instructions and generated metadata must match the
latest release. Add security coverage through [security.md](../skills/hard-implementation/references/security.md)
and keep its applicability/evidence rules linked from the loading entrypoint.

## Terminal branding

The lion, HARD wordmark and ALAEEB signature are rendered by
`src/hard_implementation/branding.py` using Rich text and terminal half blocks.
No image protocol, animation, raster dependency or external asset is required at runtime.
Wide color terminals use a side-by-side layout; medium terminals center the lion;
small, monochrome and legacy-encoding output use compact ASCII/plain branding.
JSON output remains undecorated. The consistency check detects a stale preview
version. Preview the actual renderer after visual changes:

```bash
uv run python scripts/preview_banner.py docs/assets/banner.svg
uv run python scripts/preview_banner.py /tmp/hard-banner-light.svg --theme light
uv run python scripts/preview_banner.py /tmp/hard-banner-medium.svg --width 60
```

Regenerate the README preview when its version or renderer changes. Inspect both
background themes and narrow layouts, and verify the installed package's rendering.
