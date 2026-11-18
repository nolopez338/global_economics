import xml.etree.ElementTree as ET,re
from pathlib import Path
root=ET.parse('tmp/c2_slides_rebuild/geometry.html').getroot()
pages=root.findall('.//{*}page')
frames=[tuple(map(int,x)) for x in re.findall(r'framepages \{(\d+)\}\{(\d+)\}',Path('tmp/c2_slides_rebuild/lesson.nav').read_text())]
for fi,(a,b) in enumerate(frames,1):
 if a==b:continue
 coords=[]
 for p in pages[a-1:b]:
  coords.append([(round(float(w.attrib['xMin']),2),round(float(w.attrib['yMin']),2)) for w in p.findall('.//{*}word') if w.text=='Symbol'])
 print(fi,(a,b),'stable Symbol positions:',all(c==coords[0] for c in coords),coords[0])
