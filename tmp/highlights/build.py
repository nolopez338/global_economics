from pathlib import Path
import subprocess,hashlib
root=Path.cwd(); build=root/'tmp/highlights'; src=root/'book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C1_practice_activity.tex'
prev=None
for i in range(1,6):
 r=subprocess.run(['pdflatex','-interaction=batchmode','-halt-on-error','-output-directory='+str(build),src.name if i>1 else str(src)],cwd=src.parent if i>1 else root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if r.returncode: raise RuntimeError(r.stdout.decode(errors='replace'))
 state=tuple((build/(src.stem+ext)).read_bytes() for ext in ['.aux','.toc'])
 log=(build/(src.stem+'.log')).read_text(errors='replace')
 print('Pass',i,'from', 'activity directory' if i>1 else 'repository root',flush=True)
 if state==prev and 'Rerun to get' not in log and 'undefined references' not in log:break
 prev=state
else: raise RuntimeError('Did not stabilize')
for line in log.splitlines():
 if any(t in line for t in ['Overfull','Underfull','Warning:','Output written']):print(line)
subprocess.run(['pdftoppm','-scale-to','1100','-png',str(build/(src.stem+'.pdf')),str(build/'page')],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
from PIL import Image,ImageOps,ImageDraw
files=sorted(build.glob('page-*.png'))
w=340; tiles=[]
for f in files:
 im=Image.open(f).convert('RGB'); im.thumbnail((w,470))
 tile=Image.new('RGB',(w,500),'#dddddd');tile.paste(im,((w-im.width)//2,20));ImageDraw.Draw(tile).text((8,480),f.stem,fill='black');tiles.append(tile)
for k in range(0,len(tiles),4):
 sheet=Image.new('RGB',(w*4,500),'white')
 for j,t in enumerate(tiles[k:k+4]):sheet.paste(t,(j*w,0))
 sheet.save(build/f'contact-{k//4+1}.png')
print('Rendered',len(files),'pages',flush=True)
