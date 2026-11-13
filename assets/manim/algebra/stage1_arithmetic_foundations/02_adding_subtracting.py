"""Signed addition with arrows; Manim Community 0.17.3.

    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/02_adding_subtracting.py AddingSubtracting

Uses the same render_section and clock in standalone and combined videos.
Final MP4 (repository-relative, independent of cwd):
    ../manim_media/videos/algebra/stage1_arithmetic_foundations/02_adding_subtracting.mp4
"""

from pathlib import Path
import sys
import numpy as np

REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import (
    DOWN, UP, PI, RED, Arrow, Create, DashedLine, Dot, FadeIn, FadeOut,
    Line, NumberLine, Rotate, Transform, UpdateFromAlphaFunc, VGroup, linear,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    BLUE, GREEN, MUTED, TopicScene, ADDING_SUBTRACTING_SECONDS,
)


def _arrow_label(scene, text, color):
    # A vertical shaft can pass behind its upright label during a half-turn.
    return scene.math(text, size=27).set_color(color).add_background_rectangle(
        color="#0B1426", opacity=1, buff=0.06
    )


class SignedArrow(VGroup):
    """Rotate only the geometry; the upright label follows its midpoint."""

    def __init__(self, scene, axis, value, color, height, *, below=False):
        self.value = value
        self.label_direction = DOWN if below else UP
        self.arrow = Arrow(
            axis.n2p(0) + UP * height, axis.n2p(value) + UP * height,
            buff=0, color=color, stroke_width=7 if below else 4,
            max_tip_length_to_length_ratio=0.13,
        ).set_z_index(2 if below else 3)
        self.label = _arrow_label(scene, str(value), color)
        self.label.set_z_index(4)
        super().__init__(self.arrow, self.label)
        self.attach_label()

    def attach_label(self):
        self.label.move_to(
            (self.arrow.get_start() + self.arrow.get_end()) / 2
            + self.label_direction * 0.25
        )
        self.label.add_updater(lambda label: label.move_to(
            (self.arrow.get_start() + self.arrow.get_end()) / 2
            + self.label_direction * 0.25
        ))


class AdditionPanel(VGroup):
    def __init__(self, scene, center=0, length=5.7):
        self.center_x = center
        self.axis = NumberLine(
            x_range=[-7, 7, 1], length=length, include_numbers=True,
            font_size=18, color=MUTED, stroke_width=2,
        ).move_to([center, -2.05, 0])
        # Leave room for the blue arrow's *lower* semicircle on its second turn.
        self.blue = SignedArrow(scene, self.axis, 4, BLUE, 1.9, below=True)
        self.red = SignedArrow(scene, self.axis, 3, RED, 2.6)
        super().__init__(self.axis, self.blue, self.red)


def _term(value):
    return str(value) if value >= 0 else f"({value})"


class EquationHeading(VGroup):
    """Persistent, individually addressable signed terms around a fixed plus."""

    def __init__(self, scene, panel):
        self.pivot = np.array([panel.center_x - 0.25, 2.05, 0.0])
        # The upper half-circle and upright glyphs fit below the title rule.
        self.radius = 0.45
        self.blue = scene.math("4", size=26).set_color(BLUE)
        self.red = scene.math("3", size=26).set_color(RED)
        self.plus = scene.math("+", size=26).move_to(self.pivot)
        self.blue.move_to(self.pivot + np.array([-self.radius, 0, 0]))
        self.red.move_to(self.pivot + np.array([self.radius, 0, 0]))
        self.equals = scene.math("=", size=26).move_to(self.pivot + [0.96, 0, 0])
        self.result = scene.math("7", size=26).set_color(GREEN)
        self.result.move_to(self.pivot + [1.42, 0, 0])
        self.blue_first = True
        # Equality is added separately only when the construction is complete.
        super().__init__(self.blue, self.plus, self.red)
        self.set_z_index(6)

    def swap_animations(self):
        # Move only the centers: glyphs and complete parentheses stay upright.
        animations = []
        for term in (self.blue, self.red):
            start_angle = PI if term.get_x() < self.plus.get_x() else 0
            pivot, radius = self.pivot.copy(), self.radius

            def orbit(obj, alpha, start=start_angle, center=pivot, r=radius):
                angle = start - PI * alpha
                obj.move_to(center + r * np.array([np.cos(angle), np.sin(angle), 0]))

            animations.append(UpdateFromAlphaFunc(term, orbit, rate_func=linear))
        self.blue_first = not self.blue_first
        return animations


def _negate(scene, *arrows):
    """All requested half-turns share one play, about their individual tails."""
    animations = []
    for signed in arrows:
        signed.value = -signed.value
        label_text = r"-(-4)" if signed.value == 4 else str(signed.value)
        target = _arrow_label(scene, label_text, signed.arrow.get_color())
        target.move_to(signed.label)
        animations.extend([
            Rotate(signed.arrow, angle=PI, about_point=signed.arrow.get_start(),
                   rate_func=linear),
            Transform(signed.label, target, suspend_mobject_updating=False),
        ])
        if hasattr(signed, "heading_term"):
            term = signed.heading_term
            animations.append(Transform(term, scene.math(_term(signed.value), size=26)
                                        .set_color(signed.arrow.get_color()).move_to(term)))
    scene.move(*animations, seconds=1.8)


