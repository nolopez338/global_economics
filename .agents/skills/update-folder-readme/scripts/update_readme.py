"""Create explicit Markdown targets or incrementally update existing summaries."""
import argparse
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
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
    """Validate each basename using portable Windows filename rules."""
    if (not name or
            any(ord(c) < 32 or c in '<>:"/\\|?*' for c in name) or
            Path(name).suffix.lower() not in {'.md', '.markdown'} or
            name.lower() in {'.md', '.markdown'} or invalid_component(name)):
        raise ValueError('Expected one valid Markdown filename or filepath (.md or .markdown)')


def invalid_component(name):
    return (not name or name.endswith((' ', '.')) or
            any(ord(c) < 32 or c in '<>:"|?*' for c in name) or
            name.split('.')[0].upper() in
            {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)),
             *(f'LPT{i}' for i in range(1, 10))})


def is_link(path):
    return path.is_symlink() or getattr(path, 'is_junction', lambda: False)()


def safe_path(root, rel):
    """Check lexical containment and every existing component before resolving."""
    path = root / rel
    if not path.is_relative_to(root):
        raise ValueError('Target must remain inside the repository')
    current = root
    for part in path.relative_to(root).parts:
        current = current / part
        if is_link(current):
            raise ValueError(f'Symlink traversal is forbidden: {current}')
    return path


def resolve_argument(root, argument):
    """Return a basename for discovery or a checked, repository-relative path."""
    # Shells normally remove quotes; also accept a quoted argument passed directly.
    if len(argument) >= 2 and argument[0] == argument[-1] and argument[0] in '\"\'':
        argument = argument[1:-1]
    explicit = '/' in argument or '\\' in argument or bool(PureWindowsPath(argument).drive)
    if not explicit:
        validate_filename(argument)
        return argument, False
    normalized = argument.replace('\\', '/')
    win = PureWindowsPath(argument)
    if win.drive:
        if not win.is_absolute() or win.drive.startswith('\\\\'):
            raise ValueError('Invalid absolute filepath')
        if os.name != 'nt':
            raise ValueError('Windows absolute target is outside this repository')
        candidate = Path(normalized)
    elif normalized.startswith('//'):
        raise ValueError('UNC paths are not supported')
    elif os.name != 'nt' and normalized.startswith(root.as_posix() + '/'):
        candidate = Path(normalized)
    else:
        # A single leading slash means repository-relative, including on Windows.
        candidate = root / normalized.lstrip('/')
    parts = normalized.split('/')
    for index, part in enumerate(parts):
        if part in ('', '.') or (index == 0 and win.drive):
            continue
        if part == '..' or invalid_component(part):
            raise ValueError('Invalid filepath component (traversal is forbidden)')
    validate_filename(parts[-1])
    if not candidate.is_relative_to(root):
        raise ValueError('Target must remain inside the repository')
    rel = candidate.relative_to(root).as_posix()
    path = safe_path(root, rel)
    if not path.parent.is_dir():
        raise ValueError('Target parent directory must exist; no directories are created')
    if path.exists() and not path.is_file():
        raise ValueError('Target must be a regular Markdown file, not a directory')
    # Preserve actual filesystem spelling (especially the dual-purpose template
    # on case-insensitive Windows filesystems) for inventory/control identity.
    canonical = path.resolve()
    if not canonical.is_relative_to(root):
        raise ValueError('Target must remain inside the repository')
    return canonical.relative_to(root).as_posix(), True


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
                         and not is_link(Path(directory) / d))
        if name in files:
            p = Path(directory) / name
            if not is_link(p):
                matches.append(p.relative_to(root).as_posix())
    return sorted(matches)


