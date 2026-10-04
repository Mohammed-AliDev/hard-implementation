import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load("installer", ROOT / "install.py")
audit = load("audit", ROOT / "skills/hard-implementation/scripts/audit_tasks.py")


class PackageTests(unittest.TestCase):
    def test_original_preserved_byte_for_byte(self):
        raw = (ROOT / "skills/hard-implementation/references/workflow.md").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         "3302000990ac049cc068a63927dac29757be8bd8031bb3fb9d5d7c1c715035c7")

    def test_manifest_covers_entire_payload(self):
        data = json.loads((ROOT / "distribution.json").read_text())
        actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "skills").rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
        actual.update(p.relative_to(ROOT).as_posix() for p in (ROOT / "adapters").rglob("*")
                      if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
        self.assertEqual(set(data["files"]), actual)
        for path, sha in data["files"].items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), sha)

    def test_audit_handles_crlf_metadata_and_fences(self):
        text = "- [x] T001 Setup\r\n- [ ] T002 [P] [US1] Work\r\n```md\n- [ ] T999 Example\n```\n"
        result = audit.inventory(text)
        self.assertEqual(result["checked"], ["T001"])
        self.assertEqual(result["open"], ["T002"])
        self.assertEqual(result["errors"], [])

    def test_audit_never_treats_invalid_or_empty_as_complete(self):
        for text in ("", "- [ ] forgotten ID", "- [x] T001 A\n- [ ] T001 B", "```\n- [ ] T001 Hidden"):
            with self.subTest(text=text):
                self.assertTrue(audit.inventory(text)["errors"])


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)

    def install(self, agents=("codex", "opencode"), **kwargs):
        return installer.install(self.project, ROOT, agents, **kwargs)

    def test_install_both_repeat_and_uninstall_preserves_unrelated(self):
        unrelated = self.project / "user.txt"
        unrelated.write_text("keep")
        self.install()
        self.assertTrue((self.project / installer.COMMAND).exists())
        raw = self.project / (installer.DEST_PREFIX + "references/workflow.md")
        self.assertEqual(raw.read_bytes(), (ROOT / (installer.SKILL_PREFIX + "references/workflow.md")).read_bytes())
        self.assertEqual(self.install()["write"], [])
        extra = raw.parent / "user-notes.md"
        extra.write_text("keep too")
        self.install(uninstall=True)
        self.assertFalse(raw.exists())
        self.assertEqual(extra.read_text(), "keep too")
        self.assertEqual(unrelated.read_text(), "keep")

    def test_codex_only_then_add_opencode(self):
        self.install(("codex",))
        self.assertFalse((self.project / installer.COMMAND).exists())
        self.install(("opencode",))
        self.assertTrue((self.project / installer.COMMAND).exists())
        self.assertEqual(installer.load_state(self.project)["agents"], ["codex", "opencode"])

    def test_dry_run_writes_nothing(self):
        self.assertTrue(self.install(dry_run=True)["write"])
        self.assertEqual(list(self.project.iterdir()), [])

    def test_record_parent_collision_fails_before_any_write(self):
        (self.project / ".hard-implementation").write_text("user content")
        with self.assertRaisesRegex(ValueError, "not a directory"):
            self.install()
        self.assertFalse((self.project / ".agents").exists())

    def test_corrupted_payload_fails_before_any_write(self):
        actual_read = installer.read_source
        def corrupt(source, name):
            data = actual_read(source, name)
            return data + b"altered" if name.endswith("workflow.md") else data
        with patch.object(installer, "read_source", side_effect=corrupt):
            with self.assertRaisesRegex(ValueError, "Checksum mismatch"):
                self.install()
        self.assertEqual(list(self.project.iterdir()), [])

    def test_write_failure_rolls_back(self):
        actual_write = installer.atomic_write
        calls = 0
        def fail_once(path, data):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("simulated disk error")
            return actual_write(path, data)
        with patch.object(installer, "atomic_write", side_effect=fail_once):
            with self.assertRaisesRegex(OSError, "simulated"):
                self.install()
        self.assertEqual([p for p in self.project.rglob("*") if p.is_file()], [])

    def test_collision_fails_before_any_write(self):
        command = self.project / installer.COMMAND
        command.parent.mkdir(parents=True)
        command.write_text("user's own command")
        with self.assertRaisesRegex(ValueError, "unowned"):
            self.install()
        self.assertFalse((self.project / ".agents").exists())
        self.assertEqual(command.read_text(), "user's own command")

    def test_edited_managed_file_blocks_update_and_uninstall(self):
        self.install()
        skill = self.project / (installer.DEST_PREFIX + "SKILL.md")
        skill.write_text("local edits")
        for remove in (False, True):
            with self.subTest(remove=remove), self.assertRaisesRegex(ValueError, "modified"):
                self.install(uninstall=remove)
        self.assertEqual(skill.read_text(), "local edits")
        self.assertTrue((self.project / installer.COMMAND).exists())

    def test_identical_preexisting_file_is_not_claimed(self):
        target = self.project / installer.COMMAND
        target.parent.mkdir(parents=True)
        target.write_bytes((ROOT / installer.ADAPTER).read_bytes())
        self.install()
        self.assertNotIn(installer.COMMAND, installer.load_state(self.project)["files"])
        self.install(uninstall=True)
        self.assertTrue(target.exists())

    def test_symlink_destination_is_rejected(self):
        outside = self.project / "outside"
        outside.mkdir()
        try:
            (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("Symlinks unavailable on this platform")
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_tampered_state_cannot_delete_unrelated_files(self):
        target = self.project / "user.txt"
        target.write_text("keep")
        state = self.project / installer.STATE
        state.parent.mkdir()
        state.write_text(json.dumps({"package": "hard-implementation", "agents": [],
                                     "files": {"user.txt": installer.digest(b"keep")}}))
        with self.assertRaisesRegex(ValueError, "Invalid managed"):
            self.install(uninstall=True)
        self.assertEqual(target.read_text(), "keep")

    def test_reject_path_traversal(self):
        for name in ("../x", "/tmp/x", "a/../../x", "a\\b", "C:/x", "a//b"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                installer.safe_path(self.project, name)

    def test_missing_managed_file_can_be_repaired(self):
        self.install()
        target = self.project / installer.COMMAND
        target.unlink()
        self.install()
        self.assertTrue(target.exists())


if __name__ == "__main__":
    unittest.main()
