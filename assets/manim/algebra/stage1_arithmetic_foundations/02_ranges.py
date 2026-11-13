"""Ranges, continuing the exact final composition of 01_numbers-arrows.py.

From Windows CMD at the repository root:
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/02_ranges.py Ranges

Manim CE 0.17.3; standalone or render_section reuse, no combined-lesson entry.
Stable destination: ../manim_media/videos/algebra/stage1_arithmetic_foundations/02_ranges.mp4
Source inspection only: authoring does not authorize rendering or tests.
"""

from pathlib import Path
import shutil
import subprocess
import sys

import manimpango

REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import (
    NORMAL, UP, WHITE, FadeIn, LineJointType, NumberLine, Text, Transform,
    UpdateFromAlphaFunc, ValueTracker, VGroup, VMobject, bezier, linear, smooth,
    interpolate_color, register_font,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    BLUE, GOLD, TopicScene,
)


FONT = "CMU Serif"
ARROW_OFFSET = 0.18 * UP
ARROW_STROKE_WIDTH = 5
ARROW_TIP_LENGTH = 0.34
ARROW_TIP_WIDTH = 0.14
ARROW_FULL_SIZE_LENGTH = 0.55
ARROW_MAX_TIP_RATIO = 0.48
VALUE_SCALE = 10000
STRICT_CLEARANCE = 0.04
LABEL_GAP = 0.22
# Opening 2.2; three lower-bound cases 3*10.2; four changes 4*2.6;
# closed interval 10.8; upper-bound case 8.0; final reading hold 2.0.
PLANNED_SECONDS = 64.0


def cmu_text(message, *, font_size):
    """Same scoped Roman font discovery and shaping as the preceding scene."""
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
                    disable_ligatures=True, font_size=font_size, color=WHITE)


def update_arrow_geometry(slots, axis, units):
    """Preceding scene's stable geometry, with only the value divisor adapted.

    Cairo's butt rear caps and miter ink overshoot are retained; the mathematical
    tip is exact. No minimum length, substituted arrow, or endpoint decoration.
    """
    shaft, head = slots
    if units == 0:
        shaft.clear_points()
        head.clear_points()
        return
    start = axis.n2p(0) + ARROW_OFFSET
    end = axis.n2p(units / VALUE_SCALE) + ARROW_OFFSET
    length = abs(end[0] - start[0])
    direction = (end - start) / length
    transverse = direction[0] * UP
    head_scale = length / (
        length ** 4 + (ARROW_TIP_LENGTH / ARROW_MAX_TIP_RATIO) ** 4
    ) ** 0.25
    head_length = ARROW_TIP_LENGTH * head_scale
    head_width = ARROW_TIP_WIDTH * head_scale
    proportion = min(1.0, length / ARROW_FULL_SIZE_LENGTH)

    def local(x, y):
        return end + x * head_length * direction + y * head_width * transverse

    stroke_width = ARROW_STROKE_WIDTH * proportion
    shaft.set_points_as_corners([start, end])
    shaft.set_fill(WHITE, opacity=0)
    shaft.set_stroke(WHITE, width=stroke_width, opacity=1)
    head.clear_points()
    head.start_new_path(local(-1, 0.50))
    head.add_cubic_bezier_curve_to(
        local(-0.72, 0.20), local(-0.28, 0.12), end,
    )
    head.add_cubic_bezier_curve_to(
        local(-0.28, -0.12), local(-0.72, -0.20), local(-1, -0.50),
    )
    head.joint_type = LineJointType.MITER
    head.set_fill(WHITE, opacity=0)
    head.set_stroke(WHITE, width=stroke_width, opacity=1)


def cubic_path(start, end, alpha):
    """Explicit collinear cubic, also valid for arrays of morphing points."""
    delta = end - start
    return bezier([start, start + delta / 3, end - delta / 3, end])(alpha)


SLOTS = ("operator", "left_bracket", "lower", "comma", "upper", "right_bracket")


def inequality(kind):
    """Full-run baseline shaping, then permanent semantic slots for highlights.

    Text excludes whitespace from its glyph indexing in CE. All rows share the
    identical upright a anchor; only the six tail slots participate in morphs.
    """
    message, indices = {
        "positive": ("a > 0", {"operator": [1], "lower": [2]}),
        "above_one": ("a > 1", {"operator": [1], "lower": [2]}),
        "above_half": ("a > 1.5", {"operator": [1], "lower": [2, 3, 4]}),
        "closed": ("a ∈ [2,3]", {"operator": [1], "left_bracket": [2],
                               "lower": [3], "comma": [4], "upper": [5],
                               "right_bracket": [6]}),
        "below_three": ("a < 3", {"operator": [1], "upper": [2]}),
    }[kind]
    run = cmu_text(message, font_size=80)
    run.shift([-1.7 - run[0].get_x(), 0.9 - run[0].get_y(), 0])
    parts = [run[0].copy()]
    for name in SLOTS:
        slot = VMobject().set_fill(WHITE, opacity=1).set_stroke(width=0)
        for index in indices.get(name, []):
            slot.append_points(run[index].points.copy())
        if not slot.has_points():
            # A real zero-area contour permits continuous entry/removal without
            # introducing submobjects or changing semantic slot identity.
            point = run[1].get_right()
            slot.set_points_as_corners([point, point]).set_opacity(0)
        parts.append(slot)
    return VGroup(*parts).set_z_index(4)