def _addition(scene, panels, *, keep_final=False):
    """Synchronized constructions, result lanes and persistent circular swaps."""
    for order in range(2):
        results, movers, resets, markers, resultants = [], [], [], [], []
        for panel in panels:
            first, second = ((panel.blue, panel.red) if panel.heading.blue_first
                             else (panel.red, panel.blue))
            total = first.value + second.value
            result = scene.math(str(total), size=26).set_color(GREEN)
            result.move_to(panel.heading.result)
            panel.heading.result.become(result)
            delta = first.arrow.get_end() - second.arrow.get_start()
            origin = second.arrow.get_start().copy()
            endpoint = second.arrow.get_end() + delta
            axis_point = panel.axis.n2p(total)
            # Exact connected endpoints, behind the operand shafts at emergence.
            resultant = Arrow(first.arrow.get_start(), endpoint, buff=0,
                              color=GREEN, stroke_width=7, tip_length=0.22,
                              max_stroke_width_to_length_ratio=30,
                              max_tip_length_to_length_ratio=0.4).set_z_index(1)
            label = _arrow_label(scene, str(total), GREEN).set_z_index(4)
            label.move_to((resultant.get_start() + resultant.get_end()) / 2 + DOWN * 0.28)
            resultants.append(VGroup(resultant, label))
            lane_shift = UP * (-1.25 - resultant.get_start()[1])
            marker = VGroup(
                DashedLine(endpoint + lane_shift, axis_point,
                           color=GREEN, stroke_width=2),
                Dot(axis_point, color=GREEN, radius=0.055),
            )
            results.extend([panel.heading.equals, panel.heading.result])
            movers.append((second, delta))
            resets.append((second, origin))
            markers.append(marker)
        scene.pause(1.2)
        scene.move(*[signed.arrow.animate(rate_func=linear).shift(delta)
                     for signed, delta in movers], seconds=2)
        scene.move(*[Create(group[0]) for group in resultants],
                   *[FadeIn(group[1]) for group in resultants],
                   *[FadeIn(result) for result in results], seconds=0.8)
        scene.move(*[group.animate(rate_func=linear).shift(
                       UP * (-1.25 - group[0].get_start()[1]))
                     for group in resultants], seconds=1.2)
        scene.move(*[Create(marker) for marker in markers], seconds=0.6)
        scene.pause(2.5)
        if keep_final and order == 1:
            continue
        # Clear the completed sum before moving either operand into a new one.
        scene.move(*[FadeOut(obj) for obj in results + markers + resultants],
                   seconds=0.6)
        swaps = []
        if order == 0:
            for panel in panels:
                swaps.extend(panel.heading.swap_animations())
        scene.move(*[signed.arrow.animate(rate_func=linear).shift(
                       origin - signed.arrow.get_start())
                     for signed, origin in resets],
                   *swaps, seconds=1.8)
    scene.pause(0.8)


def render_section(self, *, standalone=False):
    start = self.topic("Suma de números con signo")
    # Keep the unit scale unchanged when the centered view splits into panels.
    opening = AdditionPanel(self)
    self.move(Create(opening.axis), seconds=1)
    self.move(Create(opening.blue.arrow), FadeIn(opening.blue.label), seconds=1.2)
    self.move(Create(opening.red.arrow), FadeIn(opening.red.label), seconds=1.2)
    self.pause(2.5)

    left, right = AdditionPanel(self, -3.45), AdditionPanel(self, 3.45)
    divider = Line([0, 2.3, 0], [0, -3.08, 0],
                   stroke_color="#30415A", stroke_width=1)
    for panel in (left, right):
        panel.heading = EquationHeading(self, panel)
        panel.blue.heading_term = panel.heading.blue
        panel.red.heading_term = panel.heading.red
    headings = VGroup(left.heading, right.heading)
    # Freeze label updaters while morphing the opening into two equal copies.
    for panel in (opening, left, right):
        panel.blue.label.clear_updaters()
        panel.red.label.clear_updaters()
    twin = opening.copy()
    self.add(twin)
    self.move(Transform(opening, left), Transform(twin, right),
              Create(divider), FadeIn(headings), seconds=2)
    self.remove(opening, twin, opening.axis, opening.blue.arrow,
                opening.blue.label, opening.red.arrow, opening.red.label)
    self.add(left, right)
    for panel in (left, right):
        panel.blue.attach_label()
        panel.red.attach_label()
    self.pause(1.5)

    _negate(self, right.red)
    self.pause(0.8)
    _negate(self, right.blue)
    self.pause(1.2)
    caption = self.words("Coloca la cola de la segunda flecha en la punta de la primera.",
                         24, MUTED).move_to(DOWN * 3.5)
    self.move(FadeIn(caption), seconds=0.8)
    _addition(self, (left, right))

    self.move(FadeOut(caption), seconds=0.6)
    # The next comparison starts blue-first, using the same visible term objects.
    self.move(*left.heading.swap_animations(), *right.heading.swap_animations(),
              seconds=1.8)
    _negate(self, left.blue, right.blue)
    self.pause(1.5)
    simplified = _arrow_label(self, "4", BLUE).move_to(right.blue.label)
    explanation = self.words("El opuesto de −4 es 4: −(−4) = 4.", 27)
    explanation.move_to(DOWN * 3.5)
    self.move(Transform(right.blue.label, simplified), FadeIn(explanation), seconds=0.8)
    self.pause(2.5)
    self.move(Transform(explanation, self.words(
        "Las sumas tienen resultados opuestos.", 27
    ).move_to(DOWN * 3.5)), seconds=0.8)
    _addition(self, (left, right), keep_final=True)
    self.finish_beat(start, ADDING_SUBTRACTING_SECONDS)


class AddingSubtracting(TopicScene):
    """The shared signed-addition sequence, independently renderable."""

    video_number = 1
    source_file = __file__
    output_identity = "algebra/stage1_arithmetic_foundations/02_adding_subtracting.mp4"
    section = render_section
    planned_seconds = ADDING_SUBTRACTING_SECONDS
