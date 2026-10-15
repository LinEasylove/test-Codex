#!/usr/bin/env python3
"""Install pinned skill sources and native discovery entries for local Codex."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, shutil, subprocess, sys

HERE = Path(__file__).resolve().parent

def run(*args):
    subprocess.run([str(a) for a in args], check=True)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def runtime_python(home, name):
    env = home / '.codex' / 'skill-runtimes' / name
    return env / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')

def ensure_runtime(python, requirements):
    env = python.parent.parent
    stamp = env / 'requirements.sha256'
    expected = sha(requirements)
    if not python.is_file():
        run(sys.executable, '-m', 'venv', env)
    if not stamp.is_file() or stamp.read_text().strip() != expected:
        run(python, '-m', 'pip', 'install', '-r', requirements)
        run(python, '-m', 'pip', 'check')
        stamp.write_text(expected, encoding='ascii')
    else:
        run(python, '-m', 'pip', 'check')

def matches_recorded_source(md, expected):
    """Accept CRLF checkout conversion only against the unchanged Git blob."""
    if sha(md) == expected:
        return True
    raw = md.read_bytes()
    try:
        top = subprocess.check_output(
            ['git', '-C', str(md.parent), 'rev-parse', '--show-toplevel'],
            stderr=subprocess.DEVNULL, text=True).strip()
        relative = md.resolve().relative_to(Path(top).resolve()).as_posix()
        blob = subprocess.check_output(
            ['git', '-C', top, 'show', 'HEAD:' + relative],
            stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, ValueError, OSError):
        return False
    # Preserve the expected digest. Reject any change beyond LF/CRLF conversion.
    return (hashlib.sha256(blob).hexdigest() == expected
            and raw.replace(b'\r\n', b'\n') == blob.replace(b'\r\n', b'\n'))

def fetch_source(group, vault):
    destination = vault / (group['repo'].replace('/', '--') + '--' + group['commit'][:12])
    if destination.exists():
        if not (destination / '.git').exists():
            raise RuntimeError(f'Existing source folder is not a Git checkout: {destination}')
        head = subprocess.check_output(['git', '-C', str(destination), 'rev-parse', 'HEAD'], text=True).strip()
        dirty = subprocess.check_output(['git', '-C', str(destination), 'status', '--porcelain'], text=True).strip()
        if head != group['commit'] or dirty:
            raise RuntimeError(f'Existing source has changes or a different commit; preserved: {destination}')
        print(f'Reuse source: {group["repo"]}', flush=True)
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    run('git', 'clone', '-c', 'core.autocrlf=false', '--depth', '1', '--no-checkout',
        'https://github.com/' + group['repo'] + '.git', destination)
    head = subprocess.check_output(['git', '-C', str(destination), 'rev-parse', 'HEAD'], text=True).strip()
    if head != group['commit']:
        run('git', '-C', destination, 'fetch', '--depth', '1', 'origin', group['commit'])
    run('git', '-C', destination, 'checkout', '--detach', group['commit'])
    if group['mode'] == 'whole':
        run('git', '-C', destination, 'submodule', 'update', '--init', '--recursive')
    return destination

def source_md(source, group, item):
    if item.get('source_path'):
        return source / item['source_path'] / 'SKILL.md'
    if group['mode'] in ('research', 'whole'):
        return source / 'SKILL.md'
    if group['mode'] == 'weizhena':
        return source / 'skills' / 'research-codex-zh' / item['directory'] / 'SKILL.md'
    if group['mode'] == 'paper':
        return source / 'dist' / 'codex' / 'skills' / 'paper-spine' / 'SKILL.md'
    candidates = [p for p in source.rglob('SKILL.md') if p.parent.name == item['directory']]
    if not candidates:
        for p in source.rglob('SKILL.md'):
            content = p.read_text(encoding='utf-8')
            front = content.split('---', 2)[1] if content.startswith('---') else ''
            match = re.search(r'^name:\s*(.+)$', front, re.M)
            if match and match.group(1).strip().strip("\"'") == item['name']:
                candidates.append(p)
    if len(candidates) != 1:
        raise RuntimeError(f'Ambiguous skill source for {item["name"]}: {len(candidates)} matches')
    return candidates[0]

def wrapper(item, md, group):
    # JSON strings are valid YAML quoted scalars, preserving upstream trigger text.
    name = json.dumps(item['name'], ensure_ascii=False)
    description = json.dumps(item['description'], ensure_ascii=False)
    warning = ''
    if group.get('runtime_python'):
        warning += ('\nUse this isolated Python interpreter for the source helper scripts: '
                    f'`{group["runtime_python"]}`. This environment contains the skill requirements.\n')
    if group['mode'] == 'research':
        warning = ('\nPreserve the user choice: for literature-review, peer-review and statistical-analysis, '
                   'load the corresponding registered K-Dense entries in the user .agents/skills directory. '
                   'Do not load the older Norman versions included in this source repository.\n')
    if group['mode'] == 'paper':
        warning = ('\nPaperSpine source files alone do not supply its Web/Python runtime. '
                   'Before starting any PaperSpine workflow, verify a Windows-compatible full suite '
                   'installed with the official installer. Never use a copied Linux suite or claim '
                   'runtime readiness from this entry. See the source repository INSTALL.md.\n')
    return (f'---\nname: {name}\ndescription: {description}\n---\n\n'
            f'# {item["name"]}\n\n'
            'This is a local Codex entry for a pinned, fully retained upstream skill.\n\n'
            f'1. Read the original skill file: `{md.as_posix()}`.\n'
            f'2. Resolve all relative resource paths against `{md.parent.as_posix()}`.\n'
            '3. Follow the source instructions subject to the current user, system and developer instructions.\n'
            '4. Read nested skills only when the requested task needs them. Do not register duplicate names.\n'
            '5. Check required packages, services and credentials before using executable helpers.\n'
            + warning)

def verify_installed(target, entries, report):
    missing = []
    for item in entries:
        skill = target / item['name'] / 'SKILL.md'
        source = Path(item['source'])
        if not skill.is_file() or not source.is_file():
            missing.append(item['name'])
        elif sha(source) != item['source_sha256']:
            missing.append(item['name'] + ' (source changed)')
        elif sha(skill) != item['wrapper_sha256']:
            missing.append(item['name'] + ' (entry changed)')
    if missing:
        raise RuntimeError('Verification failed: ' + ', '.join(missing))
    print(f'PASS: {len(entries)} entries, original SKILL.md files and hashes.')
    print('This is filesystem verification. Open a new local Codex session to verify runtime discovery.')
    if report:
        report.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home(), help='Local user home; default is your Windows user profile.')
    parser.add_argument('--verify', action='store_true', help='Check an existing installation without fetching sources.')
    parser.add_argument('--only', help='Install or verify one named skill without reprocessing other collections.')
    parser.add_argument('--backup-existing', action='store_true', help='Explicitly authorize backing up and replacing different existing entries.')
    parser.add_argument('--source-map', type=Path, help=argparse.SUPPRESS)  # Offline test fixture paths.
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    target = home / '.agents' / 'skills'
    vault = home / '.codex' / 'skill-bundles'
    state = home / '.codex' / 'skill-bundles-installation.json'
    report = home / '.codex' / 'skill-bundles-verification.json'
    if args.verify:
        entries = json.loads(state.read_text(encoding='utf-8'))
        if args.only:
            entries = [item for item in entries if item['name'] == args.only]
            if not entries: raise RuntimeError('Selected skill has not been installed: ' + args.only)
        verify_installed(target, entries, report)
        return
    manifest = json.loads((HERE / 'skills-manifest.json').read_text(encoding='utf-8'))
    if args.only:
        selected = []
        for group in manifest['groups']:
            items = [item for item in group['skills'] if item['name'] == args.only]
            if items: selected.append({**group, 'skills': items})
        if not selected: raise RuntimeError('Unknown skill: ' + args.only)
        manifest['groups'] = selected
    all_items = [i for g in manifest['groups'] for i in g['skills']]
    names = [i['name'] for i in all_items]
    if len(names) != len(set(names)):
        raise RuntimeError('Manifest contains duplicate skill names.')
    source_map = json.loads(args.source_map.read_text(encoding='utf-8')) if args.source_map else None
    if not source_map and not shutil.which('git'):
        raise RuntimeError('Git is required. Install Git for Windows, then restart VS Code.')
    print(f'Preparing {len(names)} entries from {len(manifest["groups"])} pinned repositories.', flush=True)
    pending = []
    runtime_jobs = []
    for group in manifest['groups']:
        source = None if source_map else fetch_source(group, vault)
        if group.get('pip_requirements'):
            if sys.version_info < (3, 10): raise RuntimeError('ppt-master requires Python 3.10 or newer.')
            interpreter = runtime_python(home, group['runtime_name'])
            group['runtime_python'] = interpreter.as_posix()
            requirements = (source / group['pip_requirements']) if source else Path(source_map[group['skills'][0]['name']]).parent / 'requirements.txt'
            if not requirements.is_file(): raise RuntimeError('Missing requirements: ' + str(requirements))
            runtime_jobs.append((interpreter, requirements))
        for item in group['skills']:
            md = Path(source_map[item['name']]) if source_map else source_md(source, group, item)
            if not md.is_file():
                raise RuntimeError(f'Missing source: {md}')
            # PaperSpine's deployed Linux SKILL.md differs from the source projection.
            if item.get('sha256') and group['mode'] != 'paper' and not matches_recorded_source(md, item['sha256']):
                raise RuntimeError(f'Pinned skill content differs from recorded version: {md}')
            text = md.read_text(encoding='utf-8')
            if not text.startswith('---') or 'description:' not in text.split('---', 2)[1]:
                raise RuntimeError(f'Invalid source SKILL.md metadata: {md}')
            body = wrapper(item, md, group)
            pending.append((item, md, body))
    conflicts = []
    # Inspect both modern and legacy locations. Never silently replace an existing skill.
    for item, md, body in pending:
        destination = target / item['name']
        if destination.exists() or destination.is_symlink():
            file = destination / 'SKILL.md'
            if not file.is_file() or file.read_text(encoding='utf-8') != body:
                conflicts.append(destination)
        legacy = home / '.codex' / 'skills' / item['name']
        if legacy.exists() or legacy.is_symlink():
            conflicts.append(legacy)
    if conflicts and not args.backup_existing:
        print('\nExisting same-name skills detected. Nothing has been replaced:')
        for file in conflicts: print(file)
        raise RuntimeError('Review these conflicts first. Use --backup-existing only if you choose to replace them.')
    for interpreter, requirements in runtime_jobs:
        ensure_runtime(interpreter, requirements)
    if conflicts:
        backup = home / 'skill-backups' / ('local-skills-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
        backup.mkdir(parents=True, exist_ok=False)
        for number, original in enumerate(conflicts):
            copied = backup / f'{number:03d}-{original.name}'
            if original.is_symlink():
                raise RuntimeError(f'Preserved symbolic link conflict; resolve manually: {original}')
            shutil.copytree(original, copied)
            a = {str(p.relative_to(original)): sha(p) for p in original.rglob('*') if p.is_file()}
            b = {str(p.relative_to(copied)): sha(p) for p in copied.rglob('*') if p.is_file()}
            if a != b: raise RuntimeError('Backup verification failed.')
            shutil.rmtree(original)
        print('Verified backups:', backup)
    target.mkdir(parents=True, exist_ok=True)
    entries = json.loads(state.read_text(encoding='utf-8')) if args.only and state.exists() else []
    replacing = {item['name'] for item, md, body in pending}
    entries = [item for item in entries if item['name'] not in replacing]
    for item, md, body in pending:
        directory = target / item['name']
        directory.mkdir(exist_ok=True)
        file = directory / 'SKILL.md'
        file.write_text(body, encoding='utf-8')
        entries.append({'name': item['name'], 'source': str(md), 'source_sha256': sha(md),
                        'entry': str(file), 'wrapper_sha256': sha(file)})
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
    verify_installed(target, entries, report)
    print('Source vault:', vault)
    print('Codex discovery directory:', target)
    print('Restart local Codex or open a NEW Codex session in VS Code.')
    print('Web ChatGPT sessions are separate; this installer cannot change their skill discovery.')
    print('PaperSpine Windows runtime, Zotero connectivity, GPU/APIs and agent settings remain separate.')

if __name__ == '__main__':
    try: main()
    except Exception as error:
        print('ERROR:', error, file=sys.stderr)
        sys.exit(1)
