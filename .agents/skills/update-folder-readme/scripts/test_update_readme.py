"""Isolated filesystem tests; never operates on repository READMEs."""
import os
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import update_readme as helper

NAME = 'README-B_G11_T2_PA.md'


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.folder = self.root / 'content'
        self.folder.mkdir()
        self.target = self.folder / NAME
        self.target.write_bytes(b'# Directory Summary\n')
        template = self.root / helper.TEMPLATE
        template.parent.mkdir(parents=True)
        template.write_bytes(b'live template')
        self.time = 1_700_000_000_123_456_700
        os.utime(self.target, ns=(self.time, self.time))
        self.time = self.target.stat().st_mtime_ns

    def source(self, name, offset=0):
        p = self.folder / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b'source contents')
        os.utime(p, ns=(self.time + offset, self.time + offset))
        return p

    def prepare(self):
        return helper.prepare(self.root, NAME)

    def test_strict_cutoff_and_no_unchanged_reads_or_hashes(self):
        equal = self.source('equal.tex')
        older = self.source('older.tex', -100)
        newer = self.source('newer.tex', 100)
        self.source('ignored.pdf', 100)
        self.source('child/README.md', 100)
        self.source('child/deep.tex', 100)
        original = Path.read_bytes
        def guarded(path):
            if path in (equal, older):
                raise AssertionError('Unchanged source content opened')
            return original(path)
        with patch.object(Path, 'read_bytes', guarded):
            state = self.prepare()
            self.assertEqual(state['cutoff_ns'], self.time)
            self.assertEqual(set(state['eligible']),
                             {'content/newer.tex', 'content/child/README.md'})
            with self.assertRaisesRegex(ValueError, 'Read denied'):
                helper.read_input(state, 'content/equal.tex')
            self.assertEqual(helper.read_input(state, 'content/newer.tex'), newer.read_bytes())
            before = self.target.stat().st_mtime_ns
            data = self.target.read_bytes()
            self.assertEqual(helper.commit(state, data), 'already current')
            self.assertEqual(self.target.read_bytes(), data)
            self.assertEqual(self.target.stat().st_mtime_ns, before)

    def test_discovery_untracked_ambiguity_exclusions_and_root(self):
        self.assertEqual(helper.root_from(self.folder), self.root)
        for directory in ('build', '.cache', 'node_modules'):
            p = self.root / directory / NAME
            p.parent.mkdir()
            p.write_text('ignored')
        self.assertEqual(helper.discover(self.root, NAME), ['content/' + NAME])
        second = self.root / 'other' / NAME
        second.parent.mkdir()
        second.write_text('another untracked match')
        with self.assertRaisesRegex(ValueError, 'Multiple exact matches') as error:
            self.prepare()
        self.assertIn('other/' + NAME, str(error.exception))
        self.assertEqual(helper.prepare(self.root, NAME, 'content/' + NAME)['target'],
                         'content/' + NAME)
        with self.assertRaisesRegex(ValueError, 'No exact match'):
            helper.prepare(self.root, 'README-W_G10_T3_ER.md')
        for bad in ('../' + NAME, NAME + '\n', 'notes.txt', 'notes.pdf',
                    r'content\notes.md', '/notes.md', 'C:notes.md',
                    'notes.md/other.md', 'notes?.md', 'notes*.md',
                    'notes\x00.md', '.md', '.markdown', ''):
            with self.assertRaises(ValueError):
                helper.prepare(self.root, bad)

    def test_coded_and_nonstandard_names_are_exact_untracked_targets(self):
        for name in (NAME, 'template_README.md', 'README.md',
                     'README-B_G12_T2_PA.md', 'folder notes.md', 'guide.MD',
                     'summary.markdown', '-notes.md'):
            with self.subTest(name=name):
                self.target = self.target.rename(self.folder / name)
                rel = 'content/' + name
                state = helper.prepare(self.root, name, rel)
                self.assertEqual(state['target'], rel)
                self.assertIn(rel, state['inventory'])
                self.assertNotIn(rel, state['eligible'])
                self.assertEqual(helper.read_input(state, rel), self.target.read_bytes())
                self.assertEqual(helper.commit(state, ('# Directory Summary\n' + name).encode()),
                                 'updated')

    def test_nonstandard_missing_ambiguous_and_invalid_selection(self):
        name = 'directory_notes.md'
        with self.assertRaisesRegex(ValueError, 'No exact match'):
            helper.prepare(self.root, name)
        self.assertEqual(list(self.root.rglob(name)), [])
        self.target = self.target.rename(self.folder / name)
        second = self.root / 'unrelated' / name
        second.parent.mkdir()
        second.write_bytes(b'another summary')
        with self.assertRaisesRegex(ValueError, 'Multiple exact matches') as error:
            helper.prepare(self.root, name)
        self.assertIn('content/' + name, str(error.exception))
        self.assertIn('unrelated/' + name, str(error.exception))
        self.assertEqual(helper.prepare(self.root, name, 'unrelated/' + name)['target'],
                         'unrelated/' + name)
        with self.assertRaisesRegex(ValueError, 'Selection is not'):
            helper.prepare(self.root, name, 'elsewhere/' + name)

    def test_cli_rejects_extra_arguments_and_paths_without_state(self):
        state_path = self.root / 'state.json'
        for arguments in ([NAME, 'extra.md'], ['../' + NAME], ['content\\' + NAME],
                          ['notes.txt']):
            with self.subTest(arguments=arguments):
                result = subprocess.run(
                    [sys.executable, '-B', str(Path(helper.__file__).resolve()), 'prepare',
                     *arguments, '--state', str(state_path)], cwd=self.root,
                    capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(state_path.exists())

    def test_nonstandard_strict_boundary_and_child_scope(self):
        self.target = self.target.rename(self.folder / 'summary.md')
        # Use a full tick on filesystems with 100 ns precision.
        for name, offset in (('old.md', -100), ('equal.md', 0), ('new.md', 100),
                             ('child/README.md', 100),
                             ('child/README-topic.md', 100),
                             ('child/template_README.md', 100),
                             ('child/deep/README.md', 100),
                             ('child/source.tex', 100)):
            self.source(name, offset)
        state = helper.prepare(self.root, 'summary.md')
        self.assertEqual(state['cutoff_ns'], self.time)
        self.assertEqual(set(state['eligible']),
                         {'content/new.md', 'content/child/README.md',
                          'content/child/README-topic.md'})
        self.assertNotIn('content/child/template_README.md', state['inventory'])
        for rel in ('content/old.md', 'content/equal.md',
                    'content/child/template_README.md', 'content/child/source.tex',
                    'content/child/deep/README.md'):
            with self.assertRaisesRegex(ValueError, 'Read denied'):
                helper.read_input(state, rel)

    def test_template_control_is_not_a_newer_source(self):
        self.target = self.root / helper.TEMPLATE
        summary = self.target.parent / 'summary.md'
        summary.write_bytes(b'# Directory Summary\n')
        os.utime(summary, ns=(self.time, self.time))
        state = helper.prepare(self.root, 'summary.md')
        self.assertNotIn(helper.TEMPLATE, state['eligible'])
        self.assertIn(helper.TEMPLATE, state['controls'])
        helper.read_input(state, helper.TEMPLATE)
        self.assertNotIn(helper.TEMPLATE, state['reviewed'])

    def template_target(self):
        self.target = self.root / helper.TEMPLATE
        prefix = (b'# Folder README Template\r\n\r\n## Instructions for the AI\r\n'
                  b'Preserve these rules.\r\n\r\n## Output Template\r\n\r\n')
        self.target.write_bytes(prefix + b'# Directory Summary\r\nold summary\r\n')
        os.utime(self.target, ns=(self.time, self.time))
        return prefix

    def test_template_target_deduplicates_and_preserves_rules(self):
        prefix = self.template_target()
        original = Path.read_bytes
        reads = []
        def counted(path):
            reads.append(path)
            return original(path)
        with patch.object(Path, 'read_bytes', counted):
            state = helper.prepare(self.root, self.target.name)
        self.assertEqual(reads.count(self.target), 1)
        self.assertEqual(list(state['controls']), [helper.TEMPLATE])
        self.assertNotIn(helper.TEMPLATE, state['eligible'])
        self.assertEqual(state['cutoff_ns'], self.time)
        helper.read_input(state, helper.TEMPLATE)
        self.assertEqual(state['reviewed'], {})
        for invalid in (b'# Directory Summary\nLost rules\n',
                        prefix.replace(b'Preserve', b'Rewrite') + b'# Directory Summary\n',
                        prefix + b'# Other heading\n'):
            with self.assertRaisesRegex(ValueError, 'Preserve live template'):
                helper.commit(state, invalid)
        proposed = prefix + b'# Directory Summary\nnew summary\n'
        self.assertEqual(helper.commit(state, proposed), 'updated')
        self.assertEqual(self.target.read_bytes(), proposed)
        before = helper.signature(self.target)
        self.assertEqual(helper.commit(helper.prepare(self.root, self.target.name),
                                       proposed), 'already current')
        self.assertEqual(helper.signature(self.target), before)

    def test_template_missing_boundary_stops_without_writing(self):
        target = self.root / helper.TEMPLATE
        before = helper.signature(target)
        with self.assertRaisesRegex(ValueError, 'boundary'):
            helper.prepare(self.root, target.name)
        self.assertEqual(helper.signature(target), before)

    def test_template_concurrent_edit_stops(self):
        prefix = self.template_target()
        state = helper.prepare(self.root, self.target.name)
        self.target.write_bytes(prefix + b'# Directory Summary\nconcurrent\n')
        expected = self.target.read_bytes()
        with self.assertRaisesRegex(ValueError, 'Concurrent'):
            helper.commit(state, prefix + b'# Directory Summary\nstale\n')
        self.assertEqual(self.target.read_bytes(), expected)

    def test_cli_round_trip_modifies_only_selected_summary(self):
        for is_template in (False, True):
            with self.subTest(is_template=is_template):
                if is_template:
                    prefix = self.template_target()
                else:
                    self.target = self.target.rename(self.folder / 'summary.md')
                    prefix = b''
                # State/proposal stay outside the summarized folder.
                state_path = self.root / 'state.json'
                proposal_path = self.root / 'proposal.md'
                proposed = prefix + b'# Directory Summary\nCLI proposal\n'
                proposal_path.write_bytes(proposed)
                other = self.folder / 'unchanged.tex'
                other.write_bytes(b'unchanged dependency')
                before = helper.signature(other)
                def run(*arguments):
                    result = subprocess.run(
                        [sys.executable, '-B', str(Path(helper.__file__).resolve()),
                         *arguments], cwd=self.root, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    return result.stdout
                run('prepare', self.target.name, '--state', str(state_path))
                state = json.loads(state_path.read_text(encoding='utf-8'))
                self.assertEqual(state['target'], self.target.relative_to(self.root).as_posix())
                run('read', '--state', str(state_path), '--path', state['target'])
                self.assertTrue(run('commit', '--state', str(state_path),
                                    '--proposal', str(proposal_path)).startswith('updated'))
                self.assertEqual(self.target.read_bytes(), proposed)
                self.assertEqual(helper.signature(other), before)
                self.assertEqual(other.read_bytes(), b'unchanged dependency')

    def test_atomic_update_then_unchanged_run(self):
        state = self.prepare()
        self.assertEqual(helper.commit(state, b'new proposal\n'), 'updated')
        self.assertEqual(self.target.read_bytes(), b'new proposal\n')
        before = helper.signature(self.target)
        self.assertEqual(helper.commit(self.prepare(), b'new proposal\n'), 'already current')
        self.assertEqual(helper.signature(self.target), before)
        self.assertFalse(list(self.folder.glob('.readme-*.tmp')))

    def test_edit_during_staging_does_not_overwrite(self):
        state = self.prepare()
        real_verify = helper.verify
        def edit_then_verify(current, staging=None):
            if staging is not None:
                self.target.write_bytes(b'concurrent during staging')
            real_verify(current, staging)
        with patch.object(helper, 'verify', edit_then_verify):
            with self.assertRaisesRegex(ValueError, 'Concurrent'):
                helper.commit(state, b'stale proposal')
        self.assertEqual(self.target.read_bytes(), b'concurrent during staging')
        self.assertFalse(list(self.folder.glob('.readme-*.tmp')))

    def test_concurrent_changes_do_not_overwrite(self):
        for what in ('readme', 'reviewed', 'inventory', 'template'):
            with self.subTest(what=what):
                source = self.source('new.tex', 100)
                state = self.prepare()
                helper.read_input(state, 'content/new.tex')
                original = self.target.read_bytes()
                if what == 'readme':
                    self.target.write_bytes(b'concurrent README edit')
                elif what == 'reviewed':
                    source.write_bytes(b'changed contents')
                elif what == 'inventory':
                    self.source('added.tex', 100)
                else:
                    (self.root / helper.TEMPLATE).write_bytes(b'changed template')
                expected = self.target.read_bytes()
                with self.assertRaisesRegex(ValueError, 'Concurrent'):
                    helper.commit(state, b'stale proposal')
                self.assertEqual(self.target.read_bytes(), expected)
                self.target.write_bytes(original)
                os.utime(self.target, ns=(self.time, self.time))


if __name__ == '__main__':
    unittest.main()
