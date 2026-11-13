"""Signed multiplication with synchronized vector panels (Manim CE 0.17.3).

    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/03_signed_multiplication.py SignedMultiplication
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries

Standalone and combined sections share the 70-second clock in common.py.
Final MP4 (repository-relative, independent of cwd):
    ../manim_media/videos/algebra/stage1_arithmetic_foundations/03_signed_multiplication.mp4
"""

from pathlib import Path
import sys

REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

import numpy as np
from manim import (
    UP, DOWN, PI, RED, WHITE, Arrow, Create, FadeIn, FadeOut, Line,
    NumberLine, Rectangle, Rotate, Text, Transform, ValueTracker,
    VGroup, VMobject, linear,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    BLUE, MUTED, TopicScene, SIGNED_MULTIPLICATION_SECONDS,
)


class FixedNumber(VGroup):
    """Four permanent glyph paths keep Cairo's moving-family cache valid."""

    glyph_cache = {}

    def __init__(self, value, color, size=34):
        super().__init__()
        self.frame = Rectangle(width=1.18, height=.55).set_opacity(0)
        self.ink_color, self.font_size = color, size
        self.displayed = None
        self.glyphs = VGroup(*[VMobject(color=color, fill_opacity=1,
                                       stroke_width=0) for _ in range(4)])
        self.add(self.frame, self.glyphs)
        self.set_value(value)

    def set_value(self, value):
        value = round(value, 1)
        if value == 0:
            value = 0
        if value != self.displayed:
            digits = f"{abs(value):g}"
            chars = ["−" if value < 0 else "", digits[0],
                     "." if "." in digits else "",
                     digits[-1] if "." in digits else ""]
            for glyph, char, x in zip(self.glyphs, chars, [-.4, -.1, .15, .38]):
                if not char:
                    glyph.clear_points()
                    continue
                key = (char, self.font_size)
                if key not in self.glyph_cache:
                    text = Text(char, font="Consolas", font_size=self.font_size,
                                disable_ligatures=True)
                    self.glyph_cache[key] = np.concatenate([
                        part.points for part in text.family_members_with_points()])
                glyph.set_points(self.glyph_cache[key].copy())
                glyph.move_to(self.frame.get_center() +
                              np.array([x, -.12 if char == "." else 0, 0]))
            self.displayed = value
        return self


def value_arrow(axis, value, *, lift, color):
    """Scale exactly to the endpoint, with no arrowhead or shaft at zero."""
    if abs(value) < 1e-8:
        return VMobject()
    return Arrow(axis.n2p(0) + UP * lift, axis.n2p(value) + UP * lift,
                 buff=0, color=color, stroke_width=5, tip_length=.18,
                 max_tip_length_to_length_ratio=.35)


class ProductVector(VGroup):
    """Permanent shaft/tip paths scale through zero without cached ghosts."""

    def __init__(self, axis, value):
        self.axis = axis
        self.shaft = VMobject(color=RED, stroke_width=5)
        self.tip = VMobject(color=RED, fill_opacity=1, stroke_width=0)
        super().__init__(self.shaft, self.tip)
        self.set_value(value)

    def set_value(self, value):
        if abs(value) < 1e-8:
            self.shaft.clear_points()
            self.tip.clear_points()
        else:
            arrow = value_arrow(self.axis, value, lift=.85, color=RED)
            self.shaft.set_points(arrow.points.copy())
            self.tip.set_points(arrow.tip.points.copy())
        return self

    def get_start(self):
        return self.shaft.get_start() if self.shaft.has_points() else self.axis.n2p(0) + UP * .85

    def get_end(self):
        return self.tip.points[0] if self.tip.has_points() else self.get_start()


class MultiplicationPanel(VGroup):
    """Fresh geometry and instance-bound updaters, including in split view."""

    def __init__(self, scene, scalar, original=4, center=0, length=10.8):
        self.original, self.scalar = original, scalar
        self.axis = NumberLine(x_range=[-8, 8, 2], length=length,
                               include_numbers=True, font_size=20, color=MUTED)
        # Align the numerical origin, independent of number-label extents.
        self.axis.shift(np.array([center, -1.85, 0]) - self.axis.n2p(0))
        self.blue = value_arrow(self.axis, original, lift=2.25, color=BLUE)
        self.red = ProductVector(self.axis, original)
        self.blue_value = FixedNumber(original, BLUE, 27)
        self.red_value = FixedNumber(original, RED, 27)
        self.factor = FixedNumber(original, BLUE)
        self.multiplier = FixedNumber(1, WHITE)
        self.result = FixedNumber(original, RED)
        self.dot = scene.math(r"\cdot", size=34)
        self.equals = scene.math("=", size=34)
        for obj, dx in ((self.factor, -2), (self.dot, -1.2),
                        (self.multiplier, -.3), (self.equals, .6),
                        (self.result, 1.5)):
            obj.move_to([center + dx, -2.95, 0])
        self.equation = VGroup(self.factor, self.dot, self.multiplier,
                               self.equals, self.result)
        super().__init__(self.axis, self.blue, self.red, self.blue_value,
                         self.red_value, self.equation)
        self.refresh_labels()

    def product(self):
        # Quantize the input once: 4 * 0.3 is displayed as 1.2, never 1.1.
        return round(self.original * round(self.scalar.get_value(), 1), 1)

    def refresh_labels(self):
        for arrow, label, direction in ((self.blue, self.blue_value, UP),
                                         (self.red, self.red_value, DOWN)):
            midpoint = (arrow.get_start() + arrow.get_end()) / 2
            label.move_to(midpoint + direction * .29)

    def bind_labels(self):
        # FadeOut of the equation can unpack its parent in Manim 0.17.3.
        # Keep attachment on the labels themselves throughout those transitions.
        self.blue_value.add_updater(lambda mob: mob.move_to(
            (self.blue.get_start() + self.blue.get_end()) / 2 + UP * .29))
        self.red_value.add_updater(lambda mob: mob.move_to(
            (self.red.get_start() + self.red.get_end()) / 2 + DOWN * .29))

    def bind(self):
        self.red.add_updater(lambda mob: mob.set_value(
            self.original * self.scalar.get_value()))
        self.multiplier.add_updater(lambda mob: mob.set_value(self.scalar.get_value()))
        self.result.add_updater(lambda mob: mob.set_value(self.product()))
        self.red_value.add_updater(lambda mob: mob.set_value(self.product()))
        self.bind_labels()
        return self


