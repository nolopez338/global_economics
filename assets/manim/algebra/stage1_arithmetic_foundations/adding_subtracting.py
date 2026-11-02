"""AddingSubtracting: original arithmetic examples, Manim Community 0.17.3.

From the repository root (or use absolute script paths from any directory):
    manim -ql assets/manim/algebra/stage1_arithmetic_foundations/adding_subtracting.py AddingSubtracting
    manim -ql assets/manim/algebra/stage1_arithmetic_foundations/preliminaries.py ArithmeticPreliminaries

Output: San Bartolo/manim_media, resolved from common.py, independently of cwd.
Videos: San Bartolo/manim_media/videos/algebra/stage1_2/{quality}.
"""

from pathlib import Path
import sys

# Manim loads files by path; anchor package imports to the file, never to cwd.
REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import (
    DOWN, UP, Arrow, Create, Dot, FadeIn, NumberLine, VGroup, linear,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    BLUE, GREEN, MUTED, TopicScene, ADDING_SUBTRACTING_SECONDS,
)


def render_section(self, *, standalone=False):
    # 7–14.65 in the complete video: the point adds seven units.
    start = self.topic("Suma y resta con signos" if standalone
                       else "Signos y valor absoluto")
    row = self.math(r"-4-(-7)", r"=-4+7", r"=3").move_to(UP * 1.45)
    row[1].set_color(BLUE)
    row[2].set_color(GREEN)
    axis = NumberLine(x_range=[-5, 4, 1], length=9, include_numbers=True,
                      font_size=25, color=MUTED).move_to(DOWN * 0.25)
    dot = Dot(axis.n2p(-4), color=BLUE)
    travel = Arrow(axis.n2p(-4) + UP * 0.4, axis.n2p(3) + UP * 0.4,
                   buff=0, color=BLUE, stroke_width=3)
    step = self.math("+7", size=29).set_color(BLUE).next_to(travel, UP, buff=0.1)
    self.replace_body(VGroup(row[0], axis, dot))
    self.pause(1.8)
    self.move(FadeIn(row[1]), Create(travel), FadeIn(step))
    self.move(dot.animate(rate_func=linear).move_to(axis.n2p(3)), seconds=1.4)
    self.move(FadeIn(row[2]))
    self.pause(1.7)
    self.finish_beat(start, ADDING_SUBTRACTING_SECONDS)


class AddingSubtracting(TopicScene):
    """Independently renderable topic with its heading and original reading pauses."""

    video_number = 2

    section = render_section
    planned_seconds = ADDING_SUBTRACTING_SECONDS