def support(axis, lower=None, upper=None, *, included=False):
    """Fill-only rectangle: clipped ends have NO visible vertical edge.

    Six separate cubic line segments per finite edge: dashed for exclusion,
    contiguous for inclusion. Equal topology makes boundary morphs stable.
    """
    left = axis.n2p(-5 if lower is None else lower)
    right = axis.n2p(5 if upper is None else upper)
    half_height = 0.36
    bottom_left, top_left = left - half_height * UP, left + half_height * UP
    bottom_right, top_right = right - half_height * UP, right + half_height * UP
    fill = VMobject().set_points_as_corners([
        bottom_left, bottom_right, top_right, top_left, bottom_left,
    ]).set_fill(BLUE, opacity=0.11).set_stroke(width=0)

    def edge(point, finite):
        path = VMobject()
        for index in range(6):
            a = index / 6
            b = (index + (1 if included else 0.58)) / 6
            start = point + UP * (-half_height + 2 * half_height * a)
            end = point + UP * (-half_height + 2 * half_height * b)
            path.start_new_path(start)
            path.add_cubic_bezier_curve_to(
                start + (end - start) / 3, end - (end - start) / 3, end,
            )
        return path.set_fill(opacity=0).set_stroke(
            BLUE, width=1.8, opacity=0.7 if finite else 0,
        )

    return VGroup(fill, edge(left, lower is not None),
                  edge(right, upper is not None)).set_z_index(-2)