def sliding_routine(scene, scalar):
    for target in (2, -2, 1):
        scene.move(scalar.animate(rate_func=linear).set_value(target), seconds=3)
        scene.pause(1.5)


def negate_original(scene, panel):
    """A separate blue-to-blue operation; the working scalar stays at one."""
    panel.clear_updaters(recursive=True)
    old = panel.original
    temporary = VGroup(
        FixedNumber(old, BLUE), scene.math(r"\cdot", size=34),
        FixedNumber(-1, WHITE), scene.math("=", size=34),
        FixedNumber(-old, BLUE),
    )
    for term, position in zip(temporary, panel.equation):
        term.move_to(position)
    scene.move(FadeOut(panel.equation), FadeIn(temporary), seconds=.6)
    scene.pause(1)
    # Follow the normal to the rotating arrow, with upright glyphs off its shaft.
    direction = 1 if old > 0 else -1
    def rotation_label(label):
        start, end = panel.blue.get_start(), panel.blue.get_end()
        vector = end - start
        normal = np.array([-vector[1], vector[0], 0]) / np.linalg.norm(vector)
        label.move_to((start + end) / 2 + direction * normal * .32)
    panel.blue_value.add_updater(rotation_label)
    # The product flips horizontally: its path never sweeps over axis labels.
    flip = ValueTracker(old)
    panel.red.add_updater(lambda mob: mob.set_value(flip.get_value()))
    panel.red_value.add_updater(lambda mob: mob.set_value(flip.get_value()).move_to(
        (panel.red.get_start() + panel.red.get_end()) / 2 + DOWN * .29))
    scene.move(Rotate(panel.blue, PI, about_point=panel.blue.get_start(), rate_func=linear),
               flip.animate(rate_func=linear).set_value(-old), seconds=2)
    panel.clear_updaters(recursive=True)
    panel.original = -old
    for number in (panel.blue_value, panel.red_value, panel.factor, panel.result):
        number.set_value(-old)
    scene.move(panel.blue_value.animate.move_to(
        (panel.blue.get_start() + panel.blue.get_end()) / 2 + UP * .29), seconds=.3)
    scene.pause(1)
    scene.move(FadeOut(temporary), FadeIn(panel.equation), seconds=.6)
    temporary.clear_updaters(recursive=True)
    panel.clear_updaters(recursive=True)
    scene.remove(*panel.get_family())
    scene.add(panel.bind())
    scene.pause(1)


def render_section(self, *, standalone=False):
    start = self.lesson_seconds
    # Use the common transition/clock, with only mathematical objects on screen.
    self.header = ()
    scalar = ValueTracker(1)
    panel = MultiplicationPanel(self, scalar)
    self.replace_body(VGroup(panel.axis))
    self.move(Create(panel.blue), FadeIn(panel.blue_value), seconds=1)
    self.pause(1)
    times = self.math(r"\times", size=34).move_to(panel.dot)
    self.move(FadeIn(panel.factor), FadeIn(times), FadeIn(panel.multiplier), seconds=.8)
    self.pause(1)
    self.move(Transform(times, panel.dot), seconds=1)
    self.remove(times)
    self.add(panel.dot)
    self.pause(.8)
    self.move(Create(panel.red), FadeIn(panel.red_value),
              FadeIn(panel.equals), FadeIn(panel.result), seconds=1)
    # Consolidate the revealed objects before binding or copying anything.
    self.remove(*list(self.mobjects))
    self.add(panel)
    panel.bind()
    self.pause(1.5)
    sliding_routine(self, scalar)

    negate_original(self, panel)
    sliding_routine(self, scalar)

    panel.clear_updaters(recursive=True)
    left = MultiplicationPanel(self, scalar, -4, -3.55, 5.5)
    right = MultiplicationPanel(self, scalar, -4, 3.55, 5.5)
    # Copies are transition-only. Install fresh panels with their own closures.
    twin = panel.copy()
    self.add(twin)
    divider = Line([0, 3.5, 0], [0, -3.6, 0],
                   stroke_color="#30415A", stroke_width=1)
    self.move(Transform(panel, left), Transform(twin, right),
              Create(divider), seconds=2)
    self.remove(panel, twin)
    self.add(left.bind(), right.bind())
    self.pause(1.5)
    negate_original(self, right)
    sliding_routine(self, scalar)
    for item in (left, right):
        item.clear_updaters(recursive=True)
    self.finish_beat(start, SIGNED_MULTIPLICATION_SECONDS)


class SignedMultiplication(TopicScene):
    """Shared signed-vector sequence with two synchronized final panels."""

    video_number = 2
    source_file = __file__
    output_identity = "algebra/stage1_arithmetic_foundations/03_signed_multiplication.mp4"
    section = render_section
    planned_seconds = SIGNED_MULTIPLICATION_SECONDS
