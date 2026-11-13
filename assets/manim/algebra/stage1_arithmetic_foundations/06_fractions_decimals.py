"""Fraction strips and a hundred grid; Manim Community 0.17.3 (40 seconds).

From the repository root:
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/06_fractions_decimals.py FractionsDecimals
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries

Final MP4 (repository-relative, independent of cwd):
    ../manim_media/videos/algebra/stage1_arithmetic_foundations/04_fractions_decimals.mp4
"""

from pathlib import Path
import sys

REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import (
    Create, FadeIn, FadeOut, LaggedStart, Line, Rectangle,
    RIGHT, TransformFromCopy, VGroup,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    BLUE, GOLD, GREEN, MUTED, TopicScene, FRACTIONS_SECONDS,
)

# All linear lengths use this unit, including both result wholes.
UNIT = 5.2
LEFT = -5.2
HEIGHT = 0.48


def strip(y, denominator, shaded=0, color=BLUE, x=LEFT, length=UNIT):
    cells = VGroup(*[
        Rectangle(width=length / denominator, height=HEIGHT,
                  stroke_color=MUTED, stroke_width=1.3,
                  fill_color=color, fill_opacity=0.8 if i < shaded else 0)
        .move_to([x + (i + 0.5) * length / denominator, y, 0])
        for i in range(denominator)
    ])
    return cells


def divisions(y, denominator, x=LEFT, length=UNIT):
    return VGroup(*[
        Line([x + i * length / denominator, y - HEIGHT / 2, 0],
             [x + i * length / denominator, y + HEIGHT / 2, 0],
             stroke_color=MUTED, stroke_width=1.3)
        for i in range(1, denominator)
    ])


def scale(scene):
    ruler = VGroup(Line([LEFT, 1.95, 0], [LEFT + 2 * UNIT, 1.95, 0],
                        stroke_color=MUTED, stroke_width=1.5))
    for i in range(3):
        x = LEFT + i * UNIT
        ruler.add(Line([x, 1.87, 0], [x, 2.03, 0], stroke_color=MUTED),
                  scene.math(str(i), size=27).move_to([x, 2.24, 0]))
    return ruler


def clear_body(scene):
    scene.move(*[FadeOut(m) for m in list(scene.mobjects)
                 if m not in scene.header], seconds=0.6)


def pad_until(scene, start, seconds):
    remaining = seconds - (scene.lesson_seconds - start)
    if remaining < -1e-6:
        raise ValueError("El ejemplo excede su duración")
    if remaining > 1e-6:
        scene.pause(remaining)


