# Maintaining Hard Implementation

This repository packages the author's complete universal implementation skill.
These instructions govern package maintenance, documentation and release metadata.

## Preserve the original and scope

- Keep `skills/hard-implementation/references/workflow.md` byte-for-byte unchanged.
  Its historical Spec Kit wording is intentional; add host/system/security bindings
  through the entrypoint and companion references. Do not shorten original sections.
- Keep compatibility claims accurate: installer/fixture support is distinct from
  live model execution. Do not fabricate independent review, security scores,
  certifications, tests, host command support or board approvals.
- Work in this repository, not an unrelated parent Git checkout. Protect user edits
  and installer ownership records. Remote publication needs the user's authorization.

## After every substantive change

1. Review **all repository files** for affected facts, not only the diff: package
   versions, supported agents/systems, native commands and paths, loading references,
   examples, CLI help/output, metadata, README translations and validation limits.
   Use `git ls-files` and focused `rg` searches to inspect the full file inventory.
2. Update canonical facts: the agent registry/command adapters in `install.py`,
   package version in `src/hard_implementation/__init__.py`, matching installer/
   pyproject versions, and `project-metadata.json` for systems/topics. Update native
   compatibility explanations and actual implementation together.
3. Run `python scripts/check_consistency.py --write` to regenerate command tables,
   current release facts, README version links and distribution hashes. Inspect the
   generated changes; the script does not judge every prose claim or host capability.
   When the version or terminal renderer changes, regenerate `docs/assets/banner.svg`
   with `uv run python scripts/preview_banner.py docs/assets/banner.svg` and inspect
   dark/light and narrow previews as described in the maintenance guide.
   After changing lion source artwork, run `uv run --with pillow python
   scripts/build_lion_art.py` and preserve its source/prompt provenance.
4. Run the consistency check, relevant package tests, skill validation when its
   instructions change, and distribution builds when packaged files change.
   Fix drift instead of suppressing a check or deleting accurate historical evidence.
5. Preserve old changelog entries and dated validation results as history. State
   which new behavior was actually tested. Review release notes for the final scope.
6. When remote updates are authorized, synchronize GitHub About/description/topics
   using `python scripts/sync_github_metadata.py --apply`, then verify with
   `python scripts/check_consistency.py --github`. About is repository metadata,
   not a file updated by `git push`. Confirm CI and the published release/tag/assets.

This review is required without waiting for the user to identify stale information.
The automated checks cover common drift; manual full-file review remains necessary.
