from pathlib import Path
import re
from fractions import Fraction
from pypdf import PdfReader

root = Path('tmp/c3-graph-labels-20261124')
target = Path('book2026-2027/grade10/term_2/1-practice_activities/G10_T2_L1_C3_practice_activity.tex')
before = (root / 'before.tex').read_text(encoding='utf-8')
after = target.read_text(encoding='utf-8')
assert before.split(r'\begin{document}', 1)[1] == after.split(r'\begin{document}', 1)[1]
assert '% \\GTenHighlightsfalse % Uncomment' in after
calls = re.findall(r'\\BreakEvenGraph\{(\d+)\}\{(-?\d+)\}\{(-?\d+)\}\{([^}]+)\}', after)
assert len(calls) == 18
assert calls == re.findall(r'\\BreakEvenGraph\{(\d+)\}\{(-?\d+)\}\{(-?\d+)\}\{([^}]+)\}', before)
for _, low, high, zero in calls:
    assert Fraction(low) + (Fraction(high) - Fraction(low)) * Fraction(zero) == 0
oldplots = re.findall(r'\\addplot[^\n]+', before)
newplots = re.findall(r'\\addplot[^\n]+', after)
assert [x.split(';')[0] for x in oldplots] == [x.split(';')[0] for x in newplots]
print('Source: body, all 18 graph arguments, plot data/styles and exact roots preserved; toggle enabled.')
for variant, filename in [('before', 'before.pdf'), ('on', 'on/G10_T2_L1_C3_practice_activity.pdf'), ('off', 'off/off.pdf')]:
    reader = PdfReader(root / filename)
    dests = reader.named_destinations
    links = []
    for i, page in enumerate(reader.pages):
        for annotation in page.get('/Annots', []):
            a = annotation.get_object()
            if a.get('/Subtype') != '/Link':
                continue
            d = a.get('/Dest')
            action = a.get('/A', {})
            if action.get('/S') == '/GoTo':
                d = action.get('/D')
            if d is not None:
                assert isinstance(d, str) and d in dests, (variant, i+1, d)
                p = reader.get_destination_page_number(dests[d])
                assert p is not None and 0 <= p < len(reader.pages)
                links.append((i+1, d, p+1))
    if variant == 'before':
        oldlinks = links
    elif variant == 'on':
        assert oldlinks == links, 'Enabled link mapping changed'
    print(variant, 'pages:', len(reader.pages), 'resolved links:', len(links), 'named destinations:', len(dests))
    if variant == 'on':
        print('Graph pages:', [i+1 for i,p in enumerate(reader.pages) if 'individual break-even analysis' in p.extract_text()])
