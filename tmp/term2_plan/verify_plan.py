from pathlib import Path
from docx import Document
from urllib.parse import urlsplit,unquote
from lxml import html
from collections import Counter
root=Path.cwd();path=root/'book2026-2027/grade11/PGF-02-R39PLANEACION PERIODICA DE LA ENSENANZA - G11 - T2 - T41.docx'
d=Document(path);orig=Document(root/'tmp/term2_plan/original.docx')
expected={}
for a in html.fromstring((root/'grade11/src/G11_T2.html').read_text(encoding='utf8')).xpath('//a[@href]'):
 import re
 if re.match(r'C\d+\s*[–-]',a.text_content()):expected[a.text_content()]=((root/'grade11/src'/unquote(urlsplit(a.get('href')).path)).resolve(),urlsplit(a.get('href')).fragment)
cnt=Counter();missing=set()
for ti,ris in [(10,[0,1,2]),(22,[0,1]),(23,[0])]:
 for ri in ris:
  c=d.tables[ti].rows[ri].cells[1]
  for p in c.paragraphs:
   for h in p._p.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hyperlink'):
    text=''.join(h.itertext()) # use actual w:t only
    text=''.join(h.xpath('.//w:t/text()')); name=text.replace('Actividad de práctica','Practice Activity').replace('Actividad de clase','Classroom Activity').replace('Diapositivas','Slides')
    rel=d.part.rels[h.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
    s=urlsplit(rel.target_ref); actual=(path.parent/unquote(s.path)).resolve()
    assert (actual,s.fragment)==expected[name],(name,rel.target_ref)
    cnt[name]+=1
    if not actual.exists():missing.add(name)
assert len(cnt)==30 and set(cnt.values())=={2},cnt
for ti in [0,1,2,3,4,5,6,7,12,13,14,15,16,17,18,19,24]:assert d.tables[ti]._tbl.xml==orig.tables[ti]._tbl.xml,ti
for ti in [10,22,23]:
 for i,r in enumerate(d.tables[ti].rows):assert r.cells[0].text==orig.tables[ti].rows[i].cells[0].text
for a,b in [(d,orig)]:assert [s._sectPr.xml for s in a.sections]==[s._sectPr.xml for s in b.sections]
print('PASS: 30 intended resource targets, each linked in both languages (60 clickable hyperlinks).')
print('PASS: objectives, criteria, evidence groups, assessment arrangements, section layouts and all unrelated tables unchanged.')
print('Missing resource destinations retained:',len(missing))

