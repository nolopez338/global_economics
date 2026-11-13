"""Numerical properties; Manim Community 0.17.3, 42 seconds.

From the repository root (absolute script paths also work):
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/06_real_number_properties.py RealNumberProperties
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries

Final MP4 (repository-relative, independent of cwd):
    ../manim_media/videos/algebra/stage1_arithmetic_foundations/03_real_number_properties.mp4
Clock, including incoming transitions and reading pauses: 6 + 10 + 10 + 4*4.
"""
from pathlib import Path
import sys

REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, Brace, Create, DashedLine, Dot,
    FadeIn, FadeOut, Indicate, MoveAlongPath, ArcBetweenPoints, Rectangle, VGroup,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    BLUE, GOLD, GREEN, MUTED, TopicScene, PROPERTIES_SECONDS,
)


def equation(scene, *parts):
    return scene.math(*parts, size=43).move_to(UP * 1.95)


def brace_label(scene, group, direction, label):
    brace = Brace(group, direction, buff=0.15, color=MUTED)
    return VGroup(brace, scene.math(label, size=27).next_to(brace, direction, buff=0.1))


def six_bar():
    # One scene unit per arithmetic unit throughout the neutral/inverse beats.
    return VGroup(*[
        Rectangle(width=1, height=0.6, stroke_color=MUTED, stroke_width=1.3,
                  fill_color=BLUE, fill_opacity=0.8)
        .move_to([i - 2.5, -0.25, 0]) for i in range(6)
    ])


