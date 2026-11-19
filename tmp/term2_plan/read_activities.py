from pathlib import Path
from pypdf import PdfReader
import json
root=Path.cwd();out=root/'tmp/term2_plan'
for l in json.loads((out/'links.json').read_text()):
 if 'Practice Activity' not in l['label']:continue
 p=Path(l['target']); key=l['label'].split()[0]
 try:
  d=PdfReader(p);s='\n'.join(pg.extract_text() for pg in d.pages);kind='PDF'
 except Exception as e:
  p=list((root/'book2026-2027').rglob(p.with_suffix('.tex').name))[0];s=p.read_text(encoding='utf8');kind='TEX'
 (out/(key+'.txt')).write_text(s,encoding='utf8')
 print(key,kind,len(s))
