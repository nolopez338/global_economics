"""Timestamp-only review gate; standard library, no persistent cache."""
import argparse
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile

SKIP = {'.git', '.hg', '.svn', '__pycache__', '.cache', '.pytest_cache',
        '.mypy_cache', '.ruff_cache', 'node_modules', '.venv', 'venv',
        'build', 'dist', 'out', '.next', '.tox', 'coverage', '_build',
        '.readme-cache', '.codex', '.agents'}
ARTIFACTS = ('*.aux', '*.log', '*.synctex*', '*.toc', '*.out', '*.lof',
             '*.lot', '*.fls', '*.fdb_latexmk', '*.pdf', '*.gz', '*.bat',
             '*.nav', '*.snm', '*.vrb', '*.bcf', '*.run.xml', '*.blg', '*.pyc')
TEMPLATE = 'book2026-2027/preamble/template_README.md'


def validate_filename(name):
    """Accept a single portable Markdown basename, never a path."""
    if (not name or
            any(ord(c) < 32 or c in '<>:"/\\|?*' for c in name) or
            Path(name).suffix.lower() not in {'.md', '.markdown'} or
            name.lower() in {'.md', '.markdown'}):
        raise ValueError('Expected one Markdown filename (.md or .markdown) without a path')


def template_prefix(data):
    """Keep the live template's rules separate from its replaceable summary."""
    boundary = re.search(rb'(?m)^# Directory Summary\r?$', data)
    if boundary is None:
        raise ValueError('Live template lacks a # Directory Summary boundary; stop without saving')
    return data[:boundary.start()]


def root_from(cwd):
    result = subprocess.run(['git', '-C', str(cwd), 'rev-parse', '--show-toplevel'],
                            capture_output=True, text=True, check=True)
    return Path(result.stdout.strip()).resolve()


def signature(path):
    s = path.stat()
    return [s.st_mtime_ns, s.st_size, s.st_ctime_ns, s.st_ino, s.st_mode]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def discover(root, name):
    matches = []
    def fail(error):
        raise error
    for directory, dirs, files in os.walk(root, onerror=fail, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d.lower() not in SKIP
                         and not (Path(directory) / d).is_symlink())
        if name in files:
            p = Path(directory) / name
            if not p.is_symlink():
                matches.append(p.relative_to(root).as_posix())
    return sorted(matches)


def inventory(root, target):
    """Metadata only, including excluded immediate files for conflict detection."""
    entries = {}
    for p in sorted((root / target).parent.iterdir()):
        if p.name.lower() in SKIP or p.is_symlink():
            continue
        rel = p.relative_to(root).as_posix()
        entries[rel] = signature(p)
        if p.is_dir():
            for child in sorted(p.iterdir()):
                if (child.name == 'README.md' or
                        (child.name.startswith('README-') and child.suffix == '.md')):
                    if child.is_file() and not child.is_symlink():
                        entries[child.relative_to(root).as_posix()] = signature(child)
    return entries


def stable_bytes(path, expected=None):
    before = signature(path)
    if expected is not None and before != expected:
        raise ValueError(f'Concurrent edit: {path}')
    data = path.read_bytes()
    if signature(path) != before:
        raise ValueError(f'Concurrent edit while reading: {path}')
    return data


