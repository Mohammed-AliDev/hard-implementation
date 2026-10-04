import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

engine = load('universal_installer', 'install.py')
discovery = load('discovery', 'skills/hard-implementation/scripts/discover_system.py')
audit = load('universal_audit', 'skills/hard-implementation/scripts/audit_tasks.py')

class UniversalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, body='Existing approved artifact\n'):
        file = self.root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(body, encoding='utf-8')
        return file

    def test_eight_native_systems_keep_artifact_roles_and_are_read_only(self):
        layouts = {
            'Spec Kit': ('specs/001-a', ['spec.md', 'plan.md', 'tasks.md']),
            'Kiro Specs': ('.kiro/specs/b', ['requirements.md', 'design.md', 'tasks.md']),
            'cc-sdd': ('.kiro/specs/c', ['requirements.md', 'design.md', 'tasks.md', 'spec.json']),
            'Spec Workflow MCP': ('.spec-workflow/specs/d', ['requirements.md', 'design.md', 'tasks.md']),
            'OpenSpec': ('openspec/changes/e', ['proposal.md', 'specs/ui/spec.md', 'tasks.md']),
            'Spec Kitty': ('kitty-specs/001-f', ['spec.md', 'plan.md', 'tasks/WP01-core.md']),
            'Conductor': ('conductor/tracks/g', ['spec.md', 'plan.md', 'metadata.json']),
        }
        for _, (folder, names) in layouts.items():
            for name in names:
                self.write(folder + '/' + name)
        self.write('docs/superpowers/specs/h.md')
        self.write('docs/superpowers/plans/h.md', '# H Implementation Plan\n**Spec:** docs/superpowers/specs/h.md\n### Task 1: Work\n- [ ] Write tests\n')
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = discovery.discover(self.root)
        items = {c['system']: c for c in result['candidates']}
        self.assertEqual(set(items), set(layouts) | {'Superpowers'})
        self.assertTrue(all(c['ready'] for c in items.values()))
        self.assertEqual(items['Conductor']['queue'], ['conductor/tracks/g/plan.md'])
        self.assertEqual(items['Spec Kitty']['queue'], ['kitty-specs/001-f/tasks/WP01-core.md'])
        self.assertEqual(items['Superpowers']['requirements'], ['docs/superpowers/specs/h.md'])
        self.assertIsNone(result['selected'])
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_partial_spec_and_archive_are_not_reported_as_ready(self):
        self.write('openspec/changes/archive/old/tasks.md')
        self.write('specs/new/tasks.md')
        result = discovery.discover(self.root)
        self.assertEqual(len(result['candidates']), 1)
        self.assertFalse(result['candidates'][0]['ready'])
        self.assertIn('requirements', result['candidates'][0]['missing'])

    def test_outside_symlink_is_not_a_candidate(self):
        with tempfile.TemporaryDirectory() as outside:
            p = Path(outside) / 'plan.md'
            p.write_text('# Escaped Implementation Plan\n')
            folder = self.root / 'docs/plans'
            folder.mkdir(parents=True)
            try:
                (folder / 'escape.md').symlink_to(p)
            except OSError:
                self.skipTest('Symlinks unavailable')
            self.assertEqual(discovery.discover(self.root)['candidates'], [])

    def test_superpowers_relative_markdown_spec_link(self):
        self.write('docs/superpowers/specs/design.md')
        self.write('docs/superpowers/plans/work.md', '# Implementation Plan\n**Spec:** [Approved](../specs/design.md)\n### Task 1: Work\n')
        item = discovery.discover(self.root)['candidates'][0]
        self.assertEqual(item['requirements'], ['docs/superpowers/specs/design.md'])

    def test_markdown_queue_preserves_numbered_tasks_and_in_progress(self):
        result = audit.inventory('- [x] 1.1 Tests\n- [~] 1.2 Implementation\n- [ ] 2.* Optional\n', 'markdown')
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['checked'], ['1.1'])
        self.assertEqual(result['in_progress'], ['1.2'])
        self.assertEqual(len(result['open']), 2)
        self.assertEqual(audit.inventory('', 'markdown')['total'], 0)
        self.assertTrue(audit.inventory('', 'markdown')['errors'])

    def test_superpowers_checkbox_steps_are_inventoried_without_rewriting_ids(self):
        result = audit.inventory('### Task 1: Core\n- [x] Write failing test\n- [ ] Run it\n```md\n- [ ] Example\n```\n', 'markdown')
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['total'], 2)
        self.assertEqual(result['tasks'][0]['label'], 'Write failing test')

    def test_each_host_installs_full_workflow_and_uninstalls_without_user_file_loss(self):
        original = (ROOT / 'skills/hard-implementation/references/workflow.md').read_bytes()
        for scope in ('project', 'global'):
            for agent in engine.AGENTS:
                with self.subTest(scope=scope, agent=agent), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp).resolve()
                    user = root / 'user.txt'; user.write_text('keep')
                    engine.install(root, ROOT, [agent], scope=scope)
                    for prefix in engine.skill_prefixes([agent], scope):
                        self.assertEqual((root / prefix / 'references/workflow.md').read_bytes(), original)
                        self.assertTrue((root / prefix / 'references/systems.md').is_file())
                        self.assertTrue((root / prefix / 'references/security.md').is_file())
                    self.assertEqual(engine.install(root, ROOT, [agent], scope=scope)['write'], [])
                    engine.install(root, ROOT, [agent], scope=scope, uninstall=True)
                    self.assertEqual(user.read_text(), 'keep')
                    self.assertEqual([p for p in root.rglob('*') if p.is_file()], [user])

    def test_global_hermes_profile_is_respected_and_path_change_is_protected(self):
        home = self.root / 'home'; home.mkdir()
        profile = self.root / 'profile'
        engine.install(home, ROOT, ['hermes'], scope='global', hermes_home=profile)
        workflow = profile / 'skills/hard-implementation/references/workflow.md'
        self.assertTrue(workflow.exists())
        with self.assertRaisesRegex(ValueError, 'location changed'):
            engine.install(home, ROOT, ['hermes'], scope='global', hermes_home=self.root / 'another', uninstall=True)
        self.assertTrue(workflow.exists())
        engine.install(home, ROOT, ['hermes'], scope='global', hermes_home=profile, uninstall=True)
        self.assertFalse(workflow.exists())

    def test_native_collision_protects_all_destinations_before_writing(self):
        custom = self.write('.zcode/skills/hard-implementation/SKILL.md', 'user custom skill')
        with self.assertRaisesRegex(ValueError, 'unowned'):
            engine.install(self.root, ROOT, list(engine.AGENTS))
        self.assertEqual(custom.read_text(), 'user custom skill')
        self.assertFalse((self.root / '.agents').exists())

    def test_failure_rolls_back_shared_and_native_copies(self):
        actual = engine.atomic_write
        calls = 0
        def fail(path, data):
            nonlocal calls
            calls += 1
            if calls == 14:
                raise OSError('simulated native-copy failure')
            actual(path, data)
        with patch.object(engine, 'atomic_write', side_effect=fail), self.assertRaises(OSError):
            engine.install(self.root, ROOT, list(engine.AGENTS), scope='global')
        self.assertEqual([p for p in self.root.rglob('*') if p.is_file()], [])

if __name__ == '__main__':
    unittest.main()
