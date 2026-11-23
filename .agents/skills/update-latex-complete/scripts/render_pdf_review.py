"""Render PDF pages and numbered contact sheets for manual layout review.

Requires Python 3, pypdfium2 and Pillow (bundled workspace Python supports them).
Example: python render_pdf_review.py input.pdf output-directory --dpi 90
Writes page-NNN.png and sheet-NNN.png; prints page/sheet counts. Missing/invalid
inputs or invalid arguments exit nonzero. Does not modify the PDF, download
dependencies, detect overlaps, verify mathematics or replace visual inspection.
"""
from pathlib import Path
import argparse
import pypdfium2 as pdfium
from PIL import Image, ImageOps, ImageDraw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--dpi', type=int, default=90)
    parser.add_argument('--columns', type=int, default=3)
    parser.add_argument('--rows', type=int, default=3)
    parser.add_argument('--thumbnail-width', type=int, default=500)
    args = parser.parse_args()
    if min(args.dpi, args.columns, args.rows, args.thumbnail_width) < 1:
        parser.error('All numeric options must be positive.')
    if not args.pdf.is_file():
        parser.error('PDF does not exist: ' + str(args.pdf))
    args.output.mkdir(parents=True, exist_ok=True)
    doc = pdfium.PdfDocument(args.pdf)
    tiles = []
    sheet_number = 0
    for i in range(len(doc)):
        page = doc[i]
        bitmap = page.render(scale=args.dpi / 72)
        image = bitmap.to_pil().convert('RGB')
        image.save(args.output / f'page-{i + 1:03}.png')
        height = round(image.height * args.thumbnail_width / image.width)
        thumb = image.resize((args.thumbnail_width, height))
        tile = Image.new('RGB', (args.thumbnail_width, height + 28), 'white')
        tile.paste(thumb, (0, 28))
        ImageDraw.Draw(tile).text((8, 6), f'Page {i + 1}', fill='black')
        tiles.append(tile)
        bitmap.close()
        page.close()
        if len(tiles) == args.rows * args.columns or i == len(doc) - 1:
            sheet_number += 1
            tile_height = max(t.height for t in tiles)
            sheet = Image.new('RGB', (args.columns * args.thumbnail_width,
                                     args.rows * tile_height), '#dddddd')
            for j, tile in enumerate(tiles):
                sheet.paste(tile, ((j % args.columns) * args.thumbnail_width,
                                   (j // args.columns) * tile_height))
            sheet.save(args.output / f'sheet-{sheet_number:03}.png')
            tiles.clear()
    print(f'Rendered {len(doc)} pages, {sheet_number} contact sheets: {args.output}')
    doc.close()


if __name__ == '__main__':
    main()
