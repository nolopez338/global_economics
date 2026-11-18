from pathlib import Path
from PIL import Image, ImageChops
folder=Path(__file__).parent
images=[Image.open(folder/f'checkpoint-{i}.png').convert('RGB') for i in range(1,5)]
def rules(im):
    return [y for y in range(120,840) if sum(max(im.getpixel((x,y))) < 160 for x in range(560,1510)) > 900]
positions=[rules(im) for im in images]
assert all(r==positions[0] for r in positions), positions
initial=images[0]
unexpected=[(x,y) for y in range(169,822) if y not in positions[0] for x in range(822,1509) if min(initial.getpixel((x,y))) < 245]
assert not unexpected, unexpected[:10]
for i in (2,3):
    assert ImageChops.difference(images[1].crop((822,169,1509,234)),images[i].crop((822,169,1509,234))).getbbox() is None
assert ImageChops.difference(images[2].crop((822,238,1509,338)),images[3].crop((822,238,1509,338))).getbbox() is None
images[-1].convert('L').save(folder/'grayscale.png')
print('Verified: stationary table rules, initially blank answer cells, and unchanged completed point-estimate / margin-of-error entries.')
