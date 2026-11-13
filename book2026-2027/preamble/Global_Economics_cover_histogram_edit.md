# Independent histogram heights

The final artwork is `Global_Economics_cover_artwork_irregular.png`.
The original extraction and grain-only artwork are untouched. The preceding
TeX source and compiled cover are preserved as `Global_Economics_cover_tex_grain.*`.

## Method

Built-in ImageGen was used for an initial edit candidate. The candidate was
not substituted wholesale: its changes to the smallest bars were too large
for the numeric tolerance. The final precision pass uses Node.js/Sharp and
the original grain artwork, retaining pixels outside narrow regions swept
by the bar tops. This avoids regeneration of typography, labels, or page layout.

`Global_Economics_cover_histogram_edit.cjs` reproduces the final artwork with
Sharp on `NODE_PATH`. Each bar independently receives one uniform PRNG draw
in [-0.08, 0.08], using seed 20261113. Heights use the original y=1169 baseline.
Subpixel sampling permits a nonzero change below one pixel for the 12-pixel
tail bars without exceeding 8%. Widths and horizontal boundaries are fixed.
Old edge profiles retain the existing thin outline and raster edge shading.
Grain samples come from the existing bar interiors; removed areas use
ungrained original paper. Existing curve stroke pixels are protected by a
separate mask, located from the original raster and interpolated through
bar-outline intersections. The curve is not rescaled or redrawn.

The JSON file records each original and revised height, percentage change,
and a check that no changed pixel escapes the bar-height regions.
The range is -7.7383% to +7.3932%; all eleven heights remain positive.
The output remains 1102 x 1427 RGB pixels. The TeX keeps the original
`612 0 0 792 0 0 cm` image transformation and a 612 x 792 point page.

## Built-in ImageGen prompt

> Use case: precise-object-edit. Edit target: supplied Global Economics cover raster artwork. Change only eleven histogram bar heights with small independent random variations within +/-8% of their original heights. Keep the overall bell distribution. Preserve ALL other elements exactly: 1102 x 1427 composition, title and typography, diagonals, white background, axes labels ticks, baseline, bar widths and x positions, pale gray fill with very faint fine monochrome grain confined to bar interiors, thin dark outlines. The smooth black normal curve must remain unchanged including all portions crossing bars. No changes to curve shape, stroke or overlap. Return exact same page aspect ratio. Subtle natural irregularity only, no redesign.

## Verification

Compiled successfully with pdfLaTeX. PDF metadata confirms one US Letter
page, 612 x 792 points. The rendered full cover and enlarged histogram
were visually inspected, including curve crossings, revised top edges,
and grain confinement. The original reference PDF is untouched.
