from pathlib import Path
from pypdf import PdfReader
import pdfplumber
import re
import json

root = Path(__file__).resolve().parent
pdfpath = root / 'G11_T2_L1_C2_practice.pdf'
reader = PdfReader(pdfpath)
named = reader.named_destinations
aux = (root / 'G11_T2_L1_C2_practice.aux').read_text(encoding='utf-8')
labels = {}
for name, number, page, title, dest in re.findall(
    r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}', aux
):
    labels[name] = (number, int(page), title, dest)

links = []
for i, page in enumerate(reader.pages, 1):
    for annotation in page.get('/Annots', []):
        obj = annotation.get_object()
        action = obj.get('/A', {})
        if action.get('/S') == '/GoTo':
            dest = action['/D']
            assert not isinstance(dest, str) or dest in named, (i, dest)
            links.append((i, dest))

problem = labels['prob:c2-compare-three']
assert problem[0] == '3.4'
assert labels['prob:c2-4'][0] == '4.1'
assert labels['prob:c2-5'][0] == '4.2'
for key in ['prob:c2-compare-three', 'sol:c2-2-b'] + [
    'sol:c2-compare-three-' + task for task in 'abc'
]:
    number, page, title, dest = labels[key]
    assert reader.get_destination_page_number(named[dest]) + 1 == page

for task in 'abc':
    key = 'sol:c2-compare-three-' + task
    _, page, title, dest = labels[key]
    assert (problem[1], dest) in links, ('task link', key)
    for target in ['toc', 'prob:c2-compare-three', 'sec:general-worked']:
        assert (page, labels[target][3]) in links, ('return link', key, target)

assert (labels['sec:general-worked'][1], problem[3]) in links
assert [labels[key][0] for key in [
    'sec:introduction', 'sec:notation-and-procedure', 'sec:general-worked', 'sec:advanced'
] if key in labels] == ['1', '2', '3', '4']

with pdfplumber.open(pdfpath) as pdf:
    pages = {}
    for key in ['prob:c2-compare-three','sol:c2-2-b'] + [
        'sol:c2-compare-three-' + task for task in 'abc'
    ]:
        page = labels[key][1]
        text = pdf.pages[page - 1].extract_text() or ''
        pages[key] = page
        (root / (key.replace(':', '-') + '.txt')).write_text(text, encoding='utf-8')
    prompt = pdf.pages[problem[1] - 1].extract_text()
    assert all(option in prompt for option in ['A.', 'B.', 'C.', 'D.'])

summary = dict(pages=len(reader.pages), named_destinations=len(named),
               valid_internal_links=len(links), checked_pages=pages,
               numbering='3.4, 4.1, 4.2', task_and_return_links='verified')
(root / 'verification.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
