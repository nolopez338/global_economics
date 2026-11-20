"""One-off checks for the revised C4 activity; not a reusable validator."""
from pathlib import Path
from pypdf import PdfReader
import re, math
from collections import Counter

base = Path(__file__).parent
pdf = PdfReader(base / 'G11_T2_L1_C4_practice.pdf')
off = PdfReader(base / 'highlights-off.pdf')
destinations = pdf.named_destinations
links = Counter()
for page in pdf.pages:
    for annotation in page.get('/Annots', []):
        a = annotation.get_object()
        action = a.get('/A', {})
        if action.get('/S') == '/GoTo':
            target = action['/D']
            assert target in destinations, target
            destination = destinations[target]
            assert 0 <= pdf.get_destination_page_number(destination) < len(pdf.pages)
            links[target] += 1
aux = (base / 'G11_T2_L1_C4_practice.aux').read_text()
labels = re.findall(r'\\newlabel\{([^}]+)\}\{\{[^}]*\}\{(\d+)\}\{([^}]*)\}\{([^}]+)\}', aux)
for label, page, title, target in labels:
    assert target in destinations, label
    assert pdf.get_destination_page_number(destinations[target]) + 1 == int(page), label
    if label.startswith(('sol:', 'prob:', 'ex:')) or label in ('toc', 'sec:general-worked', 'sec:advanced'):
        assert links[target], label
    print(label, '-> page', page, '->', title)

# Check exact quantities and all interval constructions used in the activity.
for mean, sd, n, z, expected in [
    (420,50,100,1.96,(410.2,429.8)),
    (410,80,64,1.96,(390.4,429.6)),
    (410,80,64,2.576,(384.24,435.76)),
    (410,80,256,1.96,(400.2,419.8)),
    (74,12,36,2.576,(68.848,79.152)),
    (120,27,81,1.645,(115.065,124.935)),
    (120,27,81,1.96,(114.12,125.88)),
    (60,16,64,1.96,(56.08,63.92)),
    (60,12,64,1.96,(57.06,62.94)),
    (60,12,64,2.576,(56.136,63.864)),
]:
    margin = z*sd/math.sqrt(n)
    assert all(math.isclose(a,b,abs_tol=1e-9) for a,b in zip((mean-margin,mean+margin),expected))
assert math.isclose((2.576*12/5.152)**2,36)
assert math.isclose(4.935*math.sqrt(81)/1.645,27)
assert math.isclose((1.96*16/3.92)**2,64)
assert math.isclose(2.94*8/1.96,12)
assert round(410-1.96*80/math.sqrt(60)) == 390
assert round(410+1.96*80/math.sqrt(60)) == 430
assert math.isclose((1.96*80/20)**2,61.4656)

# Styling may affect extraction order/spacing, so compare the character inventory.
on_text = ''.join(p.extract_text() for p in pdf.pages)
off_text = ''.join(p.extract_text() for p in off.pages)
on_chars = Counter(re.sub(r'\s+', '', on_text))
off_chars = Counter(re.sub(r'\s+', '', off_text))
# These exact differences are TeX math-font extraction artifacts: three radical
# glyphs and a scalable parenthesis pair. The rendered formulas are inspected.
assert on_chars-off_chars == Counter({'p': 3, '!': 1}), on_chars-off_chars
assert off_chars-on_chars == Counter({'\u221a': 3, '\x12': 1, '\x13': 1}), off_chars-on_chars
print('PASS:', len(pdf.pages), 'pages;', sum(links.values()), 'internal link annotations;', len(labels), 'labels; calculations and highlight-off content retained.')
