from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
ps=list(Path('tmp/pdfs/c3-classroom').glob('final-*.png'))
for start in range(0,len(ps),4):
 group=ps[start:start+4]; canvas=Image.new('RGB',(1120,1500),'#ddd')
 for j,p in enumerate(group):
  im=Image.open(p);im.thumbnail((550,720));canvas.paste(im,((j%2)*560,(j//2)*750+25));ImageDraw.Draw(canvas).text(((j%2)*560+5,(j//2)*750+5),p.stem,fill='black')
 canvas.save(f'tmp/pdfs/c3-classroom/final-contact-{start//4}.png')

