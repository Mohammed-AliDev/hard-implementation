"""Command installation, upgrade, and ownership across native host locations."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("commands_engine", ROOT / "install.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hard command test ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def test_each_native_command_resolves_the_complete_canonical_skill(self):
        for scope in ("project", "global"):
            with self.subTest(scope=scope):
                root = self.root / scope; root.mkdir()
                result = engine.install(root, ROOT, list(engine.AGENTS), scope=scope)
                for agent, (_, target) in engine.COMMAND_ADAPTERS.items():
                    text = engine.destination(root, target, scope).read_text(encoding="utf-8")
                    self.assertNotIn("{{HARD_SKILL_PATH}}", text)
                    expected = (root / engine.DEST_PREFIX / "SKILL.md").as_posix() if scope == "global" else engine.DEST_PREFIX + "SKILL.md"
                    self.assertIn(expected, text.replace("\\\\", "/").replace("\\", "/"))
                    self.assertIn("complete original workflow", text)
                    self.assertIn("references/systems.md", text)
                    self.assertIn("$ARGUMENTS", text) if agent != "vscode" else self.assertNotIn("$ARGUMENTS", text)
                self.assertEqual(engine.install(root, ROOT, list(engine.AGENTS), scope=scope)["write"], [])
                self.assertEqual(len([n for n in result["destinations"] if n in engine.COMMAND_NAMES]), 5)

    def test_existing_command_conflict_prevents_all_writes(self):
        target = engine.COMMAND_ADAPTERS["claude"][1]
        path = self.root / target; path.parent.mkdir(parents=True)
        path.write_text("my existing command")
        with self.assertRaisesRegex(ValueError, "unowned"):
            engine.install(self.root, ROOT, ["claude", "pi"])
        self.assertEqual(path.read_text(), "my existing command")
        self.assertFalse((self.root / engine.STATE).exists())
        self.assertFalse((self.root / ".agents").exists())

    def test_identical_preexisting_command_is_never_claimed_or_removed(self):
        target = engine.COMMAND_ADAPTERS["pi"][1]
        desired = engine.payload(ROOT, ["pi"])[target].replace(
            b"{{HARD_SKILL_PATH}}", json.dumps(engine.DEST_PREFIX + "SKILL.md").encode())
        path = self.root / target; path.parent.mkdir(parents=True); path.write_bytes(desired)
        engine.install(self.root, ROOT, ["pi"])
        self.assertNotIn(target, engine.load_state(self.root)["files"])
        engine.install(self.root, ROOT, [], uninstall=True)
        self.assertEqual(path.read_bytes(), desired)

    def test_old_installation_gets_commands_without_replacing_workflow(self):
        engine.install(self.root, ROOT, list(engine.AGENTS))
        state = engine.load_state(self.root)
        new_commands = engine.COMMAND_NAMES - {engine.COMMAND}
        for name in new_commands:
            (self.root / name).unlink()
            state["files"].pop(name)
            state["external_paths"].pop(name)
        state["version"] = "1.2.0"
        (self.root / engine.STATE).write_text(json.dumps(state))
        original = self.root / engine.DEST_PREFIX / "references/workflow.md"
        before = original.read_bytes()
        result = engine.install(self.root, ROOT, ["codex"])
        self.assertEqual(set(result["write"]), new_commands)
        self.assertEqual(original.read_bytes(), before)
        self.assertEqual(set(result["agents"]), set(engine.AGENTS))

    def test_global_vscode_locations_match_default_profiles(self):
        for platform, relative in (
            ("linux", ".config/Code/User/prompts/hard.implement.prompt.md"),
            ("darwin", "Library/Application Support/Code/User/prompts/hard.implement.prompt.md"),
            ("win32", "AppData/Roaming/Code/User/prompts/hard.implement.prompt.md"),
        ):
            with self.subTest(platform=platform), patch.object(engine.sys, "platform", platform):
                self.assertEqual(engine.destination(self.root, engine.VSCODE_COMMAND, "global"), self.root / relative)
        self.assertEqual(engine.destination(self.root, engine.PI_COMMAND, "global"),
                         self.root / ".pi/agent/prompts/hard.implement.md")

    def test_changed_global_vscode_config_location_is_protected(self):
        with patch.object(engine.sys, "platform", "linux"):
            first = self.root / "config one"
            engine.install(self.root, ROOT, ["vscode"], scope="global", config_home=first)
            with self.assertRaisesRegex(ValueError, "location changed"):
                engine.install(self.root, ROOT, [], uninstall=True, scope="global", config_home=self.root / "config two")
            self.assertTrue((first / "Code/User/prompts/hard.implement.prompt.md").is_file())

    def test_removal_preserves_modified_native_command(self):
        engine.install(self.root, ROOT, ["commandcode"])
        target = self.root / engine.COMMAND_ADAPTERS["commandcode"][1]
        target.write_text("user edits")
        with self.assertRaisesRegex(ValueError, "modified"):
            engine.install(self.root, ROOT, [], uninstall=True)
        self.assertEqual(target.read_text(), "user edits")
        self.assertTrue((self.root / engine.DEST_PREFIX / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
