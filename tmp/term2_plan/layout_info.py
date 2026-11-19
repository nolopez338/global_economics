from docx import Document
from pathlib import Path
from lxml import etree
p=Path('book2026-2027/grade11/PGF-02-R39PLANEACION PERIODICA DE LA ENSENANZA - G11 - T2 - T41.docx');d=Document(p)
for i,t in enumerate(d.tables):
 if i in (8,9,10,11,20,21,22,23,24):
  print('TABLE',i,'rows',len(t.rows))
  for r in t.rows:print('trPr',r._tr.trPr.xml if r._tr.trPr is not None else None)
print('TOP LEVEL PARAGRAPHS')
for i,p in enumerate(d.paragraphs):
 print(i,repr(p.text),p._p.xml[:1400])
