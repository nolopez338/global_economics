# Verified typography and repository translation

## Reference configuration and evidence

Research snapshot: **2026-11-12**. Selected reference: the published `master` configuration in **3b1b/videos**, together with the published `master` ManimGL implementation and its `default` TeX template. These are moving branch links, not immutable commit pins; the settings below record what was inspected. This is a documented configuration match, not a claim about every 3Blue1Brown video or pixel-identical rendering across engines/platforms.

Primary sources:

1. [3Blue1Brown personal configuration](https://github.com/3b1b/videos/blob/master/custom_config.yml): `text.font: "CMU Serif"`, centered text, `tex.template: "default"`; camera uses black, 3840×2160, 30 fps. Typography does not require copying those camera settings.
2. [ManimGL defaults](https://github.com/3b1b/manim/blob/master/manimlib/default_config.yml): generic library text uses **Consolas**, overridden by the personal configuration. Its text/TeX unit-height calibration is 144. Generic ManimGL defaults alone therefore do not establish 3Blue1Brown's personal font.
3. [ManimGL text implementation](https://github.com/3b1b/manim/blob/master/manimlib/mobject/svg/text_mobject.py): Pango text, default normal slant and weight, configured family, ligatures disabled; current scaling calibrates a reference zero. A CE font-size number is not a guaranteed physical match to this implementation.
4. [Official title example](https://github.com/3b1b/videos/blob/master/_2023/moser_reboot/main.py): the “Problem-solving rule” title uses `Text` at size 72 without a separate font/weight. This supports using the configured regular text family for titles; it does not establish a universal title size or bold weight.
5. [ManimGL TeX templates](https://github.com/3b1b/manim/blob/master/manimlib/tex_templates.yml): selected `default` uses `latex`, the package list reproduced in the accompanying example, disabled ligatures, line spread 1, and an optional short-minus symbol. It does not load a replacement main mathematical font.
6. [ManimGL TeX compilation](https://github.com/3b1b/manim/blob/master/manimlib/utils/tex_file_writing.py): standalone preview document, `latex` → DVI → `dvisvgm -n` (glyph outlines). [Its TeX objects](https://github.com/3b1b/manim/blob/master/manimlib/mobject/svg/tex_mobject.py) distinguish mathematical `Tex` from prose `TexText`.
7. [ManimGL numerical objects](https://github.com/3b1b/manim/blob/master/manimlib/mobject/numbers.py): ordinary changing-number characters use cached **Text** glyphs, inheriting the configured text font. TeX is used for special commands. Its formatter substitutes an **en dash U+2013** for ASCII hyphen and suppresses negative zero; its precision/grouping defaults need not suit this lesson.
8. [Official project-specific typography](https://github.com/3b1b/videos/blob/master/_2021/shadows.py): `SimpleWriting` uses Better Grade and subclasses also use Kalam. Such explicit overrides show why this skill selects the personal configuration rather than claiming one font across all projects.
9. [CTAN CM Unicode](https://ctan.org/pkg/cm-unicode): CMU is a Computer Modern Unicode family distributed with TeX Live, with OTF files for OpenType consumers. An OTF text family is distinct from traditional TeX math fonts.
10. CE compatibility sources: [v0.17.3 text and font registration](https://github.com/ManimCommunity/manim/blob/v0.17.3/manim/mobject/text/text_mobject.py), [numerical objects](https://github.com/ManimCommunity/manim/blob/v0.17.3/manim/mobject/text/numbers.py), [TeX template](https://github.com/ManimCommunity/manim/blob/v0.17.3/manim/utils/tex.py). These same implementations were inspected locally in the installed package; web retrieval of these tag files was unavailable during authoring.

## Explicit reusable settings

| Role | Repository setting | Basis / qualification |
| --- | --- | --- |
| Ordinary text | `Text`, `font="CMU Serif"`, `weight=NORMAL`, `slant=NORMAL`, `disable_ligatures=True`; center multiline text deliberately | Personal configured family and normal ManimGL text defaults |
| Titles | Same CMU Serif Roman, `NORMAL` weight; use size/placement for hierarchy | Configured Text convention, supported by the official title example; do not invent a semibold identity |
| Equations and embedded static numbers | `MathTex`, explicit template below, normal math weight | Traditional **Computer Modern**: Roman digits/operators, math italic variables, symbol fonts and AMS supplements. CMU Serif is not the math-font setting |
| Standalone static readouts / axis values | CMU Serif `Text` or cached glyphs, normal weight | Match changing readouts when values share a visual role |
| Changing readouts | Cached CMU Serif text glyphs, preserved baseline and stable slots | Translation of ManimGL's text-based number convention, adapted to local Cairo patterns |
| Changing values inside equations | Prefer cached math glyphs from the same template if equation consistency requires it; explicitly identify this as a CE adaptation | ManimGL itself can replace TeX substrings with text-based numerical objects; there is no universal single-font numerical rule |

The chosen math font follows from the default standalone/LaTeX setup and the absence of a math-family override. Do not load `fontspec`, `unicode-math`, `mathastext`, `lmodern`, or Times math packages and still call it the same template. The complete selected template is in [typography-example.md](typography-example.md): `TexTemplate(tex_compiler="latex", output_format=".dvi", documentclass=r"\documentclass[preview]{standalone}", preamble=...)`; CE `MathTex` uses `align*`. Retain glyph outlines (`dvisvgm --no-fonts` in CE), zero text stroke, and opaque fills. No synthetic thickening is needed.

### Size and placement for the local frame

`common.py` sets frame width **128/9 ≈ 14.222** and height **8**. Keep its navy background `#0B1426`, white primary content, and established BLUE/GREEN/GOLD/MUTED accents where useful. These palette and sizing choices belong to this repository, not to the verified external font configuration.

Starting CE sizes: ordinary prose **30**, titles **40** (compact section heading **32**), main equations **49** (emphasis **52–60**), axis values **22–24**, standalone changing value **96–108** when it is the focus. Maintain the existing text width cap **12.3** and math cap **12**, with title center near **y=3.12** and main content below the header. Shorten a title before shrinking excessively. Select an initial size and reserved width for dynamic numbers; never fit each updated value to a new width. These are repository-appropriate starting points, not copied ManimGL sizes or visually verified specimens.

### Signs, formatting, and baseline

- In equations use TeX `-`, which produces a mathematical minus. In text-number displays use **U+2212 MINUS SIGN** consistently. This intentionally improves semantic consistency over the selected ManimGL formatter's U+2013 en dash; it is a declared deviation, not a literal reproduction. Do not mix hyphens, dashes, and minus glyphs among related readouts.
- Default to a decimal point and no thousands grouping, matching the inspected scenes. Apply any requested decimal-comma convention consistently to all readouts and math (TeX `{,}` avoids punctuation spacing). Do not infer a comma solely from Spanish titles.
- Select precision from the lesson. Quantize once, format from the quantized integer units, trim trailing fractional zeros and the unused separator, and emit unsigned `0` at zero. The example uses decimal half-even rounding explicitly. Reuse the scene's existing rounding rule when preserving established behavior matters.
- Keep all glyphs at one font size. Shape the alphabet in one text run and copy its positioned glyphs so the decimal point and minus retain their correct baseline offsets. Use tabular advances for digits and a smaller advance for the separator; do not vertically center each character independently. Reserve slots for the largest magnitude and sign; anchor the whole field or its decimal position as the layout requires.
- For equations, bottom-edge alignment of whole bounding boxes is not a general baseline solution: fractions, minus signs, and descenders alter those boxes. Shape complete rows in one `MathTex` where possible, or align dynamic slots to a fixed digit reference in the original row and preserve the original baseline offsets.
- **CE 0.17.3 differs:** `DecimalNumber` defaults to `mob_class=MathTex`, whereas the selected ManimGL implementation uses Text for digits. CE also caches number glyphs globally by string, without font/template in the cache key. Merely passing a different `font` or switching `mob_class` is insufficient for reliable mixed styles. Prefer the local fixed-slot pattern with a cache owned by the display/style; do not depend on ManimGL-only `text_config` or `make_number_changeable` APIs.

## Local dependency inventory and fallback

Read-only inspection on the snapshot date found:

- Python `C:/Python311/python.exe`; `importlib.metadata` reports **manim 0.17.3**. Package source is under `C:/tools/Manim/Lib/site-packages/manim`; ManimPango metadata reports **0.4.3**. Installed default renderer is **Cairo**, default pixels **1920×1080**; preserve the task's existing quality/fps settings.
- `manimpango.list_fonts()` did **not** list CMU Serif or Latin Modern. Available families include **Segoe UI**, Segoe UI Variable Display, Times New Roman, and Consolas. Existing scene typography uses Segoe UI/Segoe UI Variable Display; it is not an exact match to the selected reference.
- `kpsewhich cmunrm.otf` located **`C:/texlive/2025/texmf-dist/fonts/opentype/public/cm-unicode/cmunrm.otf`**. Its font metadata identifies **CMU Serif / Roman**, native OS/2 weight class **500**; the requested Manim style remains `NORMAL` (no synthetic semibold). Metadata/cmap inspection confirmed digits, dot, U+2212, and Spanish accented letters/punctuation in that face. Native font metadata does not change the documented ManimGL normal-weight setting.
- `latex`, `xelatex`, `dvisvgm`, and `kpsewhich` are on PATH in TeX Live 2025. `kpsewhich` found `standalone.cls`, every package in the copied preamble, and `cmr10.tfm`, `cmmi10.tfm`, `cmsy10.tfm`. This establishes file availability, not successful compilation.

**Preferred route:** discover `cmunrm.otf` with `kpsewhich` rather than hardcoding this machine's path, and use CE's `with register_font(path):` around every creation of CMU Serif glyphs. Keep the context alive through any updater that constructs new Text objects; cached copies need no re-registration. Confirm the family is available within the scope during an explicitly authorized execution. This does not require a system font installation. The example discovers the file without registering anything until its context is entered.

**Unavailable by default:** CMU Serif as an already registered Pango family. The OTF dependency is present; temporary registration and rendering were deliberately not executed during skill creation. If registration/file access fails on a future machine, disclose the limitation and use **Segoe UI, NORMAL** as the explicitly named repository fallback, with the same math template. It preserves local readability but is not a 3Blue1Brown font match. If exact matching is essential, report the dependency blocker instead of claiming success. Never silently install/download fonts, change system font settings, or replace the mathematical family to hide a missing text dependency.
