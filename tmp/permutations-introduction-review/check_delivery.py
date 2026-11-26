"""Document-specific audit for this counting-introduction revision."""
from pathlib import Path
import hashlib,json,re
from PIL import Image,ImageChops
import pypdfium2 as pdfium

here=Path(__file__).resolve().parent
root=here.parents[1]
deck=root/'book2026-2027/fundamentals/permutations1-introduction-slides.tex'
practice=root/'book2026-2027/fundamentals/permutations1.tex'
audit=json.loads((here/'outcome-audit.json').read_text())
assert deck.read_bytes()==(here/'lesson.tex').read_bytes()
assert hashlib.sha256(practice.read_bytes()).hexdigest()==audit['source_sha256']
assert audit['frames']==65 and len(audit['examples'])==15
source=deck.read_text(encoding='utf-8')
assert source.count(r'\begin{frame}')==65
assert not re.search(r'\\(?:input|include|includegraphics)\b',source)
assert not [c for c in source if ord(c)<32 and c not in '\r\n\t']
nav=(here/'lesson.nav').read_text()
ranges=[tuple(map(int,p)) for p in re.findall(r'\\beamer@framepages\s*\{(\d+)\}\{(\d+)\}',nav)]
assert len(ranges)==65 and ranges[-1][1]==248
assert r'\inserttotalframenumber {65}' in nav
for n in [1,2]:
    log=(here/f'final-compile-pass-{n}.txt').read_text(encoding='utf-16' if (here/f'final-compile-pass-{n}.txt').read_bytes().startswith(b'\xff\xfe') else 'utf-8',errors='replace')
    assert 'Output written on lesson.pdf (248 pages' in log
    assert not re.search(r'Overfull|LaTeX Error|Missing character|undefined|Rerun to get',log)
doc=pdfium.PdfDocument(here/'lesson.pdf')
assert len(doc)==248
for page in doc:
    w,h=page.get_size()
    assert abs(w/h-16/9)<.001
doc.close()
# Every page of the previous review was inspected. Assert pixel preservation
# outside the six explicitly repaired frames, then inspect the changed pages.
repaired_frames=[30,56,60,61,64,65]
allowed={p for f in repaired_frames for p in range(ranges[f-1][0],ranges[f-1][1]+1)}
changed=[]
for p in range(1,249):
    name=f'page-{p:03}.png'
    with Image.open(here/'final-review'/name) as before, Image.open(here/'delivery-review'/name) as after:
        if ImageChops.difference(before.convert('RGB'),after.convert('RGB')).getbbox():
            changed.append(p)
            assert p in allowed, f'Unexpected visual change on page {p}'
gray=here/'grayscale-review'
gray.mkdir(exist_ok=True)
for p in [33,41,71,97,117,122,147,194,219,235,248]:
    with Image.open(here/'delivery-review'/f'page-{p:03}.png') as im:
        im.convert('L').save(gray/f'page-{p:03}.png')
report={'logical_frames':65,'overlay_pages':248,'audited_examples':15,
        'original_source_sha256':audit['source_sha256'],
        'source_identical_to_compiled_copy':True,
        'standalone_build_passes':2,'unexpected_layout_diagnostics':False,
        'repaired_frames':repaired_frames,'changed_pages':changed,
        'other_pages_pixel_identical_to_inspected_review':True}
(here/'delivery-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
