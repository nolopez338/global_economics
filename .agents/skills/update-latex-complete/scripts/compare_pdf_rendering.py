"""Compare every PDF page with the same PDFium renderer (no tolerance).

Dependencies: Python 3, pypdfium2, Pillow. Example:
  python compare_pdf_rendering.py old.pdf new.pdf review --dpi 180
Optional --pages N and --size-mm WIDTH HEIGHT assert delivery dimensions
(0.01 mm tolerance for PDF point rounding). Writes report.json and page images
for both inputs; changed pages also get a difference image. Exit 0 means equal
pixels and passed expectations; 1 means differences; invalid inputs raise errors.
Only checks the selected resolution, page sizes and count, not mathematical
correctness, metadata, accessibility, native vector identity or hidden content.
Inspect rendered pages manually; equal images can preserve existing defects.
No downloads or changes to input documents.
"""
import argparse
import json
from pathlib import Path
import pypdfium2 as pdfium
from PIL import ImageChops


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', type=Path)
    parser.add_argument('candidate', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--dpi', type=int, default=180)
    parser.add_argument('--pages', type=int)
    parser.add_argument('--size-mm', nargs=2, type=float)
    args = parser.parse_args()
    if args.dpi < 1:
        parser.error('--dpi must be positive')
    args.output.mkdir(parents=True, exist_ok=True)
    docs = [pdfium.PdfDocument(str(p)) for p in (args.baseline, args.candidate)]
    report = {'dpi': args.dpi, 'page_counts': [len(d) for d in docs], 'pages': []}
    passed = len(docs[0]) == len(docs[1])
    if args.pages is not None:
        passed &= all(len(d) == args.pages for d in docs)
    for i in range(max(len(d) for d in docs)):
        images, sizes = [], []
        for label, doc in zip(('baseline', 'candidate'), docs):
            if i >= len(doc):
                continue
            page = doc[i]
            size = [v * 25.4 / 72 for v in page.get_size()]
            sizes.append(size)
            if args.size_mm:
                passed &= all(abs(a-b) <= .01 for a,b in zip(size,args.size_mm))
            bitmap = page.render(scale=args.dpi / 72)
            img = bitmap.to_pil().convert('RGB')
            img.save(args.output / f'{label}-{i+1:03}.png')
            images.append(img)
            bitmap.close()
            page.close()
        equal = len(images) == 2 and images[0].size == images[1].size and sizes[0] == sizes[1]
        changed = None
        bbox = None
        if equal:
            diff = ImageChops.difference(*images)
            bbox = diff.getbbox()
            # Count differing RGB pixels directly, including tiny channel deltas.
            pixels = diff.get_flattened_data() if hasattr(diff, 'get_flattened_data') else diff.getdata()
            changed = sum(1 for pixel in pixels if pixel != (0,0,0))
            equal = changed == 0
            if not equal:
                diff.save(args.output / f'difference-{i+1:03}.png')
        passed &= equal
        report['pages'].append({'page': i+1, 'sizes_mm': sizes,
                                'equal': equal, 'changed_pixels': changed,
                                'difference_bbox': bbox})
    for doc in docs:
        doc.close()
    report['passed'] = bool(passed)
    (args.output/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