def render_section(self, *, standalone=False):
    section_start = self.lesson_seconds
    # 0–6: move complete colored groups on separate semicircular paths.
    start = self.topic("Conmutativa")
    row = equation(self, "3+5", "=5+3")
    three = VGroup(*[Dot(radius=0.13, color=BLUE)
                      .move_to([-3.5 + 0.46*i, 0, 0]) for i in range(3)])
    five = VGroup(*[Dot(radius=0.13, color=GOLD)
                     .move_to([1.8 + 0.46*i, 0, 0]) for i in range(5)])
    a = VGroup(three, self.math("3", size=32).next_to(three, DOWN, buff=0.4))
    b = VGroup(five, self.math("5", size=32).next_to(five, DOWN, buff=0.4))
    self.move(FadeIn(row[0]), FadeIn(a), FadeIn(b), seconds=0.6)
    self.pause(0.6)
    ac, bc = a.get_center().copy(), b.get_center().copy()
    self.move(MoveAlongPath(a, ArcBetweenPoints(ac, bc, angle=-np.pi/2)),
              MoveAlongPath(b, ArcBetweenPoints(bc, ac, angle=-np.pi/2)), seconds=1.6)
    self.move(FadeIn(row[1]), seconds=0.5)
    self.finish_beat(start, 6)

    # 6–16: retain the very same 30 dots; change positions and grouping braces.
    start = self.topic("Asociativa")
    row = equation(self, r"(2\times5)\times3", r"=2\times(5\times3)")
    fives = [VGroup(*[
        Dot(radius=0.085, color=BLUE if col == 0 else GOLD)
        .move_to([-3.2 + col*2.4 + i*0.36, 0.55-r*0.8, 0])
        for i in range(5)
    ]) for r in range(3) for col in range(2)]
    dots = VGroup(*fives)
    ten = brace_label(self, VGroup(fives[0], fives[1]), UP, r"2\times5=10")
    rows = brace_label(self, dots, LEFT, "3")
    self.move(FadeIn(row[0]), FadeIn(dots), FadeIn(ten), FadeIn(rows), seconds=0.7)
    self.pause(1.5)
    self.move(FadeOut(ten), FadeOut(rows), seconds=0.4)
    targets = [[-3.1 + col*5.0, 0.55-r*0.8, 0]
               for r in range(3) for col in range(2)]
    self.move(*[g.animate.move_to(p) for g, p in zip(fives, targets)], seconds=1.8)
    columns = [VGroup(*fives[col::2]) for col in range(2)]
    fifteens = VGroup(*[brace_label(self, c, DOWN, r"5\times3") for c in columns])
    two = brace_label(self, dots, UP, "2")
    self.move(FadeIn(fifteens), FadeIn(two), seconds=0.6)
    self.pause(1.0)
    self.move(FadeIn(row[1]), seconds=0.6)
    self.finish_beat(start, 10)

    # 16–26: seven strips, each split exactly at 99/100; only 14 rectangles.
    start = self.topic("Distributiva")
    row = equation(self, r"7(100-1)", "=700-7", "=693")
    length, unit, left = 8.0, 0.08, -4.5
    bodies, units = VGroup(), VGroup()
    for i in range(7):
        y = 0.95 - i*0.4
        bodies.add(Rectangle(width=length-unit, height=0.23,
                            stroke_width=1, stroke_color=MUTED,
                            fill_color=BLUE, fill_opacity=0.8)
                   .move_to([left+(length-unit)/2, y, 0]))
        units.add(Rectangle(width=unit, height=0.23, stroke_width=0.6,
                           stroke_color=GOLD, fill_color=GOLD, fill_opacity=1)
                  .move_to([left+length-unit/2, y, 0]))
    hundred = self.math("100", size=27).next_to(bodies[0], LEFT, buff=0.25)
    # Ten-unit end detail: lengths 9:1, magnified fivefold horizontally.
    detail = VGroup(
        Rectangle(width=3.6, height=0.5, stroke_color=MUTED, stroke_width=1,
                  fill_color=BLUE, fill_opacity=0.8).move_to([-1.8, -2.45, 0]),
        Rectangle(width=0.4, height=0.5, stroke_color=GOLD, stroke_width=1,
                  fill_color=GOLD, fill_opacity=1).move_to([0.2, -2.45, 0]),
    )
    one = brace_label(self, detail[1], DOWN, "1")
    connectors = VGroup(
        DashedLine([left+length-10*unit, -1.57, 0], [-3.6, -2.2, 0],
                   color=MUTED, stroke_width=1),
        DashedLine([left+length, -1.57, 0], [0.4, -2.2, 0],
                   color=MUTED, stroke_width=1),
    )
    self.move(FadeIn(row[0]), FadeIn(bodies), FadeIn(units), FadeIn(hundred), seconds=0.7)
    self.move(FadeIn(detail), FadeIn(one), Create(connectors), seconds=0.6)
    self.pause(1.2)
    self.move(*[cell.animate.shift(RIGHT*1.7) for cell in units],
              FadeOut(detail), FadeOut(one), FadeOut(connectors), seconds=1.2)
    seven = brace_label(self, units, RIGHT, "7")
    self.move(FadeIn(seven), FadeIn(row[1]), seconds=0.6)
    self.pause(1.3)
    self.move(FadeIn(row[2]), seconds=0.6)
    self.finish_beat(start, 10)

    # 26–30: an empty brace carries zero; the six-unit bar never changes.
    start = self.topic("Neutros e inversos")
    row, bar = equation(self, "6+0=6"), six_bar()
    empty = VGroup(Brace(Rectangle(width=1.2, height=0.6)
                         .move_to([4.7, -0.25, 0]), DOWN, color=MUTED))
    empty.add(self.math("0", size=30).next_to(empty, DOWN, buff=0.1))
    plus = self.math("+", size=34).move_to([3.6, -0.25, 0])
    self.move(FadeIn(row), FadeIn(bar), seconds=0.5)
    self.move(FadeIn(plus), FadeIn(empty), seconds=0.5)
    self.pause(0.5)
    self.move(Indicate(bar, color=GREEN, scale_factor=1), seconds=0.5)
    self.finish_beat(start, 4)

    # 30–34: exactly one copy of that same six-unit bar.
    start = self.topic("Neutros e inversos")
    row, bar = equation(self, r"6\times1=6"), six_bar()
    one_copy = brace_label(self, bar, DOWN, "1")
    self.move(FadeIn(row), FadeIn(bar), seconds=0.5)
    self.move(FadeIn(one_copy), seconds=0.5)
    self.pause(0.5)
    self.move(Indicate(bar, color=GREEN, scale_factor=1), seconds=0.5)
    self.finish_beat(start, 4)

    # 34–38: exact head-to-tail endpoints on the same axis. The thinner return
    # arrow keeps both directions visible without changing the endpoints.
    start = self.topic("Neutros e inversos")
    row = equation(self, r"6+(-6)=0")
    origin = Dot([-3, -0.25, 0], radius=0.065, color=GREEN)
    positive = Arrow([-3, -0.25, 0], [3, -0.25, 0], buff=0,
                     color=BLUE, stroke_width=8)
    negative = Arrow([3, -0.25, 0], [-3, -0.25, 0], buff=0,
                     color=GOLD, stroke_width=3)
    labels = VGroup(self.math("6", size=30).move_to([0, 0.35, 0]),
                    self.math("-6", size=30).move_to([0, -0.85, 0]),
                    self.math("0", size=28).move_to([-3, -0.85, 0]))
    self.move(FadeIn(row), FadeIn(origin), Create(positive), FadeIn(labels[0]), seconds=0.7)
    self.move(Create(negative), FadeIn(labels[1]), seconds=0.8)
    self.move(FadeIn(labels[2]), Indicate(origin, color=GREEN), seconds=0.5)
    self.finish_beat(start, 4)

    # 38–42: divide the identical six-unit whole and emphasize one unit.
    start = self.topic("Neutros e inversos")
    row, cells = equation(self, r"6\times\frac{1}{6}=1"), six_bar()
    whole = Rectangle(width=6, height=0.6, stroke_color=MUTED, stroke_width=1.3,
                      fill_color=BLUE, fill_opacity=0.8).move_to(cells)
    self.move(FadeIn(row), FadeIn(whole), seconds=0.5)
    self.move(FadeOut(whole), FadeIn(cells), seconds=0.5)
    selected = brace_label(self, cells[0], DOWN, "1")
    self.move(cells[0].animate.set_fill(GREEN, opacity=1),
              *[cell.animate.set_fill(opacity=0.12) for cell in cells[1:]],
              FadeIn(selected), seconds=0.7)
    self.finish_beat(start, 4)
    self.check_duration(section_start + PROPERTIES_SECONDS)


class RealNumberProperties(TopicScene):
    """Identical demonstrations in standalone and combined renders."""

    video_number = 3
    source_file = __file__
    output_identity = "algebra/stage1_arithmetic_foundations/03_real_number_properties.mp4"
    section = render_section
    planned_seconds = PROPERTIES_SECONDS
