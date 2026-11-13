# Prompt: reproduce the Global Economics cover in LaTeX

Inspect `book2026-2027/preamble/Global_Economics_cover.pdf` visually and structurally, then create `book2026-2027/preamble/Global_Economics_cover_tex.tex` so compiling it reproduces the reference cover's appearance. Preserve the original PDF.

Requirements:

- Verify the reference page count, page dimensions, embedded images, text, and drawing objects before choosing an implementation.
- Match the single US Letter page (612 x 792 PDF points), edge-to-edge white background, diagonal corner lines, black GLOBAL ECONOMICS title, ACTIVITIES subtitle, and histogram with its normal curve and mathematical labels.
- The reference stores the entire design as one 1102 x 1427 RGB image. For exact visual fidelity, extract that original image losslessly to `book2026-2027/preamble/Global_Economics_cover_artwork.png` and use LaTeX `graphicx` to place it at the full page dimensions with no margins, headers, footers, or added blank pages. Do not render a screenshot or recompress the artwork with JPEG.
- Make the source compilable with pdfLaTeX from either the repository root or the preamble directory. Document both commands in comments. Do not include the original PDF as a page or require it as a compilation dependency.
- Preserve the exact image transformation `612 0 0 792 0 0 cm`. If ordinary `graphicx` placement introduces rounding differences, use pdfTeX image and page-resource primitives with an exact page-level transformation. Expand resource macros before assigning PDF resources and write the image object immediately.
- Clearly document that this is a faithful image-based LaTeX reproduction: the title and graph remain raster artwork, not individually editable LaTeX elements. Do not claim to have reconstructed editable typography or TikZ paths. If editable components are requested separately, reconstruct those as an explicitly approximate alternative.
- Compile to `book2026-2027/preamble/Global_Economics_cover_tex.pdf`, leaving the reference intact. Render both PDFs at the same resolution, inspect the output, and compare pixels to verify fidelity. Report any discrepancy honestly. Visual identity does not require byte-identical PDF metadata or object structure.
- Deliver the `.tex`, companion artwork, compiled PDF, and a brief statement of the verification result.
