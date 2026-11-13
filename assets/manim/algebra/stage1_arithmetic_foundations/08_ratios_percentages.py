"""Recipe scaling and a discount; Manim Community 0.17.3, 32 seconds.

From the repository root (or use absolute script paths from any directory):
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/08_ratios_percentages.py RatiosPercentages
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries
    python -m manim -qh --fps 60 assets/manim/algebra/stage1_arithmetic_foundations/08_ratios_percentages.py RatiosPercentages

Final MP4 (repository-relative, independent of cwd, for either quality):
    ../manim_media/videos/algebra/stage1_arithmetic_foundations/05_ratios_percentages.mp4
"""

from pathlib import Path
import sys

# Manim loads files by path; anchor package imports to the file, never to cwd.
REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import (
    DOWN, Circle, FadeIn, Indicate, Rectangle, Transform, VGroup,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    BLUE, GOLD, GREEN, MUTED, TopicScene, RATIOS_SECONDS,
)


def render_section(self, *, standalone=False):
    start = self.topic("Receta · porciones e ingrediente")
    # One four-portion group is exactly as wide as its 150 g ingredient block.
    groups = VGroup()
    blocks = VGroup()
    for x in (-2.4, 0, 2.4):
        markers = VGroup(*[
            Circle(radius=0.16, color=BLUE, fill_opacity=1)
            .move_to([x + offset, 0.85, 0])
            for offset in (-0.75, -0.25, 0.25, 0.75)
        ])
        groups.add(markers)
        block = Rectangle(width=2.4, height=0.65, stroke_color=BLUE,
                          fill_color=BLUE, fill_opacity=0.2).move_to([x, -0.1, 0])
        blocks.add(VGroup(block, self.words("150 g", 25).move_to(block)))

    portions = self.words("8 porciones", 31).move_to([0, 1.8, 0])
    grams = self.words("300 g", 31).move_to([0, -1, 0])
    self.replace_body(VGroup(portions, groups[0], groups[1],
                             blocks[0], blocks[1], grams))
    self.pause(2.4)
    self.move(FadeIn(groups[2]), FadeIn(blocks[2]), seconds=1)
    self.move(Transform(portions, self.words("12 porciones", 31).move_to(portions)),
              Transform(grams, self.words("450 g", 31).move_to(grams)), seconds=0.7)
    self.pause(1.4)
    calculation = self.math(
        r"300\,\mathrm{g}\times\frac{12}{8}=450\,\mathrm{g}", size=44
    ).move_to([0, -2, 0])
    self.move(FadeIn(calculation), seconds=0.8)
    self.pause(2.2)
    scaling = VGroup(
        self.words("8 → 12 porciones", 27, GREEN),
        self.words("300 g → 450 g", 27, GREEN),
    ).arrange(buff=0.75).move_to([0, -2.95, 0])
    self.move(FadeIn(scaling), seconds=0.6)
    self.move(Indicate(scaling[0], color=GREEN, scale_factor=1.06),
              Indicate(scaling[1], color=GREEN, scale_factor=1.06), seconds=0.9)
    self.pause(2)

    self.topic("Compra · descuento del 15%")
    # Fixed original scale: each of the twenty 0.5-wide cells is 5% = 2 dollars.
    segments = VGroup(*[
        Rectangle(width=0.5, height=0.65, stroke_color=MUTED, stroke_width=1.5,
                  fill_color=BLUE, fill_opacity=0.55)
        .move_to([-4.75 + 0.5 * index, 1, 0])
        for index in range(20)
    ])
    original = self.words("Precio original: 40 dólares", 31).move_to([0, 2, 0])
    reference = Rectangle(width=10, height=0.65, stroke_color=MUTED,
                          stroke_width=1).move_to([0, 1, 0])
    unit = self.words("Cada segmento: 5%", 24, MUTED).move_to([0, 0.25, 0])
    self.replace_body(VGroup(original, reference, segments, unit))
    self.pause(1.8)
    discount = VGroup(*segments[17:])
    percent = self.words("15%", 27, GOLD).move_to([4.25, 0.25, 0])
    self.move(discount.animate.set_fill(GOLD, opacity=0.8).set_stroke(GOLD),
              FadeIn(percent), seconds=0.7)
    self.pause(0.8)
    percent_calc = self.math(r"15\%\ \text{de}\ 40=0.15\times40=6", size=42)
    percent_calc.move_to([0, -1.65, 0])
    self.move(FadeIn(percent_calc), seconds=0.8)
    self.pause(2)
    discount_amount = self.words("6 dólares", 25, GOLD).move_to([4.25, 0.25, 0])
    self.move(Transform(percent, discount_amount), seconds=0.5)
    # Translate, never resize: the 17 remaining cells still occupy 85% of 40.
    self.move(discount.animate.shift(DOWN * 1.2),
              percent.animate.shift(DOWN * 1.2),
              unit.animate.move_to([-0.75, 0.25, 0]), seconds=1)
    remaining = VGroup(*segments[:17])
    remaining_amount = self.words("34 dólares · 85%", 27, GREEN).move_to([-0.75, 0.25, 0])
    self.move(remaining.animate.set_fill(GREEN, opacity=0.45),
              Transform(unit, remaining_amount), seconds=0.6)
    paid = self.math(r"40-6=34\ \text{dólares}", size=44).move_to([0, -2.65, 0])
    paid.set_color(GREEN)
    self.move(FadeIn(paid), seconds=0.8)
    self.finish_beat(start, RATIOS_SECONDS)


class RatiosPercentages(TopicScene):
    """Standalone and combined renders share geometry, timing and reading pauses."""

    video_number = 5
    source_file = __file__
    output_identity = "algebra/stage1_arithmetic_foundations/05_ratios_percentages.mp4"

    section = render_section
    planned_seconds = RATIOS_SECONDS
