import csv, io, json, hashlib, unicodedata
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

ROOT = Path(__file__).resolve().parents[3]
WORK = Path(__file__).resolve().parent
FOLDER = ROOT / 'book2026-2027/seminars/term_1/second_learning_evidence'
TARGET = FOLDER / 'resultados_criterios.csv'
raw = TARGET.read_bytes()
encoding = 'utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8'
source = raw.decode(encoding)  # Strict decoding, no replacement of roster characters.
delimiter = csv.Sniffer().sniff(source[:source.index('\n')], delimiters=',;\t').delimiter
parsed = list(csv.reader(io.StringIO(source, newline=''), delimiter=delimiter))
header, rows = parsed[0], [r for r in parsed[1:] if r]
assert all(len(r) == len(header) for r in rows)
original = [dict(zip(header, row)) for row in rows]
checklists = json.loads((WORK / 'checklists.json').read_text(encoding='utf-8'))
def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.upper()) if not unicodedata.combining(c)).split()
def match(name):
    words = set(norm(name))
    return [i for i, row in enumerate(original) if words <= set(norm(row['ESTUDIANTES']))]
def percentage(n, d):
    return str((Decimal(100)*n/d).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)).rstrip('0').rstrip('.')+'%'

# IDs are criterion + one-based checklist position. Every credit includes a page/location.
assessments = [
 {'pdf':'Proyecto_C7-C8.pdf', 'members':['Sebastián González Mojica','Emilio José Barón Romero'],
  'guides':['C7C8-Activity.tex'],
  'evidence':{
   'C7':{str(i): ('pp.2-3 sections 1.1-1.5' if i != 7 else 'p.3 concrete adjustment and reason') for i in range(1,9)},
   'C8':{str(i): ('pp.4-5 table, complementarity and K-specific pending verification; sources p.6') for i in range(1,14)}},
  'notes':'C5/C6 are cited as previously completed sources, not reproduced assessment sections; existing results preserved. Named interviewees on p.6 are sources, not group members.'},
 {'pdf':'Encuesta_SBLM (2).pdf', 'members':['Patrik Ayala','Gabriel Galan'],
  'guides':['C5C6-Activity.tex'],
  'evidence':{
   'C5':{'1':'pp.1-2 integrated user/context and observation-response-conclusion tables','2':'p.1 users cycle V; p.2 anonymous grade 10 profiles','3':'p.2 reduce lost break time', '5':'pp.1-2 queueing, collection, queue jumping and conflict', '7':'pp.1-2 Asobartolina, break, students/personnel, infrastructure','8':'pp.1-2 user selection and survey profile','9':'p.2 learned conclusions','11':'p.2 observation and user-response columns support conclusions'},
   'C6':{'10':'p.2 supported need and strongest evidence: grade 10 testimonies, waiting and conflicts','11':'p.2 chosen improvement: reduce time lost during break, contrasted with excessive waiting'}},
  'notes':'Explicit C5-C6 heading plus contextual evidence identify the intended stage despite older listening/survey task structure. No two-option comparison, codes, ratings, feasibility, totals or limitation. Credit substantive evidence/benefit discussion wherever it appears; missing requirements incomplete.'},
 {'pdf':'pedro_y_tape.pdf', 'members':['Pedro','Santiago'],
  'guides':['C5C6-Activity.tex','C7C8-Activity.tex'],
  'evidence':{
   'C5':{'1':'pp.1-2 integrated user/context and observation-response-conclusion tables','2':'p.1 grade 10 bathroom users','3':'p.2 clean, hygienic, comfortable bathrooms','5':'pp.1-2 using and avoiding bathrooms','7':'pp.1-2 school bathrooms, school day, students/community, facilities','8':'pp.1-2 frequent users and survey profile','9':'p.2 learned conclusions','11':'p.2 observation and testimony columns support conclusions'},
   'C6':{'10':'pp.2-3 strongest evidence and most important need: observations/testimonies of dirty bathrooms','11':'pp.2-3 comfort/hygiene benefit and avoiding bathrooms as consequence of poor conditions'},
   'C7':{'1':'p.3 agreed D1 question','2':'p.3 grade 10 students','3':'p.3 cleanliness, odor, condition and comfort','4':'p.3 school bathrooms during school day','6':'p.3 review explicitly cites observations/testimonies; uncoded findings are substantive evidence attempt'},
   'C8':{str(i):'p.3 discipline table, contextual justifications, class/institutional sources and complementarity paragraph' for i in [1,2,3,4,5,7,8,9,10,11,13]}},
  'notes':'Title C3-C8 and p.4 declaration identify cumulative C5-C8 scope; no C1-C4 updates. Neither K connection states limits/pending verification. D1 lacks a reference to a prioritized opportunity, concrete review adjustment/reason, or excluded/provisional scope. Pedro uniquely matches row 22. Santiago has two candidates (rows 21 and 25); neither updated without confirmation.'}
]

