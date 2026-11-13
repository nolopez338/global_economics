# Copyable CE 0.17.3 typography example

This is an authoring reference, not a scene or an executable validation script. Copy only the relevant definitions into an authorized scene/helper; it makes no global Manim configuration changes. It has been reviewed against installed source, not executed or rendered.

```python
from contextlib import contextmanager
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
import shutil
import subprocess

import manimpango
from manim import NORMAL, MathTex, TexTemplate, Text, register_font


PREAMBLE = r"""
\usepackage[english]{babel}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{dsfont}
\usepackage{setspace}
\usepackage{tipa}
\usepackage{relsize}
\usepackage{textcomp}
\usepackage{mathrsfs}
\usepackage{calligra}
\usepackage{wasysym}
\usepackage{ragged2e}
\usepackage{physics}
\usepackage{xcolor}
\usepackage{microtype}
\usepackage{pifont}
\DisableLigatures{encoding = *, family = * }
\linespread{1}
\DeclareMathSymbol{\minus}{\mathbin}{AMSa}{"39}
"""


def math_template():
    return TexTemplate(
        tex_compiler="latex",
        output_format=".dvi",
        documentclass=r"\documentclass[preview]{standalone}",
        preamble=PREAMBLE,
    )


@contextmanager
def cmu_scope():
    # No silent fallback. Caller can explicitly choose and report Segoe UI.
    if "CMU Serif" in manimpango.list_fonts():
        yield "CMU Serif"
        return
    lookup = shutil.which("kpsewhich")
    if lookup is None:
        raise RuntimeError("CMU Serif unavailable; kpsewhich not found")
    found = subprocess.run(
        [lookup, "cmunrm.otf"], capture_output=True, text=True, check=True
    ).stdout.strip()
    if not found or not Path(found).is_file():
        raise FileNotFoundError("CMU Serif Roman: cmunrm.otf unavailable")
    with register_font(Path(found)):
        if "CMU Serif" not in manimpango.list_fonts():
            raise RuntimeError("CMU Serif registration did not expose the family")
        yield "CMU Serif"


def words(message, *, font, size=30, **kwargs):
    # font is explicit, including when the caller uses a disclosed fallback.
    return Text(message, font=font, weight=NORMAL, slant=NORMAL,
                disable_ligatures=True, font_size=size, **kwargs)


def quantized_units(value, places=1):
    """Half-even rounding; integer units drive both display and geometry."""
    if not isinstance(places, int) or places < 0:
        raise ValueError("places must be a nonnegative integer")
    number = Decimal(str(value))
    if not number.is_finite():
        raise ValueError("display value must be finite")
    return int((number * (10 ** places)).to_integral_value(
        rounding=ROUND_HALF_EVEN
    ))


def number_string(units, places=1):
    if not isinstance(places, int) or places < 0:
        raise ValueError("places must be a nonnegative integer")
    whole, fraction = divmod(abs(units), 10 ** places)
    tail = f"{fraction:0{places}d}".rstrip("0") if places else ""
    return ("\u2212" if units < 0 else "") + str(whole) + (
        "." + tail if tail else ""
    )
```

Use within the existing `render_section` only for content requested by the user:

```python
# Authoring excerpt: constructing these objects invokes Pango/LaTeX when run.
# Do not execute this excerpt as an automatic authoring check.
with cmu_scope() as font:
    title = words("NÃºmeros con signo", font=font, size=40)
    equation = MathTex(r"(-3)\times 2=-6", font_size=49,
                       tex_template=math_template())
    units = quantized_units(tracker.get_value(), places=1)
    readout = words(number_string(units, places=1), font=font, size=96)
    # Geometry representing the readout uses units / 10, not the raw tracker.
```

The excerpt shows typography and formatting, not a dynamic layout implementation. Do not rebuild and center the whole `readout` every frame. For animation, adapt `CenteredNumber` from `assets/manim/algebra/stage1_arithmetic_foundations/01_numbers-arrows.py`: create the `0123456789âˆ’.` alphabet with the explicit selected font and normal weight inside the font scope, retain each glyph's vertical offset from the original run, then copy into fixed slots with reserved digit advances. The existing helper is specialized to tenths; keep its units and capacity consistent if adapting to other precision/ranges. Retain a fixed anchor/baseline and update geometry and glyphs from the same `units` in one ordered update. Use a separate template-based glyph cache for equation-style digits when appropriate.

The copied optional `\minus` declaration does not replace ordinary TeX `-`. Use the standard mathematical minus consistently unless a task explicitly needs the short variant. Spanish prose belongs in Pango `Text`, so the reference's English Babel option need not be changed merely for Spanish titles.
