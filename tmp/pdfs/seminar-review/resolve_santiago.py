import csv, io, json, hashlib
from pathlib import Path

work = Path(__file__).resolve().parent
root = work.parents[2]
target = root / 'book2026-2027/seminars/term_1/second_learning_evidence/resultados_criterios.csv'
raw = target.read_bytes()
text = raw.decode('utf-8')
records = list(csv.reader(io.StringIO(text, newline='')))
header = records[0]
rows = [r for r in records[1:] if r]
before = [r.copy() for r in rows]
name_col = header.index('ESTUDIANTES')
matches = [i for i,r in enumerate(rows) if r[name_col] == 'TAPIAS LÓPEZ SANTIAGO']
assert len(matches) == 1
i = matches[0]
validation = json.loads((work/'validation.json').read_text(encoding='utf-8'))
pedro = next(u for u in validation['updates'] if u['row'] == '22')
assert pedro['pdf'] == 'pedro_y_tape.pdf'
allowed = {header.index(c) for c in ['C5','C5P','C6','C6P','C7','C7P','C8','C8P','ENLACE_ACTIVIDAD']}
for criterion,result in pedro['results'].items():
    assert result['result'] == ('Yes' if 10*result['completed'] >= 6*result['required'] else 'No')
    rows[i][header.index(criterion)] = result['result']
    rows[i][header.index(criterion+'P')] = result['percentage']
link_col = header.index('ENLACE_ACTIVIDAD')
url = pedro['url']
assert url == (target.parent/'pedro_y_tape.pdf').resolve().as_uri()
if url not in rows[i][link_col].splitlines():
    rows[i][link_col] += ('\n' if rows[i][link_col] else '') + url
buf = io.StringIO(newline='')
newline = '\r\n' if text.count('\r\n') > text.count('\n')/2 else '\n'
writer = csv.writer(buf,lineterminator=newline)
writer.writerow(header); writer.writerows(rows)
trailing = text[len(text.rstrip('\r\n')):]
candidate = (buf.getvalue().rstrip('\r\n')+trailing).encode('utf-8')
(work/'before-identity-resolution.csv').write_bytes(raw)
(work/'identity-resolution-staged.csv').write_bytes(candidate)
def verify(data):
    parsed = list(csv.reader(io.StringIO(data.decode('utf-8'),newline='')))
    assert parsed[0] == header
    actual = [r for r in parsed[1:] if r]
    assert actual == rows and len(actual) == len(before) == 25
    changes=[]
    for rownum,(a,b) in enumerate(zip(before,actual)):
        for colnum,(old,new) in enumerate(zip(a,b)):
            if old != new:
                assert rownum == i and colnum in allowed
                changes.append(header[colnum])
        assert set(a[link_col].splitlines()) <= set(b[link_col].splitlines())
    pos=header.index('C10')+1
    assert header[pos:pos+10] == [f'C{j}P' for j in range(1,11)]
    assert header.count('ENLACE_ACTIVIDAD') == 1
    return changes
changes = verify(candidate)
assert target.read_bytes() == raw
target.write_bytes(candidate)
assert verify(target.read_bytes()) == changes
resolved = dict(pedro,row='25',name='TAPIAS LÓPEZ SANTIAGO')
validation['updates'].append(resolved)
validation['unresolved'] = []
validation['updated_rows'] = 6
validation['changed_cells'] += len(changes)
validation['written_sha256'] = hashlib.sha256(candidate).hexdigest()
validation['identity_resolution'] = 'User confirmed Pedro = RAMÍREZ BARRERO PEDRO MARTIN and Santiago = TAPIAS LÓPEZ SANTIAGO.'
(work/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
stage=json.loads((work/'staged_updates.json').read_text(encoding='utf-8'))
stage['updates'].append(resolved); stage['unresolved']=[]
stage['identity_resolution']=validation['identity_resolution']
(work/'staged_updates.json').write_text(json.dumps(stage,ensure_ascii=False,indent=2),encoding='utf-8')
report=work/'assessment-report.md'
content=report.read_text(encoding='utf-8')
content += '\n\n## Identity resolved by user\n\nThe user confirmed Pedro as RAMÍREZ BARRERO PEDRO MARTIN and Santiago as TAPIAS LÓPEZ SANTIAGO. Row 25 now receives the same C5–C8 results and supporting PDF link as Pedro. The earlier unresolved note is superseded; no unresolved cases remain. Reparsed and validated before and after writing: only row 25 C5/C5P–C8/C8P and ENLACE_ACTIVIDAD changed (9 cells); all other cells, existing links, encoding, delimiter, column layout, names and row order preserved. Total updated students: 6.\n'
report.write_text(content,encoding='utf-8')
print(json.dumps({'student':resolved['name'],'results':resolved['results'],'changed_cells':changes,'unresolved':[]},ensure_ascii=False,indent=2))