def render_section(self, *, standalone=False):
    start = self.topic("Fracciones y decimales")

    # Addition: repartition in place, then copy exactly 9 + 8 twelfths.
    first = strip(0.95, 4, 3, BLUE)
    second = strip(-0.05, 3, 2, GOLD)
    labels = VGroup(self.math(r"\frac34", size=41).set_color(BLUE).move_to([0.8, 0.95, 0]),
                    self.math(r"\frac23", size=41).set_color(GOLD).move_to([0.8, -0.05, 0]))
    self.move(FadeIn(scale(self)), FadeIn(first), FadeIn(second), FadeIn(labels), seconds=0.7)
    self.pause(1.0)
    self.move(Create(divisions(0.95, 12)), Create(divisions(-0.05, 12)), seconds=0.8)
    self.pause(0.7)
    equation = self.math(r"\frac34+\frac23", r"=\frac9{12}+\frac8{12}",
                         r"=\frac{17}{12}", size=47).move_to([0, -2.65, 0])
    equation[1].set_color(BLUE)
    equation[2].set_color(GREEN)
    self.move(FadeIn(equation[0]), FadeIn(equation[1]), seconds=0.6)
    self.pause(1.0)
    result = VGroup(strip(-1.45, 12), strip(-1.45, 12, x=LEFT + UNIT))
    self.move(FadeIn(result), seconds=0.4)
    source_blue = strip(0.95, 12, 9, BLUE)
    source_gold = strip(-0.05, 12, 8, GOLD)
    pieces = []
    for i in range(17):
        source = source_blue[i] if i < 9 else source_gold[i - 9]
        destination = result[i // 12][i % 12].copy().set_fill(BLUE if i < 9 else GOLD, opacity=0.8)
        pieces.append(TransformFromCopy(source, destination))
    self.move(LaggedStart(*pieces, lag_ratio=0.045), seconds=2.0)
    self.pause(0.7)
    self.move(FadeIn(equation[2]), seconds=0.6)
    pad_until(self, start, 15)

    # Division: one 8/12 measure fits in 9/12; the leftover is 1 of its 8 parts.
    division_start = self.lesson_seconds
    clear_body(self)
    target = strip(0.95, 12, 9, GOLD)
    target_label = self.math(r"\frac9{12}", size=40).set_color(GOLD).move_to([0.8, 0.95, 0])
    measure = strip(-0.35, 1, 1, BLUE, length=UNIT * 8 / 12)
    measure_label = self.math(r"\frac8{12}", size=40).set_color(BLUE).move_to([-1.0, -0.35, 0])
    measure_words = self.words("Una medida", 25, BLUE).move_to([-3.45, -1.0, 0])
    self.move(FadeIn(scale(self)), FadeIn(target), FadeIn(target_label),
              FadeIn(measure), FadeIn(measure_label), FadeIn(measure_words), seconds=0.7)
    self.pause(1)
    placed = measure.copy().move_to([LEFT + UNIT * 4 / 12, 0.95, 0])
    self.move(TransformFromCopy(measure, placed), seconds=1.0)
    self.pause(0.7)
    ticks = divisions(-0.35, 8, length=UNIT * 8 / 12)
    placed_ticks = divisions(0.95, 8, length=UNIT * 8 / 12)
    one_piece = strip(-0.35, 1, 1, GOLD, x=LEFT + UNIT * 7 / 12, length=UNIT / 12)
    eighth = VGroup(self.math(r"\frac18", size=30).set_color(GOLD),
                    self.words("de medida", 25, GOLD)).arrange(RIGHT, buff=0.12)
    eighth.move_to([1.1, -1.05, 0])
    connector = Line([LEFT + UNIT * 8.5 / 12, 0.65, 0],
                     [LEFT + UNIT * 7.5 / 12, -0.02, 0], stroke_color=GOLD, stroke_width=2)
    self.move(Create(ticks), Create(placed_ticks), seconds=0.8)
    self.move(TransformFromCopy(target[8], one_piece), Create(connector), FadeIn(eighth), seconds=0.8)
    self.pause(1.3)
    equation = self.math(r"\frac34\div\frac23", r"=\left(\frac34\right)\left(\frac32\right)",
                         r"=\frac98", size=49).move_to([0, -2.65, 0])
    equation[1].set_color(BLUE)
    equation[2].set_color(GREEN)
    self.move(FadeIn(equation[0]), seconds=0.5)
    self.move(FadeIn(equation[1]), seconds=0.6)
    self.move(FadeIn(equation[2]), seconds=0.6)
    pad_until(self, division_start, 13)

    # Decimals: the same 75 cells remain shaded as four quarters are outlined.
    decimal_start = self.lesson_seconds
    clear_body(self)
    side = 0.34
    grid = VGroup(*[
        Rectangle(width=side, height=side, stroke_color=MUTED, stroke_width=0.8,
                  fill_color=BLUE, fill_opacity=0.8 if (row < 5 or col < 5) else 0)
        .move_to([(col - 4.5) * side, 0.35 + (4.5 - row) * side, 0])
        for row in range(10) for col in range(10)
    ])
    self.move(FadeIn(grid), seconds=0.8)
    self.pause(1.2)
    equation = self.math("0.75", r"=\frac{75}{100}", r"=\frac34", size=53).move_to([0, -2.55, 0])
    equation[1].set_color(BLUE)
    equation[2].set_color(GREEN)
    self.move(FadeIn(equation[0]), FadeIn(equation[1]), seconds=0.7)
    self.pause(1.6)
    quarters = VGroup(*[
        Rectangle(width=5 * side, height=5 * side,
                  stroke_color=MUTED, stroke_width=2)
        .move_to([x, 0.35 + y, 0])
        for y in (0.85, -0.85) for x in (-0.85, 0.85)
    ])
    self.move(Create(quarters), seconds=0.8)
    for quarter in quarters[:3]:
        self.move(quarter.animate.set_stroke(GOLD, width=3), seconds=0.5)
    self.pause(0.8)
    self.move(FadeIn(equation[2]), seconds=0.6)
    pad_until(self, decimal_start, 12)
    self.finish_beat(start, FRACTIONS_SECONDS)


class FractionsDecimals(TopicScene):
    """The same 40-second section used by ArithmeticPreliminaries."""

    video_number = 4
    source_file = __file__
    output_identity = "algebra/stage1_arithmetic_foundations/04_fractions_decimals.mp4"

    section = render_section
    planned_seconds = FRACTIONS_SECONDS