def render_section(self, *, standalone=False):
    start = self.lesson_seconds
    # No topic(), entrance animation, readout, equals, or axis number labels.
    title = cmu_text("Números como vectores", font_size=40).move_to(UP * 3.12)
    axis = NumberLine(
        x_range=[-5, 5, 1], length=12.1, include_numbers=False,
        include_tip=False, tick_size=0.055, color=WHITE, stroke_width=1.4,
    ).move_to(UP * 0).set_opacity(0.42)
    # Recreate the actual existing a outline: same alphabet, size, then 48/108.
    alphabet = cmu_text("0123456789−.a=", font_size=108)
    label = alphabet[-2].copy().scale(48 / 108).set_z_index(3)
    arrow = VGroup(VMobject(), VMobject()).set_z_index(2)
    tracker = ValueTracker(1)
    state = {"units": VALUE_SCALE}

    def synchronize(_driver=None, dt=0):
        # ONE half-even quantization for shaft, head and mathematical midpoint.
        # 0.0001 resolution cannot round a 0.04 clearance onto an excluded end.
        state["units"] = int(round(VALUE_SCALE * tracker.get_value()))
        value = state["units"] / VALUE_SCALE
        update_arrow_geometry(arrow, axis, state["units"])
        midpoint = (axis.n2p(0) + axis.n2p(value)) / 2
        label.move_to(midpoint + ARROW_OFFSET + UP * (LABEL_GAP + label.height / 2))

    # One ordered driver updates all dependents, including unchanged values
    # while the axis moves. Call explicitly at animation boundaries as well.
    driver = VMobject()
    driver.add_updater(synchronize)
    synchronize()
    self.add(title, axis, arrow, label, driver)
    self.pause(0.8)

    row = inequality("positive")
    band = support(axis, lower=0).set_opacity(0)
    self.add(band)
    axis_begin = axis.get_center().copy()
    axis_end = axis_begin.copy()
    axis_end[1] = -1.65

    def lower_axis(_axis, alpha):
        _axis.move_to(cubic_path(axis_begin, axis_end, alpha))
        # The emerging band rides the very same axis trajectory. Never reveal
        # a detached support or an apparent barrier at the clipped right edge.
        band.become(support(_axis, lower=0))
        band[0].set_fill(opacity=0.11 * alpha)
        band[1].set_stroke(opacity=0.7 * alpha)
        synchronize()

    self.move(UpdateFromAlphaFunc(axis, lower_axis, rate_func=smooth),
              FadeIn(row), seconds=1.4)
    axis.move_to(axis_end)
    band.become(support(axis, lower=0))
    synchronize()

    def value_to(target, seconds, *, pulse=None):
        initial = tracker.get_value()

        def travel(_tracker, alpha):
            # A scalar cubic drives a mathematical endpoint on the line;
            # it never displaces, bends or rotates the represented arrow.
            _tracker.set_value(cubic_path(initial, target, alpha))
            synchronize()

        animations = [UpdateFromAlphaFunc(tracker, travel, rate_func=smooth)]
        if pulse is not None:
            names, side, rising = pulse

            def highlight(_band, alpha):
                strength = alpha if rising else 1 - alpha
                # interpolate_color avoids opacity/shape changes in glyphs.
                for name in names:
                    row[1 + SLOTS.index(name)].set_color(
                        interpolate_color(WHITE, GOLD, strength),
                    )
                band[side].set_stroke(
                    interpolate_color(BLUE, GOLD, strength),
                    width=1.8 + 1.4 * strength, opacity=0.7 + 0.3 * strength,
                )

            animations.append(UpdateFromAlphaFunc(band, highlight, rate_func=linear))
        self.move(*animations, seconds=seconds)
        tracker.set_value(target)
        synchronize()
        if pulse is not None:
            highlight(band, 1)

    def bump(boundary, direction, names, side, *, included=False):
        # Broad approach, compressed near-contact beat, then slower recoil.
        # The monotone cubics stay in the convex hull of permitted values.
        contact = boundary if included else boundary + direction * STRICT_CLEARANCE
        value_to(boundary + direction * 0.16, 0.55)
        value_to(contact, 0.18, pulse=(names, side, True))
        value_to(boundary + direction * 0.55, 0.42,
                 pulse=(names, side, False))
        self.pause(0.25)

    def lower_case(boundary, peak, resting):
        value_to(peak, 1.8)
        self.pause(0.6)
        value_to(boundary + 0.55, 1.8)
        self.pause(0.2)
        for _ in range(3):
            bump(boundary, 1, ("operator", "lower"), 1)
        value_to(resting, 0.8)
        self.pause(0.8)

    def change(kind, value, *, lower=None, upper=None, included=False):
        # Move first under the OLD inequality; all four preparatory targets
        # satisfy both old and new restrictions (3 belongs to the closed case).
        value_to(value, 1.0)
        self.pause(0.3)
        target_row = inequality(kind)
        target_band = support(axis, lower, upper, included=included)
        animations = []
        for current, target in zip(row[1:], target_row[1:]):
            if (current.points.shape == target.points.shape
                    and (current.points == target.points).all()):
                continue  # Keep unchanged glyph outlines untouched.
            # Force contour alignment on copies when equal point counts could
            # otherwise bypass CE 0.17.3's contour compatibility check.
            target = target.copy()
            if current.get_num_points() == target.get_num_points():
                target.add_line_to(target.get_last_point())
            animations.append(Transform(current, target, path_func=cubic_path,
                                        rate_func=smooth))
        animations.append(Transform(band, target_band, path_func=cubic_path,
                                    rate_func=smooth))
        self.move(*animations, seconds=0.9)
        # Restore original contours and exact resting styles before reading.
        for current, target in zip(row[1:], target_row[1:]):
            current.become(target)
        band.become(target_band)
        synchronize()
        self.pause(0.4)

    lower_case(0, 3.6, 1)
    change("above_one", 2, lower=1)
    lower_case(1, 3.8, 2)
    change("above_half", 2, lower=1.5)
    lower_case(1.5, 3.9, 2)
    change("closed", 3, lower=2, upper=3, included=True)

    # Four excursions, alternating exact included endpoints. Only that end's
    # digit/bracket and actual vertical support edge pulse, never ∈ or comma.
    self.pause(0.6)
    for boundary, direction, names, side in (
        (2, 1, ("left_bracket", "lower"), 1),
        (3, -1, ("upper", "right_bracket"), 2),
        (2, 1, ("left_bracket", "lower"), 1),
        (3, -1, ("upper", "right_bracket"), 2),
    ):
        value_to(boundary + direction * 0.30, 1.1)
        bump(boundary, direction, names, side, included=True)
    self.pause(0.2)

    change("below_three", 2, upper=3)
    value_to(2.45, 1.6)
    self.pause(0.4)
    for _ in range(3):
        bump(3, -1, ("operator", "upper"), 2)
    value_to(2, 1.0)
    self.pause(0.8)

    # All targets and resting styles have been resolved explicitly. No owned
    # updater survives the section, whether standalone or called by a scene.
    synchronize()
    for owned in (driver, tracker, title, axis, arrow, label, row, band):
        owned.clear_updaters()
    self.remove(driver)
    self.pause(2.0)
    self.finish_beat(start, PLANNED_SECONDS)


class Ranges(TopicScene):
    source_file = __file__
    output_identity = "algebra/stage1_arithmetic_foundations/02_ranges.mp4"
    section = render_section
    planned_seconds = PLANNED_SECONDS
