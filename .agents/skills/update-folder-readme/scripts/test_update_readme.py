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
                    'C:notes.md', 'notes.md/other.md', 'notes?.md', 'notes*.md',
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

    def test_cli_rejects_extra_arguments_and_invalid_paths_without_state(self):
        state_path = self.root / 'state.json'
        for arguments in ([NAME, 'extra.md'], ['../' + NAME], ['missing\\notes.md'],
                          ['notes.txt']):
            with self.subTest(arguments=arguments):
                result = subprocess.run(
                    [sys.executable, '-B', str(Path(helper.__file__).resolve()), 'prepare',
                     *arguments, '--state', str(state_path)], cwd=self.root,
                    capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(state_path.exists())

    def test_explicit_paths_bypass_discovery(self):
        for argument in ('content/' + NAME, 'content\\' + NAME,
                         '/content/' + NAME, '\\content\\' + NAME,
                         str(self.target), self.target.as_posix()):
            with self.subTest(argument=argument), patch.object(
                    helper, 'discover', side_effect=AssertionError('discovery called')):
                state = helper.prepare(self.root, argument)
                self.assertEqual(state['target'], 'content/' + NAME)
                self.assertTrue(state['target_existed'])
                self.assertEqual(state['mode'], 'update')
                self.assertEqual(state['cutoff_ns'], self.time)

    @unittest.skipUnless(os.name == 'nt', 'Windows case-insensitive paths')
    def test_case_variants_keep_live_template_protection(self):
        prefix = self.template_target()
        state = helper.prepare(self.root, helper.TEMPLATE.upper())
        self.assertEqual(state['target'], helper.TEMPLATE)
        with self.assertRaisesRegex(ValueError, 'Preserve live template'):
            helper.commit(state, b'# Directory Summary\nlost instructions')
        self.assertEqual(helper.commit(state, prefix + b'# Directory Summary\nnew'), 'updated')

    def test_symlink_rejection_without_os_privileges(self):
        original = helper.is_link
        for rel in ('content', 'content/new.md', helper.TEMPLATE):
            with self.subTest(rel=rel), patch.object(
                    helper, 'is_link', lambda path: path == self.root / rel or original(path)):
                with self.assertRaisesRegex(ValueError, 'Symlink traversal'):
                    helper.prepare(self.root, 'content/new.md')

    def test_creation_cli_read_commit_and_reporting(self):
        self.source('old.tex', -100)
        state_path = self.root / 'state.json'
        proposal = self.root / 'proposal.md'
        proposal.write_bytes(b'# Directory Summary\nproposal')
        def run(*arguments, success=True):
            result = subprocess.run(
                [sys.executable, '-B', str(Path(helper.__file__).resolve()), *arguments],
                cwd=self.root, capture_output=True, text=True)
            self.assertEqual(result.returncode == 0, success, result.stderr)
            return result.stdout + result.stderr
        run('prepare', 'content/new notes.md', '--state', str(state_path))
        self.assertFalse((self.folder / 'new notes.md').exists())
        run('read', '--state', str(state_path), '--path', 'content/old.tex')
        run('read', '--state', str(state_path), '--path', 'content/new notes.md', success=False)
        report = run('commit', '--state', str(state_path), '--proposal', str(proposal))
        self.assertTrue(report.startswith('created\n'))
        self.assertIn('not applicable', report)
        self.assertIn('content/new notes.md', report)
        self.assertIn('content/old.tex', report)
        self.assertIn('unreviewed_eligible', report)

    def test_cli_keeps_state_and_proposals_outside_folder_in_both_modes(self):
        for target in ('content/' + NAME, 'content/new.md'):
            with self.subTest(target=target):
                result = subprocess.run(
                    [sys.executable, '-B', str(Path(helper.__file__).resolve()), 'prepare',
                     target, '--state', str(self.folder / 'state.json')], cwd=self.root,
                    capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('outside the summarized folder', result.stderr)
                self.assertFalse((self.folder / 'state.json').exists())

    def test_quoted_paths_spaces_extensions_and_leading_backslash(self):
        folder = self.root / 'teacher' / 'assets' / 'css'
        folder.mkdir(parents=True)
        state = helper.prepare(self.root, r'\teacher\assets\css\README_TAcss.md')
        self.assertEqual(state['target'], 'teacher/assets/css/README_TAcss.md')
        self.assertEqual(state['mode'], 'create')
        for name in ('folder notes.MD', 'folder notes.MARKDOWN'):
            for arg in (f'"content/{name}"', f"'content/{name}'", f'content/{name}'):
                with self.subTest(argument=arg):
                    self.assertEqual(helper.prepare(self.root, arg)['target'], 'content/' + name)
        state_path = self.root / 'state.json'
        result = subprocess.run(
            [sys.executable, '-B', str(Path(helper.__file__).resolve()), 'prepare',
             'content/folder notes.md', '--state', str(state_path)], cwd=self.folder,
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(state_path.read_text())['mode'], 'create')

    def test_invalid_explicit_paths_and_missing_parents(self):
        (self.folder / 'directory.md').mkdir()
        outside = self.root.parent / 'outside.md'
        arguments = ('content/directory.md', 'missing/notes.md', '../outside.md',
                     'content/../notes.md', 'content/notes.txt', 'content/NUL.md',
                     'content/notes?.md', 'content/notes.md/', '//server/share/notes.md',
                     'C:notes.md', 'content/notes\x00.md', 'content/notes.md ')
        if os.name == 'nt':
            arguments += (str(outside), 'Z:/outside.md')
        for argument in arguments:
            with self.subTest(argument=argument), self.assertRaises(ValueError):
                helper.prepare(self.root, argument)
        self.assertFalse((self.root / 'missing').exists())
        with self.assertRaisesRegex(ValueError, 'explicit filepath is required'):
            helper.prepare(self.root, 'absent.md')

    def test_creation_all_eligible_immediate_inputs_and_proposal(self):
        for name, offset in (('old.tex', -100), ('equal.tex', 0), ('new.tex', 100),
                             ('ignored.pdf', -100), ('child/README.md', -100),
                             ('child/README-topic.md', 0), ('child/notes.md', 100),
                             ('child/deep/README.md', 100)):
            self.source(name, offset)
        state = helper.prepare(self.root, 'content/new summary.md')
        self.assertFalse(state['target_existed'])
        self.assertIsNone(state['cutoff_ns'])
        self.assertEqual(state['cutoff_utc'], 'not applicable')
        self.assertEqual(set(state['controls']), {helper.TEMPLATE})
        self.assertEqual(set(state['eligible']), {'content/' + NAME, 'content/old.tex',
                         'content/equal.tex', 'content/new.tex', 'content/child/README.md',
                         'content/child/README-topic.md'})
        with self.assertRaisesRegex(ValueError, 'Read denied'):
            helper.read_input(state, state['target'])
        for rel in state['eligible']:
            helper.read_input(state, rel)
        proposed = b'# Directory Summary\nnew summary from proposal\n'
        self.assertFalse((self.folder / 'new summary.md').exists())
        self.assertEqual(helper.commit(state, proposed), 'created')
        self.assertEqual((self.folder / 'new summary.md').read_bytes(), proposed)
        self.assertFalse(list(self.folder.glob('.readme-*.tmp')))

    def test_missing_live_template_stops_creation_including_template_target(self):
        template = self.root / helper.TEMPLATE
        template.unlink()
        for argument in ('content/new.md', helper.TEMPLATE):
            with self.subTest(argument=argument), self.assertRaisesRegex(ValueError, 'template is missing'):
                helper.prepare(self.root, argument)
        self.assertFalse(template.exists())

    def test_creation_rechecks_inputs_controls_and_inventory(self):
        for what in ('reviewed', 'control', 'inventory'):
            with self.subTest(what=what):
                source = self.source('old.tex', -100)
                state = helper.prepare(self.root, 'content/new.md')
                helper.read_input(state, 'content/old.tex')
                if what == 'reviewed':
                    source.write_bytes(b'changed')
                elif what == 'control':
                    (self.root / helper.TEMPLATE).write_bytes(b'changed template')
                else:
                    self.source('extra.tex')
                with self.assertRaisesRegex(ValueError, 'Concurrent'):
                    helper.commit(state, b'proposal')
                self.assertFalse((self.folder / 'new.md').exists())

    def test_concurrent_creation_before_and_after_final_verification(self):
        target = self.folder / 'new.md'
        state = helper.prepare(self.root, 'content/new.md')
        target.write_bytes(b'concurrent')
        with self.assertRaisesRegex(ValueError, 'Concurrent target creation'):
            helper.commit(state, b'proposal')
        self.assertEqual(target.read_bytes(), b'concurrent')
        target.unlink()
        state = helper.prepare(self.root, 'content/new.md')
        real_publish = helper.publish_new
        def race(source, destination):
            target.write_bytes(b'race winner')
            return real_publish(source, destination)
        with patch.object(helper, 'publish_new', race):
            with self.assertRaisesRegex(ValueError, 'Concurrent target creation'):
                helper.commit(state, b'proposal')
        self.assertEqual(target.read_bytes(), b'race winner')
        self.assertFalse(list(self.folder.glob('.readme-*.tmp')))

    def test_symlink_traversal_and_concurrent_replacement(self):
        link = self.root / 'linked'
        try:
            link.symlink_to(self.folder, target_is_directory=True)
        except OSError as error:
            self.skipTest(f'Symlinks unavailable: {error}')
        with self.assertRaisesRegex(ValueError, 'Symlink traversal'):
            helper.prepare(self.root, 'linked/new.md')
        target_link = self.folder / 'linked.md'
        target_link.symlink_to(self.target)
        with self.assertRaisesRegex(ValueError, 'Symlink traversal'):
            helper.prepare(self.root, 'content/linked.md')
        state = helper.prepare(self.root, 'content/new.md')
        (self.folder / 'new.md').symlink_to(self.target)
        with self.assertRaises(ValueError):
            helper.commit(state, b'proposal')

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
