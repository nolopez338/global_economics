"""Check actual PVC downloads after pvc-pdf.browser.cjs. Requires pypdf."""
import re
import sys
from pathlib import Path
from pypdf import PdfReader

folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('tmp/pdfs/pvc-export')
def drawn_images(page):
    resources = page['/Resources']['/XObject']
    return [resources[args[0]].get_object() for args, op in page.get_contents().operations if op == b'Do']


for name in ['frame', 'mixed-cm', 'compact', 'committed']:
    reader = PdfReader(folder / f'{name}.pdf')
    assert len(reader.pages) == 3, name
    for page in reader.pages:
        assert abs(float(page.mediabox.width) - 595.28) < 0.1
        assert abs(float(page.mediabox.height) - 841.89) < 0.1
    text = reader.pages[0].extract_text()
    assert 'Cut lengths include the tube inserted into fitting sockets.' in text
    for page, labels in zip(reader.pages[1:], [
        ['Front', 'Back', 'Left', 'Right'],
        ['Top', 'Bottom', 'Isometric front-right', 'Isometric rear-left'],
    ]):
        assert all(label in page.extract_text().splitlines() for label in labels), name
        images = drawn_images(page)
        assert len(images) == 4, (name, len(images))
        assert all((im['/Width'], im['/Height']) == (1092, 1218) for im in images)
        transform = None
        for args, op in page.get_contents().operations:
            if op == b'cm':
                transform = args
            if op == b'Do':
                assert transform is not None
                assert abs(float(transform[0]) / float(transform[3]) - 1092 / 1218) < 1e-8

    assert all((im['/Width'], im['/Height']) == (450, 300) for im in drawn_images(reader.pages[0]))
    if name == 'frame':
        assert 'Total pieces: 8' in text and 'Total tube cut length: 1800 mm' in text
        assert re.search(r'90° elbow\s+2 sockets\s+For OD 32 mm\s+4', text)
        for length in [350, 550]:
            assert re.search(rf'Cut {length} mm\nOD 32 mm\n2', text)
    elif name == 'mixed-cm':
        assert 'Total pieces: 11' in text and 'Total tube cut length: 154.69120001 cm' in text
        for length in ['12.3456', '12.34560001', '65']:
            assert f'Cut {length} cm' in text
        assert re.search(r'Cut 65 cm\nOD 3.2 cm\n2', text)
        assert len({args[0] for args, op in reader.pages[0].get_contents().operations if op == b'Do'}) == 8  # All catalog types, tubes reuse one reference.
    elif name == 'compact':
        assert 'Total pieces: 20' in text and 'Total tube cut length: 1790 mm' in text
        assert text.count('Reference') == 2
        assert all(f'Cut {i} mm' in text for i in range(80, 100))
    else:
        assert 'Cut 500 mm' in text and '800 mm' not in text
        assert 'Total pieces: 1' in text
    print(f'PASS {name}: A4 portrait, 3 pages, complete materials and 8 print-resolution views')