def inventory(root, target):
    """Metadata only, including excluded immediate files for conflict detection."""
    entries = {}
    for p in sorted(safe_path(root, target).parent.iterdir()):
        if p.name.lower() in SKIP:
            continue
        rel = p.relative_to(root).as_posix()
        if is_link(p):
            s = p.lstat()
            entries[rel] = [s.st_mtime_ns, s.st_size, s.st_ctime_ns, s.st_ino, s.st_mode]
            continue
        entries[rel] = signature(p)
        if p.is_dir():
            for child in sorted(p.iterdir()):
                if (child.name == 'README.md' or
                        (child.name.startswith('README-') and child.suffix == '.md')):
                    if not is_link(child) and child.is_file():
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
    root = root.resolve()
    argument, explicit = resolve_argument(root, name)
    if explicit:
        if select is not None:
            raise ValueError('--select applies only to bare-filename discovery')
        target = argument
    else:
        matches = discover(root, argument)
        if not matches:
            raise ValueError('No exact match; an explicit filepath is required for creation')
        if select is None and len(matches) != 1:
            raise ValueError('Multiple exact matches; ask which to use:\n' + '\n'.join(matches))
        target = select if select is not None else matches[0]
        if target not in matches:
            raise ValueError('Selection is not an exact discovered match')
    target_path = safe_path(root, target)
    existed = target_path.exists()
    template = safe_path(root, TEMPLATE)
    if not template.is_file():
        raise ValueError('Live control template is missing; stop without creating it or a summary')
    snap = inventory(root, target)
    if (existed and target not in snap) or (not existed and target in snap):
        raise ValueError('Concurrent target change during prepare')
    cutoff = snap[target][0] if existed else None
    control_paths = tuple(dict.fromkeys((target, TEMPLATE))) if existed else (TEMPLATE,)
    eligible = [p for p, s in snap.items() if p not in control_paths and stat.S_ISREG(s[4])
                and (cutoff is None or s[0] > cutoff)
                and not any(fnmatch.fnmatch(Path(p).name.lower(), pattern)
                            for pattern in ARTIFACTS)]
    controls = {}
    preserved_prefix = None
    for rel in control_paths:
        path = safe_path(root, rel)
        sig = signature(path)
        data = stable_bytes(path, sig)
        controls[rel] = {'signature': sig, 'hash': digest(data)}
        if target == TEMPLATE and rel == target:
            prefix = template_prefix(data)
            preserved_prefix = {'length': len(prefix), 'hash': digest(prefix)}
    if existed and controls[target]['signature'] != snap[target]:
        raise ValueError('Concurrent README edit during prepare')
    cutoff_utc = 'not applicable'
    if cutoff is not None:
        seconds, nanos = divmod(cutoff, 1_000_000_000)
        utc = datetime.fromtimestamp(seconds, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')
        cutoff_utc = f'{utc}.{nanos:09d}Z'
    return dict(root=str(root), target=target, mode='update' if existed else 'create',
                target_existed=existed, cutoff_ns=cutoff,
                cutoff_utc=cutoff_utc, inventory=snap,
                eligible=eligible, controls=controls, reviewed={},
                template_prefix=preserved_prefix)


def read_input(state, rel):
    root = Path(state['root'])
    if rel in state['controls']:
        control = state['controls'][rel]
        data = stable_bytes(safe_path(root, rel), control['signature'])
        if digest(data) != control['hash']:
            raise ValueError('Concurrent control edit')
    elif rel in state['eligible']:
        data = stable_bytes(safe_path(root, rel), state['inventory'][rel])
        state['reviewed'][rel] = digest(data)
    else:
        raise ValueError('Read denied: path is not a control or eligible source')
    return data


def verify(state, staging=None):
    root = Path(state['root'])
    target = safe_path(root, state['target'])
    if not state['target_existed'] and os.path.lexists(target):
        raise ValueError('Concurrent target creation; stop without saving')
    snapshot = inventory(root, state['target'])
    if staging is not None:
        snapshot.pop(staging.relative_to(root).as_posix(), None)
    if snapshot != state['inventory']:
        raise ValueError('Concurrent inventory/input edit; stop without saving')
    for rel, control in state['controls'].items():
        if digest(stable_bytes(safe_path(root, rel), control['signature'])) != control['hash']:
            raise ValueError(f'Concurrent control edit: {rel}')
    for rel, expected in state['reviewed'].items():
        if digest(stable_bytes(safe_path(root, rel), state['inventory'][rel])) != expected:
            raise ValueError(f'Concurrent reviewed input edit: {rel}')


def publish_new(staging, target):
    """Atomically publish without overwriting; never fall back to replace."""
    # Windows rename fails on an existing destination; POSIX rename overwrites.
    if os.name == 'nt':
        os.rename(staging, target)
    else:
        os.link(staging, target)


def commit(state, proposed):
    verify(state)
    if state['target'] == TEMPLATE:
        prefix = state['template_prefix']
        if (digest(proposed[:prefix['length']]) != prefix['hash'] or
                not re.match(rb'# Directory Summary(?:\r?\n|$)', proposed[prefix['length']:])):
            raise ValueError('Preserve live template instructions byte for byte before # Directory Summary')
    target = Path(state['root']) / state['target']
    if state['target_existed']:
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
        if state['target_existed']:
            os.chmod(temporary, stat.S_IMODE(target.stat().st_mode))
        verify(state, temporary)
        if state['target_existed']:
            os.replace(temporary, target)
            return 'updated'
        try:
            publish_new(temporary, target)
        except FileExistsError as error:
            raise ValueError('Concurrent target creation; stop without saving') from error
        return 'created'
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    prep = sub.add_parser('prepare')
    prep.add_argument('filename', help='one Markdown filename or explicit filepath')
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
                              ('mode', 'target', 'cutoff_ns', 'cutoff_utc', 'reviewed')}, indent=2))
            print(json.dumps({'controls': list(state['controls']),
                              'limitations': {'unreviewed_eligible': sorted(
                                  set(state['eligible']) - set(state['reviewed']))}}, indent=2))
        else:
            print(json.dumps(state, indent=2))
        if args.command != 'commit':
            args.state.write_text(json.dumps(state, indent=2), encoding='utf-8')
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
