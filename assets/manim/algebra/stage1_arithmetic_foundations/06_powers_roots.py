"""Numerical powers and roots recap; Manim Community 0.17.3.

From the repository root (or use absolute script paths from any directory):
    manim -ql assets/manim/algebra/stage1_arithmetic_foundations/06_powers_roots.py PowersRoots
    manim -ql assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries

Output: San Bartolo/manim_media, resolved from common.py, independently of cwd.
Standalone and combined section: 48 seconds. No audio or external assets.
Videos: San Bartolo/manim_media/videos/algebra/stage1.
"""

from pathlib import Path
import sys

# Manim loads files by path; anchor package imports to the file, never to cwd.
REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, Create, FadeIn, Indicate,
    Line, Square, SurroundingRectangle, VGroup,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    BLUE, GOLD, GREEN, MUTED, TopicScene, POWERS_SECONDS,
)


def render_section(self, *, standalone=False):
    start = self.topic("Potencias y raíces")

    def read_until(offset):
        """Keep each numerical reminder inside its own reading window."""
        remaining = start + offset - self.lesson_seconds
        if remaining < -1e-6:
            raise ValueError("El recordatorio excede su ventana de lectura")
        if remaining > 1e-6:
            self.pause(remaining)

    # 0–12 s: one-to-one cancellation; all eight canceled factors stay visible.
    equation = self.math(r"2^3\times2^2\div2^4", r"=2^{3+2-4}", "=2", size=44)
    equation.move_to(UP * 1.75)
    equation[1].set_color(BLUE)
    equation[2].set_color(GREEN)
    self.replace_body(equation[0])
    self.pause(1)
    numerator = self.math("(", "2", r"\cdot", "2", r"\cdot", "2", ")",
                          r"\cdot", "(", "2", r"\cdot", "2", ")", size=42)
    numerator.move_to(UP * 0.35)
    denominator = self.math("2", r"\cdot", "2", r"\cdot", "2", r"\cdot", "2", size=42)
    denominator.move_to(DOWN * 0.8)
    bar = Line(LEFT * (numerator.width / 2 + 0.2),
               RIGHT * (numerator.width / 2 + 0.2), color=MUTED)
    self.move(FadeIn(numerator), Create(bar), FadeIn(denominator))
    self.pause(1)
    for top_index, bottom_index in zip((1, 3, 5, 9), (0, 2, 4, 6)):
        top, bottom = numerator[top_index], denominator[bottom_index]
        slashes = VGroup(*[
            Line(factor.get_corner(DOWN + LEFT) + LEFT * 0.07,
                 factor.get_corner(UP + RIGHT) + RIGHT * 0.07,
                 color=GOLD, stroke_width=3)
            for factor in (top, bottom)
        ])
        self.move(Create(slashes), top.animate.set_color(MUTED).set_opacity(0.3),
                  bottom.animate.set_color(MUTED).set_opacity(0.3), seconds=0.45)
        self.pause(0.25)
    self.move(numerator[11].animate.set_color(GREEN), FadeIn(equation[1]))
    self.pause(0.8)
    self.move(FadeIn(equation[2]))
    read_until(12)

    # 12–24 s: a compact ladder, revealed one step at a time.
    values = (r"2^2=4", r"2^1=2", r"2^0=1",
              r"2^{-1}=\frac12", r"2^{-2}=\frac14")
    nodes = VGroup(*[self.math(value, size=34) for value in values])
    nodes.arrange(RIGHT, buff=0.85).move_to(UP * 0.35)
    links = []
    for left, right in zip(nodes, nodes[1:]):
        arrow = Arrow(left.get_right() + RIGHT * 0.1,
                      right.get_left() + LEFT * 0.1, buff=0,
                      color=MUTED, stroke_width=2, tip_length=0.12)
        label = self.math(r"\div2", size=23).set_color(GOLD)
        label.next_to(arrow, UP, buff=0.14)
        links.append(VGroup(arrow, label))
    self.replace_body(nodes[0])
    self.pause(0.85)
    for link, node in zip(links, nodes[1:]):
        self.move(FadeIn(link), FadeIn(node), seconds=0.6)
        self.pause(0.85)
    self.pause(0.8)
    reminders = VGroup(self.math("3^0=1"), self.math(r"2^{-2}=\frac14"))
    reminders.arrange(RIGHT, buff=1.8).move_to(UP * 0.3)
    self.replace_body(reminders)
    read_until(24)

    # 24–30 s: exactly five rows and five columns; side and area are distinct.
    grid = VGroup(*[Square(side_length=0.48, stroke_color=BLUE, stroke_width=1.5,
                          fill_color=BLUE, fill_opacity=0.12) for _ in range(25)])
    grid.arrange_in_grid(rows=5, cols=5, buff=0).move_to(LEFT * 2.8)
    area = VGroup(self.words("Área", 25, MUTED), self.math("25", size=33))
    area.arrange(RIGHT, buff=0.18).next_to(grid, UP, buff=0.22)
    side = self.math("5", size=33).next_to(grid, DOWN, buff=0.18)
    side_marker = Line(grid.get_corner(DOWN + LEFT) + DOWN * 0.12,
                       grid.get_corner(DOWN + RIGHT) + DOWN * 0.12, color=GOLD)
    self.replace_body(VGroup(grid, area, side_marker, side))
    self.pause(1.5)
    square_root = self.math(r"\sqrt{25}=5").move_to(RIGHT * 2.3)
    self.move(FadeIn(square_root))
    read_until(30)

    # 30–36 s: negative direction on a line, beside a numerical cube check.
    axis = Line([-4.8, -0.15, 0], [-0.8, -0.15, 0], color=MUTED, stroke_width=2)
    zero = [-1.2, -0.15, 0]
    negative_two = [-4.2, -0.15, 0]
    ticks = VGroup(*[Line([x, -0.28, 0], [x, -0.02, 0], color=MUTED)
                     for x in (-4.2, -2.7, -1.2)])
    labels = VGroup(self.math("0", size=31).move_to([-1.2, -0.65, 0]),
                    self.math("-2", size=31).move_to([-4.2, -0.65, 0]))
    check = self.math(r"(-2)^3=-8", size=44).move_to([2.5, 0.65, 0])
    self.replace_body(VGroup(axis, ticks, labels, check))
    direction = Arrow(zero, negative_two, buff=0, color=BLUE, stroke_width=5,
                      tip_length=0.2).shift(UP * 0.2)
    self.move(Create(direction))
    self.pause(1)
    cube_root = self.math(r"\sqrt[3]{-8}=-2", size=44).move_to([2.5, -0.8, 0])
    self.move(FadeIn(cube_root))
    read_until(36)

    # 36–48 s: isolate the base so the scope excludes/includes the minus sign.
    caption = self.words("El signo y los paréntesis", 27, MUTED).move_to(UP * 1.9)
    upper = self.math(r"-{{3}}^2", r"\;\longrightarrow\;",
                      r"-(3\times3)", r"\;\longrightarrow\;", "-9", size=45)
    lower = self.math(r"{{(-3)}}^2", r"\;\longrightarrow\;",
                      r"(-3)(-3)", r"\;\longrightarrow\;", "9", size=45)
    upper.move_to(UP * 0.65)
    lower.move_to(DOWN * 0.85)
    # Double braces isolate the complete base without altering exponent layout.
    upper_base = upper.get_part_by_tex("3", substring=False)
    lower_base = lower.get_part_by_tex("(-3)", substring=False)
    upper_scope = SurroundingRectangle(upper_base, color=GOLD, buff=0.09)
    lower_scope = SurroundingRectangle(lower_base, color=BLUE, buff=0.09)
    # Semantic chunks preceding each arrow include the isolated base and exponent.
    upper_power = VGroup(*upper[:3])
    lower_power = VGroup(*lower[:2])
    self.replace_body(VGroup(caption, upper_power, lower_power))
    self.move(Create(upper_scope), Indicate(upper_base, color=GOLD), seconds=0.6)
    self.move(FadeIn(VGroup(*upper[3:])), seconds=0.7)
    self.pause(1.5)
    self.move(Create(lower_scope), Indicate(lower_base, color=BLUE), seconds=0.6)
    self.move(FadeIn(VGroup(*lower[2:])), seconds=0.7)
    self.pause(1.5)
    equalities = VGroup(self.math(r"-3^2=-9"), self.math(r"(-3)^2=9"))
    equalities.arrange(DOWN, buff=0.75).move_to(UP * 0.1)
    equalities[0].set_color(GOLD)
    equalities[1].set_color(BLUE)
    self.replace_body(equalities)
    self.finish_beat(start, POWERS_SECONDS)


class PowersRoots(TopicScene):
    """The same 48-second numerical recap used by the complete lesson."""

    video_number = 6

    section = render_section
    planned_seconds = POWERS_SECONDS
