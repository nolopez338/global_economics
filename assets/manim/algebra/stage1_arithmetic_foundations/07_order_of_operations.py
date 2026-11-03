"""Six explicit arithmetic reductions, Manim Community 0.17.3.

From the repository root (or use absolute script paths from any directory):
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/07_order_of_operations.py OrderOfOperations
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries

Output: San Bartolo/manim_media, resolved from common.py, independently of cwd.
Standalone and combined section: 26 seconds on the lesson clock.
Measured 0.17.3 preview: 25.933 seconds (389 frames at 15 fps; frame rounding).
The combined runtime is calculated in common.py. No audio or external assets.
Videos: San Bartolo/manim_media/videos/algebra/stage1.
"""

from pathlib import Path
import sys

# Manim loads files by path; anchor package imports to the file, never to cwd.
REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import (
    DOWN, UP, Create, FadeIn, FadeOut, ReplacementTransform, Transform,
    TransformFromCopy, Underline, VGroup,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    GOLD, MUTED, TopicScene, ORDER_SECONDS,
)


# Each item is one semantic token, so unchanged terms have explicit destinations.
FORMS = (
    ("18", r"\div", "3", r"\times", "2", "+", r"\sqrt{16}", "-", "2^3"),
    ("18", r"\div", "3", r"\times", "2", "+", "4", "-", "2^3"),
    ("18", r"\div", "3", r"\times", "2", "+", "4", "-", "8"),
    ("6", r"\times", "2", "+", "4", "-", "8"),
    ("12", "+", "4", "-", "8"),
    ("16", "-", "8"),
    ("8",),
)
# Half-open spans: never include the multiplication when selecting 18 / 3.
STEPS = (
    (6, 7, "Potencias y raíces"),
    (8, 9, "Potencias y raíces"),
    (0, 3, "División y multiplicación · de izquierda a derecha"),
    (0, 3, "División y multiplicación · de izquierda a derecha"),
    (0, 3, "Suma y resta · de izquierda a derecha"),
    (0, 3, "Suma y resta · de izquierda a derecha"),
)


def render_section(self, *, standalone=False):
    start = self.topic("Orden de las operaciones")
    current = self.math(*FORMS[0]).set_color(MUTED).move_to(UP * 1.1)
    label = self.words(STEPS[0][2], 26, MUTED).move_to(DOWN * 2.25)
    body = VGroup(current, label)
    self.replace_body(body, seconds=0.6)
    # Keep the row and label as canonical scene objects during token animations.
    self.remove(body)
    self.add(current, label)
    self.pause(1.2)

    for index, (first, stop, wording) in enumerate(STEPS):
        selected = VGroup(*current[first:stop])
        underline = Underline(selected, buff=0.16, color=GOLD, stroke_width=4)
        new_label = self.words(wording, 26, MUTED).move_to(label)
        self.move(Transform(label, new_label), selected.animate.set_color(GOLD),
                  Create(underline), seconds=0.4)
        self.pause(0.8)

        following = self.math(*FORMS[index + 1]).set_color(MUTED).move_to(DOWN * 0.65)
        following[first].set_color(GOLD)
        arrow = self.math(r"\downarrow", size=35).set_color(MUTED).move_to(UP * 0.1)
        # The complete old row remains readable. Copies carry every unchanged
        # token to its new position; only the selected span becomes a result.
        moves = [TransformFromCopy(current[i], following[i]) for i in range(first)]
        moves.append(ReplacementTransform(selected.copy(), following[first]))
        moves.extend(TransformFromCopy(current[i], following[i - (stop - first) + 1])
                     for i in range(stop, len(current)))
        self.move(FadeIn(arrow), *moves, seconds=1)
        # Normalize ownership after animations that add individual target tokens.
        self.remove(*following)
        self.add(following)
        self.pause(0.8)
        self.move(FadeOut(current), FadeOut(arrow), FadeOut(underline),
                  following.animate.move_to(UP * 1.1).set_color(
                      GOLD if index == len(STEPS) - 1 else MUTED), seconds=0.6)
        current = following

    self.finish_beat(start, ORDER_SECONDS)


class OrderOfOperations(TopicScene):
    """The same 26-second evaluation in standalone and combined renders."""

    video_number = 7

    section = render_section
    planned_seconds = ORDER_SECONDS



