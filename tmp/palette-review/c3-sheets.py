from pathlib import Path
from PIL import Image,ImageDraw
p=Path('tmp/palette-review/G10_T2_L1_C3_practice_activity');imgs=sorted(p.glob('page-*.png'))
for start in range(0,len(imgs),6):
 sheet=Image.new('RGB',(1500,2130),'#dddddd');draw=ImageDraw.Draw(sheet)
 for i,src in enumerate(imgs[start:start+6]):
  im=Image.open(src).convert('RGB');im.thumbnail((745,680));x=(i%2)*750;y=(i//2)*710;sheet.paste(im,(x,y+22));draw.text((x+5,y+3),src.stem,fill='black')
 sheet.save(p/('sheet-'+str(start//6+1)+'.png'))
