# Histogram grain edit

Built-in ImageGen edit prompt (input: `Global_Economics_cover_artwork.png`):

> Use case: precise-object-edit. Edit target: supplied Global Economics cover. Add only very faint, fine monochromatic white-noise grain inside the pale gray histogram bar fills near the bottom. Preserve the exact composition, dimensions/aspect ratio, all text, diagonals, axes, normal curve, bar shapes and black outlines. Keep the bars' pale gray colors and readability. Grain should be random fine luminance variations, no pattern, no large speckles, no tint. All other cover elements and white background must remain unchanged. This is a subtle print texture edit, not a redesign.

## Preservation pass

The generated full cover was not substituted wholesale. Only its fine luminance grain was transferred into the untouched original, producing `Global_Economics_cover_artwork_grain.png` (1102 x 1427 RGB pixels).

Bar bounds in original image coordinates (left, right, top), with common baseline y=1169:

```text
(186,254,1157), (254,321,1122), (321,388,1057), (388,456,972),
(456,524,889), (524,593,845), (593,661,889), (661,730,972),
(730,798,1057), (798,866,1122), (866,935,1157)
```

The mask uses three-pixel insets and ends at y=1165. Original pixels outside the gray range 210-247 are excluded, as are pixels within a two-pixel neighborhood of any original pixel below 205, protecting the curve and linework.

Grain is the generated red-channel sample minus its four axial neighbors' mean, scaled by 1.2, rounded, and clamped to +/-5. That same small delta is added to each original RGB channel, preserving color differences and the original shading.

Verification: 73,654 changed pixels, all within bar interiors; every pixel outside the mask and all protected linework remain identical. Maximum channel change is 5/255; RMS delta over eligible pixels is 2.006/255; mean delta is -0.019/255. The original PNG and reference PDF remain unchanged. The compiled cover has one 612 x 792 point page, with the original image transformation retained. The rendered full page and histogram detail were visually inspected.
