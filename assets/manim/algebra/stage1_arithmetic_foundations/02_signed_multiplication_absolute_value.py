"""Continuous signed multiplication and absolute value, Manim Community 0.17.3.

From the repository root (or use absolute script paths from any directory):
    manim -ql assets/manim/algebra/stage1_arithmetic_foundations/02_signed_multiplication_absolute_value.py SignedMultiplicationAbsoluteValue
    manim -ql assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries

Output: San Bartolo/manim_media, resolved from common.py, independently of cwd.
Standalone and combined section: 40 seconds. No audio or external assets.
Videos: San Bartolo/manim_media/videos/algebra/stage1.
"""

from pathlib import Path
import sys

# Manim loads files by path; anchor package imports to the file, never to cwd.
REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

import numpy as np
from manim import (
    UP, Arrow, DecimalNumber, Dot, NumberLine, Rectangle, ValueTracker,
    VGroup, VMobject, always_redraw, linear,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    BLUE, GOLD, MUTED, TopicScene, SIGNED_MULTIPLICATION_SECONDS,
)


class FixedDecimal(VGroup):
    """A DecimalNumber in four stationary character cells (sign, digit, dot, digit)."""

    def __init__(self, value, color, size=38):
        super().__init__()
        self.frame = Rectangle(width=1.2, height=0.6).set_opacity(0)
        self.number = DecimalNumber(value, num_decimal_places=1,
                                    group_with_commas=False, font_size=size,
                                    color=color)
        self.add(self.frame, self.number)
        self.set_value(value)

    def set_value(self, value):
        value = round(value, 1)
        if value == 0:
            value = 0.0  # Never display negative zero.
        self.number.set_value(value)
        chars = f"{value:.1f}".rjust(4)
        for glyph, char, slot in zip(self.number, chars.lstrip(),
                                     range(4 - len(chars.lstrip()), 4)):
            # A fixed baseline and fixed cells also keep the minus sign stationary.
            y = -0.13 if char == "." else 0
            glyph.move_to(self.frame.get_center() + np.array([(slot - 1.5) * 0.28, y, 0]))
        return self


def value_arrow(axis, value, *, lift=0, color=BLUE, opacity=1):
    """No shaft or arrowhead at zero; all other endpoints are exact."""
    if abs(value) < 1e-8:
        return VMobject()
    return Arrow(axis.n2p(0) + UP * lift, axis.n2p(value) + UP * lift,
                 buff=0, color=color, stroke_width=5, tip_length=0.18,
                 max_tip_length_to_length_ratio=0.35).set_opacity(opacity)


def render_section(self, *, standalone=False):
    # Own the incoming transition in both the standalone and combined video.
    start = self.topic("Signos y valor absoluto")
    for original in (4, -4):
        scalar = ValueTracker(1)
        axis = NumberLine(x_range=[-8, 8, 2], length=11.2,
                          include_numbers=True, font_size=24, color=MUTED)
        axis.move_to(UP * -0.55)
        reference = value_arrow(axis, original, lift=0.65, color=MUTED, opacity=0.45)
        product = always_redraw(lambda: value_arrow(axis, original * scalar.get_value(), lift=0.15))
        original_label = self.words("Original", 23, MUTED).move_to([-5, 0.85, 0])
        original_value = self.math(str(original), size=30).set_color(MUTED).move_to([-3.7, 0.85, 0])
        product_label = self.words("Producto", 23, BLUE).move_to([-5, -1.65, 0])

        # Prose, punctuation and numeric cells have independent fixed positions.
        factor = self.math("4.0" if original > 0 else "(-4.0)", size=40).move_to([-3.1, 1.75, 0])
        times = self.math(r"\times", size=40).move_to([-1.9, 1.75, 0])
        left = self.math("(", size=40).move_to([-1.25, 1.75, 0])
        multiplier = FixedDecimal(1, GOLD).move_to([-0.5, 1.75, 0])
        right = self.math(")", size=40).move_to([0.25, 1.75, 0])
        equals = self.math("=", size=40).move_to([1, 1.75, 0])
        result = FixedDecimal(original, BLUE).move_to([2.1, 1.75, 0])
        # The product uses the displayed scalar, so every displayed equality is exact.
        multiplier.add_updater(lambda mob: mob.set_value(scalar.get_value()))
        result.add_updater(lambda mob: mob.set_value(original * round(scalar.get_value(), 1)))
        indicator = self.words("Multiplicador", 21, GOLD).move_to([-0.5, 0.85, 0])
        body = VGroup(axis, reference, product, original_label, original_value,
                      product_label, factor, times, left, multiplier, right,
                      equals, result, indicator)
        self.replace_body(body)
        self.pause(1.4)
        for target in (2, -2, 1):
            self.move(scalar.animate(rate_func=linear).set_value(target), seconds=2.6)
            self.pause(1.4)
        # Freeze outgoing objects before the next transition.
        body.clear_updaters(recursive=True)

    input_value = ValueTracker(-2)
    upper = NumberLine(x_range=[-3, 3, 1], length=9,
                       include_numbers=True, font_size=25, color=MUTED)
    upper.move_to(UP * 0.25)
    lower = NumberLine(x_range=[-3, 3, 1], length=9,
                       include_numbers=True, font_size=25, color=MUTED)
    # Align by zero, including label extents, rather than by bounding-box centers.
    lower.shift(upper.n2p(0) - lower.n2p(0) + UP * -2)
    point = Dot(upper.n2p(-2), color=BLUE, radius=0.09)
    point.add_updater(lambda mob: mob.move_to(upper.n2p(input_value.get_value())))
    absolute = always_redraw(lambda: value_arrow(lower, abs(input_value.get_value()), lift=0.12))
    input_label = self.words("Entrada", 23, BLUE).move_to([-5.5, 0.8, 0])
    absolute_label = self.words("Valor absoluto", 23, BLUE).move_to([-5.1, -1.1, 0])
    left_bar = self.math("|", size=42).move_to([-1.85, 1.75, 0])
    live_input = FixedDecimal(-2, BLUE).move_to([-1.05, 1.75, 0])
    right_bar = self.math("|", size=42).move_to([-0.25, 1.75, 0])
    equals = self.math("=", size=42).move_to([0.45, 1.75, 0])
    live_absolute = FixedDecimal(2, BLUE).move_to([1.5, 1.75, 0])
    live_input.add_updater(lambda mob: mob.set_value(input_value.get_value()))
    live_absolute.add_updater(lambda mob: mob.set_value(abs(round(input_value.get_value(), 1))))
    body = VGroup(upper, lower, point, absolute, input_label, absolute_label,
                  left_bar, live_input, right_bar, equals, live_absolute)
    self.replace_body(body)
    self.pause(1.4)
    self.move(input_value.animate(rate_func=linear).set_value(0), seconds=3)
    self.pause(1.4)
    self.move(input_value.animate(rate_func=linear).set_value(2), seconds=3)
    self.pause(1.65)
    body.clear_updaters(recursive=True)
    self.finish_beat(start, SIGNED_MULTIPLICATION_SECONDS)


class SignedMultiplicationAbsoluteValue(TopicScene):
    """The same 40-second visual reminder used by the complete lesson."""

    video_number = 2

    section = render_section
    planned_seconds = SIGNED_MULTIPLICATION_SECONDS
