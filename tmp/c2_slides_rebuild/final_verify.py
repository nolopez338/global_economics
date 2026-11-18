from pathlib import Path
import re,xml.etree.ElementTree as ET
from PIL import Image,ImageChops
base=Path('tmp/c2_slides_rebuild')
a=(base/'final.txt').read_text(encoding='utf8'); b=(base/'disabled_full.txt').read_text(encoding='utf8')
na,nb=re.sub(r'\s+','',a),re.sub(r'\s+','',b)
if na!=nb:
 import difflib
 print('Toggle text diff:', '\n'.join(list(difflib.unified_diff(a.splitlines(),b.splitlines()))[:30]))
else: print('PASS: enabled and disabled PDF text identical after whitespace normalization.')
root=ET.parse(base/'final_geometry.html').getroot(); pages=root.findall('.//{*}page')
frames=[tuple(map(int,x)) for x in re.findall(r'framepages \{(\d+)\}\{(\d+)\}',(base/'next.nav').read_text())]
for fi,(a,b) in enumerate(frames,1):
 if a==b:continue
 token='Study' if fi==13 else 'Symbol'
 coords=[[(round(float(w.attrib['xMin']),2),round(float(w.attrib['yMin']),2)) for w in p.findall('.//{*}word') if w.text==token and float(w.attrib['xMin'])<100] for p in pages[a-1:b]]
 assert all(c==coords[0] for c in coords),(fi,coords)
print('PASS: stable table-heading geometry across all overlays; 16 logical frames /',len(pages),'PDF pages.')
assert len(pages)==67
assert '16/16' in (base/'final.txt').read_text().split('\f')[-2]
assert Path('book2026-2027/grade11/term_2/3-slides/G11_T2_L1_C2_slides.tex').read_bytes()==(base/'next.tex').read_bytes()
print('PASS: delivered source matches compiled source; settled final frame total.')
