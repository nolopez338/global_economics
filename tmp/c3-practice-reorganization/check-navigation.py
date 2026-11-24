from pypdf import PdfReader
from pathlib import Path
import re,sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('tmp/c3-practice-reorganization/off/highlights-off.pdf')
aux=p.with_suffix('.aux').read_text()
labels={m[1]:(int(m[2]),m[3]) for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}\{[^}]*\}\{([^}]+)\}',aux)}
r=PdfReader(p)
names=r.named_destinations
expected=['sol:c3-'+k+'-'+t for k in ['inventory','coffee','energy','manufacturing','restaurant','agriculture'] for t in ['model','decision']]
print('Pages',len(r.pages),'destinations',len(names))
for k in expected:
 assert k in labels,k
 page,dest=labels[k]
 assert dest in names,dest
 pg=r.get_destination_page_number(names[dest]);txt=r.pages[pg].extract_text()
 assert pg+1==page
 assert ('Task 1' if k.endswith('model') else 'Task 2') in txt
 print(k,pg+1)
broken=[];count=0
for j,page in enumerate(r.pages):
 for ref in page.get('/Annots',[]):
  an=ref.get_object();act=an.get('/A',{})
  if act.get('/S')=='/GoTo':
   dest=act.get('/D');count+=1
   if isinstance(dest,str) and dest not in names:broken.append((j+1,dest))
assert not broken,broken
print('Resolved internal GoTo links:',count)
