"""Verify real Person PDF downloads after pvc-person.browser.cjs (pypdf)."""
from pathlib import Path
from pypdf import PdfReader

folder = Path('tmp/pvc-person')
for name, count, length in [('mixed', 8, 1800), ('references-only', 0, 0)]:
    reader = PdfReader(folder / f'{name}.pdf')
    assert len(reader.pages) == 3
    text = reader.pages[0].extract_text()
    assert f'Total pieces: {count}' in text, text
    assert f'Total tube cut length: {length} mm' in text, text
    assert 'Scale references: 2' in text, text
    assert 'Person' not in text and 'silhouette' not in text
    assert 'Cut lengths include the tube inserted into fitting sockets.' in text
    if count:
        assert 'Straight tube' in text and '90° elbow' in text
    else:
        assert 'Straight tube' not in text and 'socket' not in text.split('Total pieces:')[0]
        assert 'No PVC construction materials.' in text
    for page in reader.pages:
        assert abs(float(page.mediabox.width) - 595.28) < .1
        assert abs(float(page.mediabox.height) - 841.89) < .1
    for page, labels in zip(reader.pages[1:], [
        ['Front', 'Back', 'Left', 'Right'],
        ['Top', 'Bottom', 'Isometric front-right', 'Isometric rear-left']
    ]):
        assert all(label in page.extract_text().splitlines() for label in labels)
        resources = page['/Resources']['/XObject']
        images = [resources[args[0]].get_object() for args, op in page.get_contents().operations if op == b'Do']
        assert len(images) == 4
        assert all((im['/Width'], im['/Height']) == (1092, 1218) for im in images)
    print(f'PASS {name}: three A4 pages, PVC-only materials, two references, eight full-resolution views')
