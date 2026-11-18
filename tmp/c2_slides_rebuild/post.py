from pathlib import Path
from PIL import Image,ImageChops
base=Path('tmp/c2_slides_rebuild')
a=Image.open(base/'final_overlay-04.png'); b=Image.open(base/'final_overlay-67.png')
assert ImageChops.difference(a.crop((0,0,1100,585)),b.crop((0,0,1100,585))).getbbox() is None
print('PASS: opening and closing combined legends identical above footer.')
s=(base/'montage.py').read_text().replace("f'overlay-{n:02}.png'","f'final_overlay-{n:02}.png'")
(base/'final_montage.py').write_text(s)
