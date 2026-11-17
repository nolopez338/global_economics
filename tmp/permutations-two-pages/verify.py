from pathlib import Path
import re, json
from PIL import Image, ImageChops
from pypdf import PdfReader
base=Path('tmp/permutations-two-pages')
a=(base/'original.tex').read_text(); b=Path('book2026-2027/olympiad/permutations1.tex').read_text()
# Remove exactly the new layout-only wrapper, then restore the three changed reservations/breaks.
start=b.index('% Compact opening only;'); end=b.index('\\vspace*{0pt}',start)
c=b[:start]+b[end:]
c=c.replace('\\clearpage\n\\endgroup\n\\restoregeometry\n','\\clearpage\n')
c=c.replace('\\stageheading{Worked Examples}', '\\clearpage\n\\stageheading{Worked Examples}')
c=c.replace('\\stageheading{1. Progressive Problems}', '\\clearpage\n\\stageheading{1. Progressive Problems}')
c=c.replace('\\Needspace{3\\baselineskip}', '\\Needspace{15\\baselineskip}')
assert re.sub(r'\s+','',a)==re.sub(r'\s+','',c), 'Source content differs'
assert a.split('\\stageheading{3. Solutions}',1)[1]==b.split('\\stageheading{3. Solutions}',1)[1]
old=PdfReader(base/'original.pdf'); new=PdfReader('book2026-2027/olympiad/permutations1.pdf')
assert len(new.pages)==9
assert '3. Solutions' in new.pages[2].extract_text()
comparisons=[]
for n in range(3,10):
    im1=Image.open(base/f'before-{n+1:02}.png').convert('RGB')
    im2=Image.open(base/f'final-{n}.png').convert('RGB')
    # Exclude only the footer page numeral, which necessarily decreases by one.
    region=(0,0,im1.width,940)
    same=ImageChops.difference(im1.crop(region),im2.crop(region)).getbbox() is None
    comparisons.append(same)
assert all(comparisons),comparisons
report={'source_preservation':'PASS: reversing only declared layout edits reproduces original source (whitespace ignored)', 'solutions_source':'byte-for-byte unchanged after heading', 'pages':len(new.pages), 'solutions_begin_page':3, 'solution_page_render_comparisons':comparisons,'font_size':'original 11pt retained', 'paper':'letter'}
(base/'verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