proposed = [r.copy() for r in original]
allowed = set()
pending = []
staged = []
for assessment in assessments:
    url = (FOLDER/assessment['pdf']).resolve().as_uri()
    assert (FOLDER/assessment['pdf']).is_file()
    results = {}
    for criterion, evidence in assessment['evidence'].items():
        total = len(checklists[criterion]); count = len(evidence)
        assert all(1 <= int(k) <= total for k in evidence)
        results[criterion] = {'completed':count,'required':total,'percentage':percentage(count,total),'result':'Yes' if 10*count >= 6*total else 'No'}
    for member in assessment['members']:
        matches = match(member)
        if len(matches) != 1:
            pending.append({'pdf':assessment['pdf'],'name':member,'candidates':[original[i]['ESTUDIANTES'] for i in matches], 'criteria':list(results)})
            continue
        i = matches[0]
        for criterion, result in results.items():
            for column, value in [(criterion,result['result']),(criterion+'P',result['percentage'])]:
                assert (i,column) not in allowed, 'Conflicting staged submissions'
                proposed[i][column] = value; allowed.add((i,column))
        old_links = original[i]['ENLACE_ACTIVIDAD']
        links = old_links.splitlines()
        proposed[i]['ENLACE_ACTIVIDAD'] = old_links if url in links else old_links + ('\n' if old_links else '') + url
        allowed.add((i,'ENLACE_ACTIVIDAD'))
        staged.append({'row':original[i]['No'],'name':original[i]['ESTUDIANTES'],'pdf':assessment['pdf'],'results':results,'url':url})

# Snapshot and reviewable staging before replacement.
(WORK/'original.csv').write_bytes(raw)
(WORK/'staged_updates.json').write_text(json.dumps({'updates':staged,'unresolved':pending,'assessments':assessments},ensure_ascii=False,indent=2),encoding='utf-8')
newline = '\r\n' if source.count('\r\n') > source.count('\n')/2 else '\n'
buf = io.StringIO(newline='')
writer = csv.writer(buf,delimiter=delimiter,lineterminator=newline)
writer.writerow(header)
writer.writerows([[row[h] for h in header] for row in proposed])
# Preserve any original terminal blank lines.
trailing = source[len(source.rstrip('\r\n')):]
candidate = (buf.getvalue().rstrip('\r\n')+trailing).encode(encoding)
stage_path = WORK/'staged.csv'
stage_path.write_bytes(candidate)

def validate(data):
    assert data.startswith(b'\xef\xbb\xbf') == raw.startswith(b'\xef\xbb\xbf')
    text = data.decode(encoding)
    assert csv.Sniffer().sniff(text.splitlines()[0],delimiters=',;\t').delimiter == delimiter
    records = list(csv.reader(io.StringIO(text,newline=''),delimiter=delimiter))
    out_header, out_rows = records[0], [r for r in records[1:] if r]
    assert out_header == header
    pcols = [f'C{i}P' for i in range(1,11)]
    pos = out_header.index('C10')+1
    assert out_header[pos:pos+10] == pcols
    assert all(out_header.count(c)==1 for c in pcols+['ENLACE_ACTIVIDAD'])
    assert len(out_rows)==len(rows)
    diffs=[]
    for i,(before,after) in enumerate(zip(rows,out_rows)):
        assert len(after)==len(header)
        for j,(a,b) in enumerate(zip(before,after)):
            if a != b:
                assert (i,header[j]) in allowed, (i,header[j])
                diffs.append((original[i]['No'],header[j],a,b))
        assert after[header.index('ESTUDIANTES')]==before[header.index('ESTUDIANTES')]
        assert all(dict(zip(header,after))[h]==proposed[i][h] for h in header)
        assert set(original[i]['ENLACE_ACTIVIDAD'].splitlines()) <= set(proposed[i]['ENLACE_ACTIVIDAD'].splitlines())
    for update in staged:
        i = next(i for i,r in enumerate(original) if r['No']==update['row'])
        for c, r in update['results'].items():
            assert r['result']==('Yes' if 10*r['completed']>=6*r['required'] else 'No')
            assert r['percentage']==percentage(r['completed'],r['required'])
            assert proposed[i][c]==r['result'] and proposed[i][c+'P']==r['percentage']
        assert update['url'] in proposed[i]['ENLACE_ACTIVIDAD'].splitlines()
    return diffs

diffs = validate(stage_path.read_bytes())
assert TARGET.read_bytes()==raw, 'Source changed since snapshot'
TARGET.write_bytes(candidate)
assert TARGET.read_bytes()==candidate
assert validate(TARGET.read_bytes())==diffs
summary={'encoding':encoding,'delimiter':delimiter,'rows':len(rows),'updated_rows':len(set(u['row'] for u in staged)),'changed_cells':len(diffs),'original_sha256':hashlib.sha256(raw).hexdigest(),'written_sha256':hashlib.sha256(candidate).hexdigest(),'unresolved':pending,'updates':staged}
(WORK/'validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
report=['# Seminar assessment audit','', 'Completion only. Exact threshold: 10 × completed ≥ 6 × required. All 13 pages were extracted and visually inspected.','', '## Fixed checklists (established before PDF review)','']
for c, items in checklists.items():
    report += [f'### {c} — {len(items)} required','']+[f'- {c}.{i:02}: {item}' for i,item in enumerate(items,1)]+['']
for a in assessments:
    report += [f"## {a['pdf']}",'', 'Named members: '+', '.join(a['members']), 'Guides: '+', '.join(a['guides']), '',a['notes'],'']
    for c, ev in a['evidence'].items():
        n,d=len(ev),len(checklists[c])
        report += [f"### {c}: {n}/{d}, {percentage(n,d)}, {'Yes' if 10*n>=6*d else 'No'}",'']
        for i in range(1,d+1):
            report.append(f"- {c}.{i:02}: "+('Complete — '+ev[str(i)] if str(i) in ev else 'Incomplete — no substantive response to the full checklist item.'))
        report += ['']
report += ['## Unresolved','',json.dumps(pending,ensure_ascii=False,indent=2),'','## Validation','',f"Passed before and after writing: {len(rows)} rows, {len(set(u['row'] for u in staged))} updated students, {len(diffs)} changed cells; UTF-8, comma delimiter, headers, row order, roster names, existing links and every unrelated cell preserved."]
(WORK/'assessment-report.md').write_text('\n'.join(report),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
