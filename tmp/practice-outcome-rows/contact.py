from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
pages=[9,11,13,15,17,20,24,27,31,35,39]
canvas=Image.new('RGB',(1872,2460),'white')
for i,n in enumerate(pages):
 im=Image.open(f'tmp/practice-outcome-rows/row-{n}.png');im.thumbnail((460,600))
 x=(i%4)*468;y=(i//4)*820
 canvas.paste(im,(x,y));ImageDraw.Draw(canvas).text((x+10,y+605),str(n),fill='black')
canvas.save('tmp/practice-outcome-rows/final-review.png')
