from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
b=Path('.exam-build-check/c8c9c10-solution')
files=sorted(b.glob('page-*.png'))
for start in range(0,len(files),4):
 sheet=Image.new('RGB',(1300,1720),'#b0b0b0')
 for j,p in enumerate(files[start:start+4]):
  im=Image.open(p);im.thumbnail((640,820)); x=(j%2)*650;y=(j//2)*860
  sheet.paste(im,(x,y+25));ImageDraw.Draw(sheet).text((x+10,y+5),p.stem,fill='black')
 sheet.save(b/f'contact-{start//4}.png')
