from pathlib import Path
from docx import Document
from lxml import html
import json,re
root=Path.cwd(); out=root/'tmp/term2_plan'
p= root/'book2026-2027/grade11/PGF-02-R39PLANEACION PERIODICA DE LA ENSENANZA - G11 - T2 - T41.docx'
d=Document(p)
lines=[]
for i,t in enumerate(d.tables):
 for j,row in enumerate(t.rows):
  lines.append(f'TABLE {i} ROW {j}')
  for k,c in enumerate(row.cells):
   lines.append(f'CELL {k}: '+c.text)
(out/'document.txt').write_text('\n'.join(lines),encoding='utf8')
ref=(root/'book2026-2027/grade11/PGF-02-R39PLANEACION PERIODICA DE LA ENSENANZA ELEVENTH GRADE FIRST TERM.md').read_text(encoding='utf8')
ref=re.sub(r'!\[.*?\]\(data:image/.*?\)', '[image]',ref)
(out/'reference.txt').write_text(ref,encoding='utf8')
soup=html.fromstring((root/'grade11/src/G11_T2.html').read_text(encoding='utf8'))
links=[]
for a in soup.xpath('//a[@href]'):
 if re.match(r'C\d+\s*[–-]',a.text_content()):
  target=(root/'grade11/src'/a.get('href')).resolve()
  links.append(dict(label=a.text_content(),href=a.get('href'),target=str(target),exists=target.exists()))
(out/'links.json').write_text(json.dumps(links,indent=2),encoding='utf8')
print(json.dumps(links,indent=2))

