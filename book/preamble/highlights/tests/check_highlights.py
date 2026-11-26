"""Focused highlights invariants; Python 3, no external dependencies.

Run: python book/preamble/highlights/tests/check_highlights.py
Optional --root DIR checks an isolated copy of the highlights directory.
Reads TeX declarations, checks membership/identity/loading/document links, and
exits nonzero on violations. This is not a TeX interpreter or a layout check;
compile public_interfaces.tex and the viewers for runtime/render verification.
"""
from pathlib import Path
import argparse
import re


def group(text, pos):
    assert text[pos] == '{', text[pos:pos + 50]
    begin = pos + 1
    depth = 1
    pos += 1
    while depth:
        if text[pos] == '%' and text[pos - 1] != '\\':
            pos = text.index('\n', pos)
            continue
        if text[pos] == '\\':
            match = re.match(r'\\(?:[A-Za-z@]+|.)', text[pos:])
            pos += len(match[0])
            continue
        depth += (text[pos] == '{') - (text[pos] == '}')
        pos += 1
    return text[begin:pos - 1], pos


def declarations(text):
    for match in re.finditer(r'\\HighlightDeclare(Concept|Context|Reference)\s*', text):
        identity, end = group(text, match.end())
        while text[end].isspace():
            end += 1
        body, end = group(text, end)
        fields = {}
        pos = 0
        while pos < len(body):
            key = re.match(r'\s*,?\s*([\w-]+)\s*=\s*', body[pos:])
            if key is None:
                assert not body[pos:].strip(), (identity, body[pos:])
                break
            pos += key.end()
            value, pos = group(body, pos)
            assert key[1] not in fields, (identity, key[1])
            fields[key[1]] = value
        yield match[1], identity, fields


def check(root):
    records = {key: {} for key in ('Concept', 'Context', 'Reference')}
    owners = {}
    # This order matches the live public loader.
    for dataset in ('g11_t1', 'g10_t1', 'g10_t2', 'g11_t2'):
        path = root / ('highlights_' + dataset + '.tex')
        for kind, identity, fields in declarations(path.read_text(encoding='utf-8')):
            assert identity not in records[kind], ('duplicate', kind, identity)
            records[kind][identity] = fields
            owners[kind, identity] = dataset
            if kind == 'Concept':
                assert all(k in fields for k in ('role', 'name', 'notation', 'brief',
                                                'definition', 'source')), \
                    ('missing concept fields', identity)
            if kind == 'Context':
                assert fields['concept'] in records['Concept'], ('unknown concept', identity)
                assert fields['grade'] in ('10', '11') and fields['term'] in ('1', '2')
                assert all(k in fields for k in ('criteria', 'variant', 'notation', 'examples', 'source'))
                assert dataset == 'g' + fields['grade'] + '_t' + fields['term'], ('scope', identity)
            if kind == 'Reference':
                members = [m for m in fields['members'].split(',') if m]
                assert len(members) == len(set(members)), ('duplicate membership', identity)
                assert all(m in records['Context'] for m in members), ('unknown member', identity)
                assert fields['status'] in ('available', 'pending')
                assert bool(members) == (fields['status'] == 'available'), ('availability', identity)

    concepts, contexts, refs = (records[k] for k in ('Concept', 'Context', 'Reference'))
    assert all(k in concepts for k in ('success-probability', 'population-proportion',
                                      'poisson-expected-count', 'exponential-rate',
                                      'sample-standard-deviation', 'standard-error'))
    for grade in (10, 11):
        pending = refs[f'G{grade}-T3-full']
        assert pending == {'status': 'pending', 'members': ''}
        for term in (1, 2):
            full = set(refs[f'G{grade}-T{term}-full']['members'].split(','))
            expected = {i for i, c in contexts.items()
                        if c['grade'] == str(grade) and c['term'] == str(term)
                        and c['variant'] in ('default', 'coordinated', 'introductory-prerequisite')}
            assert full == expected, ('full union coverage', grade, term, full ^ expected)
            assert all(contexts[i]['grade'] == str(grade) and contexts[i]['term'] == str(term)
                       for i in full), ('union scope', grade, term)
    for key in ('G10-T1-C1', 'G10-T1-C2', 'G10-T1-C3', 'G11-T1-C6', 'G11-T1-C7'):
        assert key not in refs, ('fabricated individual reference', key)
    assert refs['G10-T2-C10']['status'] == 'pending'
    assert refs['G11-T1-C9']['members'].split(',')[0] == 'g11-t1-c9-location', \
        'C9 must retain the location prerequisite from its opening comparison'
    compat = '\n'.join((root / f'highlights_compat_{s}.tex').read_text(encoding='utf-8')
                       for s in ('ttwo', 'g10', 'g11'))
    keys = set(re.findall(r'practicehighlightlegend@(G\d+-T\d+-[^\\}\s]+)', compat))
    assert keys <= refs.keys(), ('registry key without reference', keys - refs.keys())
    for key in keys:
        assert refs[key]['status'] == 'available', ('registry availability', key)
    viewer = (root / 'specific_highlights_view.tex').read_text(encoding='utf-8')
    sections = re.findall(r'\\(?:PreviewSection\{[^}]+\}|section)\{([^}]+)\}', viewer[viewer.index('\\begin{document}'):])
    assert sections == ['Introduction', 'Grade 10', 'Grade 11', 'Grade 10 Term 1',
                        'Grade 10 Term 2', 'Grade 10 Term 3', 'Grade 11 Term 1',
                        'Grade 11 Term 2', 'Grade 11 Term 3'], sections
    assert '\\begin{longtable}' not in viewer and '\\begin{tabular' not in viewer
    for (kind, identity), dataset in owners.items():
        if kind not in ('Concept', 'Reference'):
            continue
        text = (root / ('specific_highlights_' + dataset + '.md')).read_text(encoding='utf-8')
        assert '`' + identity + '`' in text, ('undocumented interface', identity)
        if kind == 'Reference':
            record = refs[identity]
            count = len([m for m in record['members'].split(',') if m])
            expected = f'| `{identity}` | {record["status"]} | {count} |'
            assert expected in text, ('stale reference inventory', identity)
    for path in root.glob('specific_highlights_*.md'):
        text = path.read_text(encoding='utf-8')
        assert 'specific_highlights_index.md' in text, ('missing backlink', path)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if '://' not in target:
                assert (path.parent / target.split('#')[0]).exists(), ('broken link', path, target)
    assert not (root / 'specific_highlights.md').exists()
    assert not (root / 'specific_highlights_proposal.md').exists()
    print(f'PASS: {len(concepts)} concepts, {len(contexts)} contexts, {len(refs)} references; '
          f'{len(keys)} historical registry keys; complete scoped unions and documentation links.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    check(parser.parse_args().root)
