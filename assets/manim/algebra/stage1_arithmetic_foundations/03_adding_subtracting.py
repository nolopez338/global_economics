"""Signed addition with arrows; Manim Community 0.17.3.

    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/03_adding_subtracting.py AddingSubtracting

Uses the same render_section and clock in standalone and combined videos.
Final MP4 (repository-relative, independent of cwd):
    ../manim_media/videos/algebra/stage1_arithmetic_foundations/02_adding_subtracting.mp4
"""

from pathlib import Path
import sys
import shutil
import subprocess
import manimpango
import numpy as np

REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import (
    DOWN, UP, PI, RED, WHITE, NORMAL, Create, DashedLine, Dot, FadeIn, FadeOut,
    Line, LineJointType, MathTex, NumberLine, Rotate, Text, TexTemplate,
    Transform, UpdateFromAlphaFunc, VGroup, VMobject, smooth, RIGHT,
    bezier, interpolate_color, register_font,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    BLUE, GREEN, MUTED, TopicScene, ADDING_SUBTRACTING_SECONDS,
)


FONT = "CMU Serif"
SYMBOL_STROKE_AT_108 = 1.2
MINUS_WIDTH_FACTOR = 0.75


def _cubic_path(bend):
    """Pointwise cubic translation/morph; Animation supplies easing once."""
    def path(start, end, alpha):
        delta = end - start
        return bezier([start, start + delta / 3 + bend,
                       start + 2 * delta / 3 + bend, end])(alpha)

    return path


def _bezier_shift(obj, delta, *, bend):
    # A common offset for every point keeps glyphs upright and shafts straight.
    return Transform(obj, obj.copy().shift(delta), path_func=_cubic_path(bend),
                     rate_func=smooth)


