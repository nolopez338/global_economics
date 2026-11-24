from pathlib import Path
from pypdf import PdfReader
import re
folder=Path('tmp/c4-solution-statements')
r=PdfReader(folder/'final/G11_T2_L1_C4_practice.pdf')
destinations=r.named_destinations
alltext='\n'.join(p.extract_text() for p in r.pages)
assert alltext.count('Problem statement with concept highlights.')==11
links=0
for page in r.pages:
 for ref in page.get('/Annots',[]):
  a=ref.get_object(); action=a.get('/A',{})
  target=a.get('/Dest') or (action.get('/D') if action.get('/S')=='/GoTo' else None)
  if isinstance(target,str):
   assert target in destinations,target
   links+=1
aux=(folder/'final/G11_T2_L1_C4_practice.aux').read_text(encoding='utf-8')
for label, page, destination in re.findall(r'\\newlabel\{(sol:c4-[^}]+)\}\{\{[^}]*\}\{(\d+)\}\{[^}]*\}\{([^}]+)\}',aux):
 assert destination in destinations,label
 d=destinations[destination]
 actual=r.get_destination_page_number(d)
 assert actual==int(page)-1,(label,actual,page)
 assert 'Problem statement with concept highlights.' in r.pages[actual].extract_text(),label
 print(label+': destination verified on page '+page)
print(f'{len(r.pages)} pages; 11 rendered copies; {links} internal links resolve.')
log=(folder/'final/G11_T2_L1_C4_practice.log').read_text(encoding='utf-8')
assert not re.search(r'Overfull|Underfull|LaTeX Warning|^!',log,re.M)
print('Final build log clean.')
