"""Regression checks for the stale facts that prompted the maintenance workflow."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_consistency as check
import sync_github_metadata as sync


class ConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        for name in check.repository_files(ROOT):
            source = ROOT / name
            if source.is_file():
                target = self.root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)

    def issues(self):
        return check.local_issues(self.root, check.facts(self.root))[0]

    def test_current_repository_and_full_file_inventory_are_consistent(self):
        data = check.facts(self.root)
        errors, names = check.local_issues(self.root, data)
        self.assertEqual(errors, [])
        self.assertIn("AGENTS.md", names)
        self.assertIn("skills/hard-implementation/references/security.md", names)
        self.assertEqual(len(data["agents"]), 10)
        self.assertEqual(len(data["systems"]), 8)

    def test_stale_skill_version_and_native_command_are_detected(self):
        path = self.root / "skills/hard-implementation/SKILL.md"
        text = path.read_text(encoding="utf-8").replace(
            f'version: "{check.project_version(self.root)}"', 'version: "0.0.0"')
        text = text.replace("| Pi | `/hard.implement` |", "| Pi | `/skill:hard-implementation` |")
        path.write_text(text, encoding="utf-8")
        errors = self.issues()
        self.assertTrue(any("Generated facts are stale" in e for e in errors))
        self.assertTrue(any("Stale invocation" in e and "pi" in e for e in errors))

    def test_stale_package_and_readme_versions_are_detected(self):
        for name in ("pyproject.toml", "README.ar.md"):
            path = self.root / name
            path.write_text(path.read_text(encoding="utf-8").replace(
                check.project_version(self.root), "0.0.0"), encoding="utf-8")
        errors = self.issues()
        self.assertTrue(any("pyproject.toml" in e for e in errors))
        self.assertTrue(any("README.ar.md" in e for e in errors))

    def test_broken_links_are_detected_in_unchanged_areas_and_space_paths(self):
        path = self.root / "docs/extra-review.md"
        path.write_text('[Missing](<missing reference.md>)\n\n```md\n[Example](fake.md)\n```\n', encoding="utf-8")
        errors = self.issues()
        self.assertTrue(any("missing reference.md" in e for e in errors))
        self.assertFalse(any("fake.md" in e for e in errors))

    def test_missing_security_payload_is_not_a_valid_complete_installation(self):
        path = self.root / "distribution.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["files"].pop("skills/hard-implementation/references/security.md")
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("Security Gate missing" in e for e in self.issues()))
        engine = check.load_engine(self.root)
        with tempfile.TemporaryDirectory() as target, self.assertRaisesRegex(ValueError, "Required workflow"):
            engine.install(Path(target), self.root, ["codex"])
            self.fail("Incomplete security resource must stop installation")

    def test_corrupted_security_gate_refuses_install_before_any_write(self):
        path = self.root / "skills/hard-implementation/references/security.md"
        path.write_text("changed security gate", encoding="utf-8")
        engine = check.load_engine(self.root)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            with self.assertRaisesRegex(ValueError, "Checksum mismatch"):
                engine.install(target, self.root, ["claude"])
            self.assertEqual(list(target.iterdir()), [])

    def test_old_about_and_topics_fail_against_generated_current_facts(self):
        data = check.facts(self.root)
        old = {"description": "Complete Spec Kit workflow for Codex and OpenCode", "topics": ["spec-kit", "codex"]}
        self.assertEqual(len(check.github_issues(data, old)), 2)
        current = {"description": data["description"], "topics": list(reversed(data["topics"]))}
        self.assertEqual(check.github_issues(data, current), [])

    def test_metadata_preview_does_not_write_to_github(self):
        with patch.object(sys, "argv", ["sync_github_metadata.py"]), \
             patch.object(sync.subprocess, "run") as remote, contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(sync.main(), 0)
        remote.assert_not_called()
        self.assertIn("Preview only", output.getvalue())

    def test_generation_excludes_original_and_historical_evidence(self):
        updates = check.generated_updates(self.root, check.facts(self.root))
        self.assertNotIn("skills/hard-implementation/references/workflow.md", updates)
        self.assertNotIn("CHANGELOG.md", updates)
        self.assertNotIn("docs/VALIDATION.md", updates)


if __name__ == "__main__":
    unittest.main()
