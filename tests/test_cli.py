import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
try:
    from rich.console import Console
    from hard_implementation import cli
except ImportError:
    cli = None


@unittest.skipIf(cli is None, "CLI dependencies not installed; use uv run python -m unittest discover -s tests -v")
class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = io.StringIO()
        self.console = Console(file=self.output, width=80, color_system=None)

    def run_cli(self, args):
        return cli.main(args, console=self.console)

    def test_project_setup_has_usable_next_steps_and_verified_status(self):
        project = self.root / "new project"
        result = self.run_cli(["init", str(project), "--agent", "both", "--yes", "--source", str(ROOT)])
        self.assertEqual(result, 0)
        self.assertIn("Ready to use", self.output.getvalue())
        self.assertIn("$hard-implementation", self.output.getvalue())
        self.assertIn("/hard.implement", self.output.getvalue())
        self.assertNotIn("specs/your-feature", self.output.getvalue())
        self.assertTrue((project / ".opencode/commands/hard.implement.md").is_file())
        self.assertEqual(self.run_cli(["status", str(project)]), 0)
        self.assertIn("Verified", self.output.getvalue())

    def test_wizard_routes_selected_agent_and_scope(self):
        project = self.root / "project"
        project.mkdir()
        with patch.object(cli.sys.stdin, "isatty", return_value=True), \
             patch.object(cli.sys.stdout, "isatty", return_value=True), \
             patch.object(cli.Path, "cwd", return_value=project), \
             patch.object(cli, "choose", side_effect=["codex", "project"]) as picker, \
             patch.object(cli.questionary, "confirm") as confirm:
            confirm.return_value.ask.return_value = True
            self.assertEqual(self.run_cli(["init", "--source", str(ROOT)]), 0)
        self.assertEqual(picker.call_count, 2)
        self.assertTrue((project / ".agents/skills/hard-implementation/SKILL.md").is_file())
        self.assertFalse((project / ".opencode").exists())

    def test_declining_wizard_writes_nothing(self):
        with patch.object(cli.sys.stdin, "isatty", return_value=True), \
             patch.object(cli.sys.stdout, "isatty", return_value=True), \
             patch.object(cli.questionary, "confirm") as confirm:
            confirm.return_value.ask.return_value = False
            self.assertEqual(self.run_cli(["init", str(self.root), "--agent", "both", "--source", str(ROOT)]), 0)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_noninteractive_missing_choices_does_not_install(self):
        with patch.object(cli.sys.stdin, "isatty", return_value=False):
            self.assertEqual(self.run_cli(["init", str(self.root)]), 1)
        self.assertIn("--agent", self.output.getvalue())
        self.assertEqual(list(self.root.iterdir()), [])

    def test_dry_run_new_directory_is_read_only(self):
        project = self.root / "new"
        self.assertEqual(self.run_cli(["init", str(project), "--agent", "both", "--dry-run"]), 0)
        self.assertFalse(project.exists())

    def test_global_install_uses_native_paths_and_absolute_fallback(self):
        config = self.root / "custom configuration"
        with patch.object(cli.Path, "home", return_value=self.root), \
             patch.dict(cli.os.environ, {"XDG_CONFIG_HOME": str(config)}):
            self.assertEqual(self.run_cli(["init", "--global", "--agent", "both", "--yes", "--source", str(ROOT)]), 0)
            command = config / "opencode/commands/hard.implement.md"
            self.assertTrue(command.is_file())
            self.assertIn(str(self.root / ".agents/skills/hard-implementation/SKILL.md"), command.read_text())
            self.assertEqual(self.run_cli(["status", "--global"]), 0)
            self.assertEqual(self.run_cli(["uninstall", "--global", "--yes"]), 0)
            self.assertFalse(command.exists())
        self.assertFalse((self.root / ".opencode").exists())

    def test_global_record_and_project_record_are_separate(self):
        with patch.object(cli.Path, "home", return_value=self.root), patch.dict(cli.os.environ, {}, clear=True):
            self.assertEqual(self.run_cli(["init", str(self.root), "--agent", "codex", "--yes", "--source", str(ROOT)]), 0)
            # A different project path would normally be used; identical global
            # files are shared without transferring ownership of pre-existing files.
            self.assertEqual(self.run_cli(["init", "--global", "--agent", "opencode", "--yes", "--source", str(ROOT)]), 0)
            self.assertTrue((self.root / ".hard-implementation/install.json").is_file())
            self.assertTrue((self.root / ".hard-implementation/global-install.json").is_file())

    def test_status_reports_modified_managed_file(self):
        self.run_cli(["init", str(self.root), "--agent", "codex", "--yes", "--source", str(ROOT)])
        (self.root / ".agents/skills/hard-implementation/SKILL.md").write_text("local edit")
        self.assertEqual(self.run_cli(["status", str(self.root)]), 1)
        self.assertIn("Needs attention", self.output.getvalue())

    def test_json_mode_has_no_banner_and_is_parseable(self):
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            result = self.run_cli(["init", str(self.root), "--agent", "codex", "--yes", "--json", "--source", str(ROOT)])
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(capture.getvalue())["scope"], "project")
        self.assertEqual(self.output.getvalue(), "")

    def test_global_changed_configuration_path_does_not_delete_old_files(self):
        original_config = self.root / "original"
        changed_config = self.root / "changed"
        with patch.object(cli.Path, "home", return_value=self.root):
            with patch.dict(cli.os.environ, {"XDG_CONFIG_HOME": str(original_config)}):
                self.assertEqual(self.run_cli(["init", "--global", "--agent", "opencode", "--yes", "--source", str(ROOT)]), 0)
            with patch.dict(cli.os.environ, {"XDG_CONFIG_HOME": str(changed_config)}):
                self.assertEqual(self.run_cli(["uninstall", "--global", "--yes"]), 1)
        self.assertTrue((original_config / "opencode/commands/hard.implement.md").exists())
        self.assertFalse(changed_config.exists())


if __name__ == "__main__":
    unittest.main()