def prepare(root, name, select=None):
    validate_filename(name)
    matches = discover(root, name)
    if not matches:
        raise ValueError('No exact match; no summary created')
    if select is None and len(matches) != 1:
        raise ValueError('Multiple exact matches; ask which to use:\n' + '\n'.join(matches))
    target = select if select is not None else matches[0]
    if target not in matches:
        raise ValueError('Selection is not an exact discovered match')
    snap = inventory(root, target)
    cutoff = snap[target][0]
    control_paths = tuple(dict.fromkeys((target, TEMPLATE)))
    eligible = [p for p, s in snap.items() if p not in control_paths and stat.S_ISREG(s[4])
                and s[0] > cutoff
                and not any(fnmatch.fnmatch(Path(p).name.lower(), pattern)
                            for pattern in ARTIFACTS)]
    controls = {}
    preserved_prefix = None
    for rel in control_paths:
        sig = signature(root / rel)
        data = stable_bytes(root / rel, sig)
        controls[rel] = {'signature': sig, 'hash': digest(data)}
        if target == TEMPLATE and rel == target:
            prefix = template_prefix(data)
            preserved_prefix = {'length': len(prefix), 'hash': digest(prefix)}
    if controls[target]['signature'] != snap[target]:
        raise ValueError('Concurrent README edit during prepare')
    seconds, nanos = divmod(cutoff, 1_000_000_000)
    utc = datetime.fromtimestamp(seconds, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
    return dict(root=str(root), target=target, cutoff_ns=cutoff,
                cutoff_utc=f'{utc}.{nanos:09d}Z', inventory=snap,
                eligible=eligible, controls=controls, reviewed={},
                template_prefix=preserved_prefix)


def read_input(state, rel):
    root = Path(state['root'])
    if rel in state['controls']:
        control = state['controls'][rel]
        data = stable_bytes(root / rel, control['signature'])
        if digest(data) != control['hash']:
            raise ValueError('Concurrent control edit')
    elif rel in state['eligible']:
        data = stable_bytes(root / rel, state['inventory'][rel])
        state['reviewed'][rel] = digest(data)
    else:
        raise ValueError('Read denied: path is not a control or newer source')
    return data


def verify(state, staging=None):
    root = Path(state['root'])
    snapshot = inventory(root, state['target'])
    if staging is not None:
        snapshot.pop(staging.relative_to(root).as_posix(), None)
    if snapshot != state['inventory']:
        raise ValueError('Concurrent inventory/input edit; stop without saving')
    for rel, control in state['controls'].items():
        if digest(stable_bytes(root / rel, control['signature'])) != control['hash']:
            raise ValueError(f'Concurrent control edit: {rel}')
    for rel, expected in state['reviewed'].items():
        if digest(stable_bytes(root / rel, state['inventory'][rel])) != expected:
            raise ValueError(f'Concurrent reviewed input edit: {rel}')


def commit(state, proposed):
    verify(state)
    if state['target'] == TEMPLATE:
        prefix = state['template_prefix']
        if (digest(proposed[:prefix['length']]) != prefix['hash'] or
                not re.match(rb'# Directory Summary(?:\r?\n|$)', proposed[prefix['length']:])):
            raise ValueError('Preserve live template instructions byte for byte before # Directory Summary')
    target = Path(state['root']) / state['target']
    old = stable_bytes(target, state['inventory'][state['target']])
    if proposed == old:
        return 'already current'
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.readme-',
                                         suffix='.tmp', delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(proposed)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, stat.S_IMODE(target.stat().st_mode))
        verify(state, temporary)
        os.replace(temporary, target)
        return 'updated'
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    prep = sub.add_parser('prepare')
    prep.add_argument('filename')
    prep.add_argument('--select')
    prep.add_argument('--state', required=True, type=Path)
    read = sub.add_parser('read')
    read.add_argument('--state', required=True, type=Path)
    read.add_argument('--path', required=True)
    read.add_argument('--output', type=Path)
    save = sub.add_parser('commit')
    save.add_argument('--state', required=True, type=Path)
    save.add_argument('--proposal', required=True, type=Path)
    args = parser.parse_args()
    try:
        state = (prepare(root_from(Path.cwd()), args.filename, args.select)
                 if args.command == 'prepare' else
                 json.loads(args.state.read_text(encoding='utf-8')))
        folder = (Path(state['root']) / state['target']).parent.resolve()
        paths = [args.state]
        if args.command == 'commit':
            paths.append(args.proposal)
        if args.command == 'read' and args.output:
            paths.append(args.output)
        for path in paths:
            if path.resolve().is_relative_to(folder):
                raise ValueError('Workflow temporary files must be outside the summarized folder')
        if args.command == 'read':
            data = read_input(state, args.path)
            if args.output:
                args.output.write_bytes(data)
            else:
                print(data.decode('utf-8-sig'))
        elif args.command == 'commit':
            print(commit(state, args.proposal.read_bytes()))
            print(json.dumps({k: state[k] for k in
                              ('target', 'cutoff_ns', 'cutoff_utc', 'reviewed')}, indent=2))
        else:
            print(json.dumps(state, indent=2))
        if args.command != 'commit':
            args.state.write_text(json.dumps(state, indent=2), encoding='utf-8')
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
