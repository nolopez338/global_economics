from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
base=Path('tmp/c2_slides_rebuild')
groups={'legends':[2,3,4,67],'task1':[6,7,8,11,12,13,14,18,20,21],'task2a':[22,23,24,25,26,27,28,29], 'task2b':[30,32,34,36,37,38,39,40], 'task2c':[41,42,43,45,46,47], 'task3a':[48,49,50,51,52,53,54,55,56], 'task3b':[57,58,59,60,61,62,63,64,65,66]}
for name, nums in groups.items():
 w,h=660,396; canvas=Image.new('RGB',(w*2,h*((len(nums)+1)//2)), 'white'); draw=ImageDraw.Draw(canvas)
 for j,n in enumerate(nums):
  im=Image.open(base/f'final_overlay-{n:02}.png'); im.thumbnail((w,h-22))
  x=(j%2)*w;y=(j//2)*h
  canvas.paste(im,(x,y+22));draw.text((x+8,y+4),f'PDF page {n}',fill='black')
 canvas.save(base/f'{name}_sheet.png')