def cmu_text(message, *, font_size):
    """Shape Roman text in a temporary CE font scope; cached copies need none."""
    lookup = shutil.which("kpsewhich")
    if lookup is None:
        raise RuntimeError("CMU Serif Roman unavailable: kpsewhich not found")
    try:
        found = subprocess.run(
            [lookup, "cmunrm.otf"], capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise RuntimeError(
            "CMU Serif Roman unavailable: kpsewhich could not locate cmunrm.otf"
        ) from error
    if not found or not Path(found).is_file():
        raise FileNotFoundError("CMU Serif Roman unavailable: cmunrm.otf missing")
    with register_font(Path(found)):
        if FONT not in manimpango.list_fonts():
            raise RuntimeError("CMU Serif Roman registration did not expose the family")
        return Text(message, font=FONT, weight=NORMAL, slant=NORMAL,
                    disable_ligatures=True, font_size=font_size, color=WHITE).set_stroke(width=0)


def emphasize_symbol(glyph, *, font_size):
    """Stroke one filled glyph without changing its outline points or position."""
    glyph.set_fill(WHITE, opacity=1)
    glyph.set_stroke(WHITE, width=SYMBOL_STROKE_AT_108 * font_size / 108,
                     opacity=1)
    return glyph


def shorten_minus(glyph):
    """Compress only U+2212 horizontally, retaining center and vertical metrics."""
    glyph.stretch(MINUS_WIDTH_FACTOR, 0, about_point=glyph.get_center())
    return glyph


def axis_label(value, *, position):
    message = str(value).replace("-", "−")
    label = cmu_text(message, font_size=22)
    # Position using the original shaped bounds so compression cannot move digits.
    label.move_to(position)
    # Shape the complete label first; preserve its kerning and baseline offsets.
    for index, char in enumerate(message):
        if char == "−":
            shorten_minus(label[index])
            emphasize_symbol(label[index], font_size=22)
    return label


def _words(message, size=30, color=WHITE):
    result = cmu_text(message, font_size=size).set_stroke(width=0).set_color(color)
    if result.width > 12.3:
        result.scale_to_fit_width(12.3)
    return result


def _math(*pieces, size=49):
    # Computer Modern, matching the skill's complete default LaTeX template.
    template = TexTemplate(
        tex_compiler="latex", output_format=".dvi",
        documentclass=r"\documentclass[preview]{standalone}",
        preamble=r"""
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
""",
    )
    return MathTex(*pieces, font_size=size, tex_template=template)


class OpenArrow(VGroup):
    """Stable shaft/head slots; exact centerline endpoints, including at zero."""

    def __init__(self, start, end, color, scale):
        super().__init__(VMobject(), VMobject())
        self.geometry(start, end, color, scale)

    def get_color(self):
        return self[0].get_color()

    def get_start(self):
        return self[0].get_start() if self[0].has_points() else self.zero_point.copy()

    def get_end(self):
        return self[0].get_end() if self[0].has_points() else self.zero_point.copy()

    def geometry(self, start, end, color, scale):
        shaft, head = self
        self.zero_point = np.array(start).copy()
        delta = end - start
        length = np.linalg.norm(delta)
        if length < 1e-10:
            shaft.clear_points()
            head.clear_points()
            return
        direction = delta / length
        transverse = np.array([-direction[1], direction[0], 0])
        nominal = 0.34 * scale
        head_scale = length / (length**4 + (nominal / 0.48)**4)**0.25
        head_length, head_width = nominal * head_scale, 0.14 * scale * head_scale
        stroke = 5 * scale * min(1, length / (0.55 * scale))

        def local(x, y):
            return end + x * head_length * direction + y * head_width * transverse

        shaft.set_points_as_corners([start, end])
        head.clear_points()
        head.start_new_path(local(-1, 0.5))
        head.add_cubic_bezier_curve_to(local(-0.72, 0.20), local(-0.28, 0.12), end)
        head.add_cubic_bezier_curve_to(local(-0.28, -0.12), local(-0.72, -0.20),
                                      local(-1, -0.5))
        head.joint_type = LineJointType.MITER
        for slot in self:
            slot.set_fill(color, opacity=0)
            slot.set_stroke(color, width=stroke, opacity=1)
        # CE Cairo has butt rear caps; miter ink can project beyond the tip anchor.


def _arrow_label(scene, text, color):
    return _words(text.replace("-", "−"), 27, color)


def _label_point(arrow, below=False, label=None):
    start, end = arrow.get_start(), arrow.get_end()
    delta = end - start
    length = np.linalg.norm(delta)
    normal = (np.array([-delta[1], delta[0], 0]) / length
              if length > 1e-10 else UP.copy())
    # Choose a continuous side relative to the directed arrow during rotation.
    clearance = 0.29 if label is None else max(
        0.29, (abs(normal[0]) * label.width + abs(normal[1]) * label.height) / 2 + 0.12)
    return (start + end) / 2 + (-1 if below else 1) * clearance * normal


class SignedArrow(VGroup):
    """Rotate geometry alone; upright labels follow its normalized normal."""

    def __init__(self, scene, axis, value, color, height, *, below=False):
        self.value, self.below = value, below
        self.arrow = OpenArrow(axis.n2p(0) + UP * height,
                               axis.n2p(value) + UP * height, color, 0.65)
        self.arrow.set_z_index(2 if below else 3)
        self.label = _arrow_label(scene, str(value), color).set_z_index(4)
        super().__init__(self.arrow, self.label)
        self.attach_label()

    def attach_label(self):
        self.label.clear_updaters()
        self.label.move_to(_label_point(self.arrow, self.below, self.label))
        self.label.add_updater(lambda label: label.move_to(
            _label_point(self.arrow, self.below, self.label)))


class AdditionPanel(VGroup):
    def __init__(self, scene, center=0, length=5.7):
        self.center_x = center
        self.axis = NumberLine(
            x_range=[-7, 7, 1], length=length, include_numbers=False,
            tick_size=0.055, color=MUTED, stroke_width=1.4,
        ).move_to([center, -2.05, 0])
        self.axis_labels = VGroup(*[
            _words(str(value).replace("-", "−"), 18, MUTED).move_to(
                self.axis.n2p(value) + DOWN * 0.32)
            for value in (-7, -5, 0, 5, 7)
        ])
        # Leave room for the blue arrow's *lower* semicircle on its second turn.
        self.blue = SignedArrow(scene, self.axis, 4, BLUE, 1.9, below=True)
        self.red = SignedArrow(scene, self.axis, 3, RED, 2.6)
        # These are order slots, not color slots. Preserve exact common tails
        # even after the second operand has moved into a head-to-tail sum.
        self.operand_tails = (self.blue.arrow.get_start().copy(),
                              self.red.arrow.get_start().copy())
        super().__init__(self.axis, self.axis_labels, self.blue, self.red)

    def swap_animations(self):
        """Circular terms and translating arrows share one eased play."""
        first, second = ((self.blue, self.red) if self.heading.blue_first
                         else (self.red, self.blue))
        animations = self.heading.swap_animations()
        # Route the outgoing first operand left/up and the incoming first
        # operand right/down. Separate corridor centers allow for the widest
        # label (including the later double negative), not just shaft tips.
        # Each cubic has explicit controls P0 + delta/3 + bend and
        # P0 + 2*delta/3 + bend; its midpoint offset is 3*bend/4.
        for signed, target, side in (
                (first, self.operand_tails[1], -1),
                (second, self.operand_tails[0], 1)):
            delta = target - signed.arrow.get_start()
            midpoint = (signed.arrow.get_start() + signed.arrow.get_end()) / 2
            corridor_x = self.center_x + side * 1.15
            bend = np.array([
                (corridor_x - midpoint[0] - delta[0] / 2) / 0.75,
                -side * 0.65,
                0,
            ])
            # Translate geometry only; the existing ordered label updater
            # follows the same progress without rotating or replacing glyphs.
            animations.append(_bezier_shift(signed.arrow, delta, bend=bend))
        return animations


def _term(value):
    return str(value) if value >= 0 else f"({value})"


class EquationHeading(VGroup):
    """Persistent, individually addressable signed terms around a fixed plus."""

    def __init__(self, scene, panel):
        self.pivot = np.array([panel.center_x - 0.25, 2.05, 0.0])
        # The upper half-circle and upright glyphs fit below the title rule.
        self.radius = 0.45
        self.blue = _math("4", size=26).set_color(BLUE)
        self.red = _math("3", size=26).set_color(RED)
        self.plus = _math("+", size=26).move_to(self.pivot)
        self.blue.move_to(self.pivot + np.array([-self.radius, 0, 0]))
        self.red.move_to(self.pivot + np.array([self.radius, 0, 0]))
        self.equals = _math("=", size=26).move_to(self.pivot + [0.96, 0, 0])
        self.result = _math("7", size=26).set_color(GREEN)
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

            animations.append(UpdateFromAlphaFunc(term, orbit, rate_func=smooth))
        self.blue_first = not self.blue_first
        return animations


def _negate(scene, *arrows):
    """All requested half-turns share one play, about their individual tails."""
    animations = []
    for signed in arrows:
        signed.value = -signed.value
        label_text = "−(−4)" if signed.value == 4 else str(signed.value)
        target = _arrow_label(scene, label_text, signed.arrow.get_color())
        target.move_to(signed.label)
        animations.extend([
            Rotate(signed.arrow, angle=PI, about_point=signed.arrow.get_start(),
                   rate_func=smooth),
            Transform(signed.label, target, suspend_mobject_updating=False),
        ])
        if hasattr(signed, "heading_term"):
            term = signed.heading_term
            animations.append(Transform(term, _math(_term(signed.value), size=26)
                                        .set_color(signed.arrow.get_color()).move_to(term)))
    scene.move(*animations, seconds=1.8)
    for signed in arrows:
        tail = signed.arrow.get_start().copy()
        unit = np.linalg.norm(signed.arrow.get_end() - tail) / abs(signed.value)
        signed.arrow.geometry(tail, tail + np.array([unit * signed.value, 0, 0]),
                              signed.arrow[0].get_color(), 0.65)
        signed.label.move_to(_label_point(signed.arrow, signed.below, signed.label))


def _addition(scene, panels, *, keep_final=False):
    """Synchronized constructions, result lanes and persistent circular swaps."""
    for order in range(2):
        results, movers, resets, markers, resultants = [], [], [], [], []
        for panel in panels:
            first, second = ((panel.blue, panel.red) if panel.heading.blue_first
                             else (panel.red, panel.blue))
            total = first.value + second.value
            result = _math(str(total), size=26).set_color(GREEN)
            result.move_to(panel.heading.result)
            panel.heading.result.become(result)
            delta = first.arrow.get_end() - second.arrow.get_start()
            origin = second.arrow.get_start().copy()
            endpoint = second.arrow.get_end() + delta
            axis_point = panel.axis.n2p(total)
            # Exact connected endpoints, behind the operand shafts at emergence.
            resultant = OpenArrow(first.arrow.get_start(), endpoint, GREEN, 0.65)
            resultant.set_z_index(1)
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
            # Bow away from the other operand's lane until the tails connect.
            bend = (DOWN if second.below else UP) * 0.18
            movers.append((second, delta, bend))
            resets.append((second, origin, bend))
            markers.append(marker)
        scene.pause(1.2)
        scene.move(*[_bezier_shift(signed.arrow, delta, bend=bend)
                     for signed, delta, bend in movers], seconds=2)
        scene.move(*[Create(group[0]) for group in resultants],
                   *[FadeIn(group[1]) for group in resultants],
                   *[FadeIn(result) for result in results], seconds=0.8)
        # Bow toward the panel interior, leaving the outer frame edge clear.
        scene.move(*[_bezier_shift(group,
                       UP * (-1.25 - group[0].get_start()[1]),
                       bend=RIGHT * (-0.12 if group[0].get_end()[0]
                                     > group[0].get_start()[0] else 0.12))
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
                # The permutation also resets the connected second arrow;
                # never animate that same arrow a second time in this play.
                swaps.extend(panel.swap_animations())
        else:
            swaps.extend(_bezier_shift(signed.arrow,
                         origin - signed.arrow.get_start(), bend=bend)
                         for signed, origin, bend in resets)
        scene.move(*swaps, seconds=1.8)
    scene.pause(0.8)


def _incoming_equation():
    """Only 01's final compact positive state, from the identical shaped run."""
    source = cmu_text("0123456789−.a=", font_size=108)
    source.shift(UP * (0.9 - source[0].get_y()))
    glyphs = dict(zip("0123456789−.a=", source))
    for glyph in glyphs.values():
        glyph.set_x(0)
    equals = emphasize_symbol(glyphs["="].copy(), font_size=108)
    variable = glyphs["a"].copy()
    edge = 0.5 * 0.01 * SYMBOL_STROKE_AT_108
    variable.set_x(equals.get_left()[0] - edge - 0.24 - variable.width / 2)
    digit = glyphs["1"].copy()
    digit.set_x(equals.get_right()[0] + edge + 0.24 + digit.width / 2)
    return variable, equals, digit


def _standalone_opening(scene, opening, title, rule):
    incoming_title = _words("Números como vectores", 40).move_to(UP * 3.12)
    variable, equals, digit = _incoming_equation()
    axis = NumberLine(
        x_range=[-5, 5, 1], length=12.1, include_numbers=False,
        include_tip=False, tick_size=0.055, color=WHITE, stroke_width=1.4,
    ).move_to(DOWN * 1.65).set_opacity(0.42)
    labels = VGroup(*[
        axis_label(value, position=axis.n2p(value) + DOWN * 0.42)
        for value in (-5, 0, 5)
    ]).set_opacity(0.75)
    arrow = OpenArrow(axis.n2p(0) + UP * 0.18, axis.n2p(1) + UP * 0.18,
                      WHITE, 1)
    # Immediate endpoint, including baseline, symbol stroke and axis opacity.
    scene.add(incoming_title, variable, equals, digit, axis, labels, arrow)
    scene.pause(0.8)
    scene.move(Transform(incoming_title, title), FadeOut(variable), FadeOut(equals),
               Create(rule), seconds=0.8)

    extra_ticks = VGroup(*[Line(UP * 0.055, DOWN * 0.055)
                           for _ in range(4)]).set_opacity(0)
    extra_labels = VGroup(opening.axis_labels[1].copy(),
                          opening.axis_labels[-2].copy()).set_opacity(0)
    # Endpoint glyphs -5/+5 evolve into -7/+7 as the domain expands;
    # the central zero remains fixed. New interior labels enter at +/-5.
    old_labels = [label.copy() for label in labels]
    target_labels = [opening.axis_labels[index].copy() for index in (0, 2, 4)]
    label_pairs = []
    for old, target in zip(old_labels, target_labels):
        old.align_data(target)
        label_pairs.append((old, target))
    old_digit, target_digit = digit.copy(), opening.blue.label[0].copy()
    # Force contour alignment even when CE sees equal total point counts.
    if old_digit.get_num_points() == target_digit.get_num_points():
        old_digit.add_line_to(old_digit.get_last_point())
    old_digit.align_points(target_digit)
    exact_digit = opening.blue.label[0].copy()
    initial_digit = digit.copy()
    start_center, end_center = initial_digit.get_center(), exact_digit.get_center()
    # Use both endpoint bounds: aligned outline interpolation cannot exceed
    # their maximum width/height. Keep the turn well left of the x=0 tail;
    # the lower handle delays re-entry until the shaft has risen above it.
    # The shaft rises from y=-1.47 to -0.15 while the axis stays below -1.65.
    # This low approach stays above the axis and below the late rising shaft,
    # rather than aiming at a lower-label position that itself moves each frame.
    half_width = max(initial_digit.width, exact_digit.width) / 2
    half_height = max(initial_digit.height, exact_digit.height) / 2
    detour_x = arrow.get_start()[0] - 2.6 - half_width
    digit_path = bezier([
        start_center,
        np.array([detour_x, start_center[1], 0]),
        np.array([detour_x, end_center[1] - 1.1 - half_height, 0]),
        end_center,
    ])
    driver = VGroup(axis, labels, arrow, digit, extra_ticks, extra_labels)
    scene.add(driver)

    def evolve(_driver, alpha):
        # One ordered callback: update the coordinate map, then ticks/labels,
        # then the represented vector and its single upright numeral slot.
        extent = 5 + 2 * alpha
        length = 12.1 + (5.7 - 12.1) * alpha
        y = -1.65 - 0.4 * alpha
        axis.x_range = np.array([-extent, extent, 1])
        axis.x_min, axis.x_max = -extent, extent
        axis.set_points_as_corners([[-length / 2, y, 0], [length / 2, y, 0]])
        color = interpolate_color(WHITE, MUTED, alpha)
        axis.set_stroke(color, width=1.4, opacity=0.42 + 0.58 * alpha)
        for value, tick in zip(range(-5, 6), axis.ticks):
            coordinate = np.sign(value) * extent if abs(value) == 5 else value
            point = axis.n2p(coordinate)
            tick.set_points_as_corners([point + UP * 0.055, point + DOWN * 0.055])
        for value, tick in zip((-6, -5, 5, 6), extra_ticks):
            # New range grows at its boundary; never place hidden geometry
            # outside the frame or detach an existing mathematical tick.
            point = axis.n2p(np.clip(value, -extent, extent))
            tick.set_points_as_corners([point + UP * 0.055, point + DOWN * 0.055])
            tick.set_stroke(color, width=1.4, opacity=min(1, max(0, extent - abs(value))) * alpha)
        for value, label, (old, target) in zip((-5, 0, 5), labels, label_pairs):
            for slot, first, last in zip(label.get_family(), old.get_family(), target.get_family()):
                slot.interpolate(first, last, alpha)
            coordinate = value * extent / 5
            label.move_to(axis.n2p(coordinate) + DOWN * (0.42 - 0.10 * alpha))
        for value, label in zip((-5, 5), extra_labels):
            label.move_to(axis.n2p(np.clip(value, -extent, extent))
                          + DOWN * (0.42 - 0.10 * alpha))
            # Wait for separation from the migrating endpoint glyphs.
            label.set_opacity(smooth(np.clip((alpha - 0.30) / 0.40, 0, 1)))
        height = 0.18 + (1.9 - 0.18) * alpha
        value = 1 + 3 * alpha
        arrow.geometry(axis.n2p(0) + UP * height, axis.n2p(value) + UP * height,
                       interpolate_color(WHITE, BLUE, alpha), 1 - 0.35 * alpha)
        digit.interpolate(old_digit, target_digit, alpha)
        # Spatial cubic and outline interpolation share the already eased phase.
        # Translate the single glyph slot without rotating its changing outline.
        digit.move_to(digit_path(alpha))

    scene.move(UpdateFromAlphaFunc(driver, evolve, rate_func=smooth), seconds=3.2)
    evolve(driver, 1)
    # Restore exact targets within the surviving shaft/head and glyph slots.
    # Merge new ticks into the same axis in mathematical order for the split.
    all_ticks = dict(zip(range(-4, 5), axis.ticks[1:-1]))
    all_ticks[-7], all_ticks[7] = axis.ticks[0], axis.ticks[-1]
    all_ticks.update(zip((-6, -5, 5, 6), extra_ticks))
    axis.ticks.submobjects = [all_ticks[value] for value in range(-7, 8)]
    axis.length, axis.unit_size = 5.7, 5.7 / 14
    for tick, target in zip(axis.ticks, opening.axis.ticks):
        tick.set_points(target.points.copy()).match_style(target)
    axis.set_points(opening.axis.points.copy())
    axis.match_style(opening.axis)
    ordered_labels = [labels[0], extra_labels[0], labels[1], extra_labels[1], labels[2]]
    for label, target in zip(ordered_labels, opening.axis_labels):
        label.become(target)
    arrow.geometry(opening.blue.arrow.get_start(), opening.blue.arrow.get_end(), BLUE, 0.65)
    arrow.set_z_index(2)
    digit.set_points(exact_digit.points.copy()).match_style(exact_digit)
    scene.remove(driver, axis, labels, arrow, digit, extra_ticks, extra_labels,
                 incoming_title)
    opening.axis = axis
    opening.axis_labels = VGroup(*ordered_labels)
    opening.blue.arrow = arrow
    opening.blue.label = VGroup(digit).set_z_index(4)
    opening.blue.submobjects = [arrow, opening.blue.label]
    opening.blue.attach_label()
    opening.submobjects = [axis, opening.axis_labels, opening.blue, opening.red]
    scene.add(title, axis, opening.axis_labels, arrow, opening.blue.label)
    scene.pause(0.6)
    scene.move(Create(opening.red.arrow), FadeIn(opening.red.label), seconds=1)
    scene.pause(1)


def render_section(self, *, standalone=False):
    start = self.lesson_seconds
    title = _words("Suma de números con signo", 40).move_to(UP * 3.12)
    rule = Line([-6.2, 2.65, 0], [6.2, 2.65, 0],
                stroke_color="#30415A", stroke_width=1)
    opening = AdditionPanel(self)
    self.header = (title, rule)
    if standalone:
        _standalone_opening(self, opening, title, rule)
    else:
        # 00 has its own introduction and deliberately does not include 01.
        old = list(self.mobjects)
        self.move(*[FadeOut(obj) for obj in old], FadeIn(title), Create(rule), seconds=0.8)
        self.move(Create(opening.axis), FadeIn(opening.axis_labels), seconds=1)
        self.move(Create(opening.blue.arrow), FadeIn(opening.blue.label), seconds=1.2)
        self.pause(1)
        self.move(Create(opening.red.arrow), FadeIn(opening.red.label), seconds=1)
        self.pause(2.4)
    # Both entrances: 7.4 s. Remaining lesson: 61.7 s; final hold: 4.9 s.

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
    self.remove(opening.axis, opening.axis_labels, opening.blue.arrow,
                opening.blue.label, opening.red.arrow, opening.red.label)
    self.add(opening)
    twin = opening.copy()
    self.add(twin)
    # A shallow common bow clears the axis/arrow lanes without tilting labels
    # or bending the mathematical lines during the two-panel translation.
    self.move(Transform(opening, left, path_func=_cubic_path(UP * 0.12)),
              Transform(twin, right, path_func=_cubic_path(UP * 0.12)),
              Create(divider), FadeIn(headings), seconds=2)
    self.remove(opening, twin, opening.axis, opening.blue.arrow,
                opening.blue.label, opening.red.arrow, opening.red.label, opening.axis_labels)
    self.add(left, right)
    for panel in (left, right):
        panel.blue.attach_label()
        panel.red.attach_label()
    self.pause(1.5)

    _negate(self, right.red)
    self.pause(0.8)
    _negate(self, right.blue)
    self.pause(1.2)
    caption = _words("Coloca la cola de la segunda flecha en la punta de la primera.",
                         24, MUTED).move_to(DOWN * 3.5)
    self.move(FadeIn(caption), seconds=0.8)
    _addition(self, (left, right))

    self.move(FadeOut(caption), seconds=0.6)
    # The next comparison starts blue-first, using the same visible term objects.
    self.move(*left.swap_animations(), *right.swap_animations(),
              seconds=1.8)
    _negate(self, left.blue, right.blue)
    self.pause(1.5)
    simplified = _arrow_label(self, "4", BLUE).move_to(right.blue.label)
    explanation = VGroup(_words("El opuesto de −4 es 4:", 27),
                         _math("-(-4)=4", size=27)).arrange(RIGHT, buff=0.16)
    explanation.move_to(DOWN * 3.5)
    self.move(Transform(right.blue.label, simplified), FadeIn(explanation), seconds=0.8)
    self.pause(2.5)
    comparison = _words("Las sumas tienen resultados opuestos.", 27).move_to(DOWN * 3.5)
    self.move(FadeOut(explanation), FadeIn(comparison), seconds=0.8)
    _addition(self, (left, right), keep_final=True)
    for panel in (left, right):
        panel.blue.label.clear_updaters()
        panel.red.label.clear_updaters()
    # Explicit arithmetic: 7.4 + 3.5 + 3.6 + 2.0 + 0.8 + 22.2 + 0.6
    # + 1.8 + 1.8 + 1.5 + 0.8 + 2.5 + 0.8 + 19.8 = 69.1 seconds.
    # Preserve the final comparison for the remaining 4.9 seconds.
    self.pause(4.9)
    self.finish_beat(start, ADDING_SUBTRACTING_SECONDS)


class AddingSubtracting(TopicScene):
    """The shared signed-addition sequence, independently renderable."""

    video_number = 1
    source_file = __file__
    output_identity = "algebra/stage1_arithmetic_foundations/02_adding_subtracting.mp4"
    section = render_section
    planned_seconds = ADDING_SUBTRACTING_SECONDS
