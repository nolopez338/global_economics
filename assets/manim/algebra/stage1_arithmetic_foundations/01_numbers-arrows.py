"""Numbers as signed arrows; Manim Community 0.17.3.

Standalone render from the repository root:
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/01_numbers-arrows.py NumbersAsArrows

Uses TopicScene's section and explicit clock, without adding this standalone
interlude to the combined lesson. Uses the shared stable output identity.
CMU Serif Roman is discovered through kpsewhich and registered only while shaping
text; a missing dependency is reported explicitly rather than silently substituted.
Final MP4 (repository-relative, independent of cwd):
    ../manim_media/videos/algebra/stage1_arithmetic_foundations/01_numbers-arrows.mp4
"""

from bisect import bisect_right
from pathlib import Path
import shutil
import subprocess
import sys

import manimpango

REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import (
    DOWN, NORMAL, UP, WHITE, Create, FadeIn, FadeOut, LineJointType, NumberLine,
    Text, UpdateFromAlphaFunc, ValueTracker, VGroup, VMobject, bezier, linear,
    register_font, smooth,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import TopicScene


FONT = "CMU Serif"
# Local, requested symbol emphasis: 1.2 at 108, about 0.244 at 22.
SYMBOL_STROKE_AT_108 = 1.2
MINUS_WIDTH_FACTOR = 0.75
# Original 34 s, fade 0.6 s, reposition 1.4 s, repeat 13.8 s, final hold 1.2 s.
PLANNED_SECONDS = 51.0
ARROW_OFFSET = 0.18 * UP
# Narrow open heads, coordinated with this scene's axis spacing.
ARROW_STROKE_WIDTH = 5
ARROW_TIP_LENGTH = 0.34
ARROW_TIP_WIDTH = 0.14
ARROW_FULL_SIZE_LENGTH = 0.55
ARROW_MAX_TIP_RATIO = 0.48


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
                    disable_ligatures=True, font_size=font_size, color=WHITE)


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


def displayed_tenths(value):
    """One quantization feeds BOTH the glyphs and the arrow, including zero."""
    return int(round(10 * value))


def number_string(tenths):
    magnitude = abs(tenths)
    integer, decimal = divmod(magnitude, 10)
    return ("−" if tenths < 0 else "") + str(integer) + (
        f".{decimal}" if decimal else ""
    )


class CenteredNumber(VGroup):
    """Compact equation: fixed a and equals, translating semantic number slots."""

    def __init__(self, tenths=10):
        alphabet = "0123456789−.a="
        source = cmu_text(alphabet, font_size=108)
        # One shaped run supplies all baseline offsets, including punctuation.
        source.shift(UP * (0.9 - source[0].get_y()))
        self.glyphs = dict(zip(alphabet, source))
        shorten_minus(self.glyphs["−"])
        for char in "−=":
            emphasize_symbol(self.glyphs[char], font_size=108)
        for glyph in self.glyphs.values():
            glyph.set_x(0)
        self.digit_width = max(self.glyphs[c].width for c in "0123456789")
        self.digit_gap = 0.035
        self.sign_gap = 0.12
        self.equation_gap = 0.24
        # Cairo CE 0.17.3 uses a 0.01 stroke-width factor; bounds omit strokes.
        self.symbol_edge = 0.5 * 0.01 * SYMBOL_STROKE_AT_108
        self.equals = self.glyphs["="].copy()  # Anchored at x=0 for the section.
        self.variable = self.glyphs["a"].copy()
        self.variable.set_x(self.equals.get_left()[0] - self.symbol_edge
                            - self.equation_gap - self.variable.width / 2)
        self.numeric_left = (self.equals.get_right()[0] + self.symbol_edge
                             + self.equation_gap)
        columns = ("sign", "tens", "units", "decimal", "tenths")
        numeric_slots = [VMobject() for _ in columns]
        super().__init__(self.variable, self.equals, *numeric_slots)
        self.column_slots = dict(zip(columns, numeric_slots))
        self.visual_key = None
        self.transitions = {}
        self.current_tenths = tenths  # Authoritative quantized state for geometry.
        self.show_exact(tenths)

    def layout(self, tenths):
        integer, separator, fraction = number_string(abs(tenths)).partition(".")
        if len(integer) > 2:
            raise ValueError("CenteredNumber reserves at most two integer digits")
        characters = {
            "sign": "−" if tenths < 0 else None,
            "tens": integer[-2] if len(integer) == 2 else None,
            "units": integer[-1],
            "decimal": separator or None,
            "tenths": fraction or None,
        }
        advance = self.digit_width + self.digit_gap
        local = {"tens": -advance, "units": 0,
                 "decimal": (self.digit_width + self.glyphs["."].width) / 2
                            + self.digit_gap}
        local["tenths"] = 2 * local["decimal"]
        first_column = "tens" if characters["tens"] else "units"
        first_left = (local[first_column]
                      - self.glyphs[characters[first_column]].width / 2)
        sign_width = self.glyphs["−"].width
        # Reclaim unused sign/integer width by translating the internal grid.
        integer_left = self.numeric_left
        if characters["sign"]:
            integer_left += sign_width + 2 * self.symbol_edge + self.sign_gap
        offset = integer_left - first_left
        centers = {column: x + offset for column, x in local.items()}
        centers["sign"] = self.numeric_left + self.symbol_edge + sign_width / 2
        # Empty leading slots collapse at the first ink edge. Entry/removal
        # grows/shrinks with the space the digit grid is opening/reclaiming.
        if characters["sign"] is None:
            centers["sign"] = self.numeric_left
        if characters["tens"] is None:
            centers["tens"] = integer_left
        return characters, centers

    def show_exact(self, tenths):
        """Restore cache outlines/styles, discarding alignment-only contours."""
        key = (tenths, tenths)
        if self.visual_key == key:
            return
        characters, centers = self.layout(tenths)
        for column, slot in self.column_slots.items():
            char = characters[column]
            if char is None:
                slot.clear_points()
            else:
                glyph = self.glyphs[char]
                slot.set_points(glyph.points.copy())
                slot.match_style(glyph)
                slot.shift([centers[column], 0, 0])
        self.transitions.clear()
        self.visual_key = key

    def show_interval(self, reached, following, phase):
        """70% exact hold, then one coordinated shape/layout interpolation."""
        if phase <= 0.7:
            self.show_exact(reached)
            return
        if phase >= 1:
            self.show_exact(following)
            return
        key = (reached, following)
        if self.visual_key != key:
            old_chars, old_centers = self.layout(reached)
            new_chars, new_centers = self.layout(following)
            self.transitions.clear()
            for column in self.column_slots:
                old, new = old_chars[column], new_chars[column]
                if old is None and new is None:
                    self.column_slots[column].clear_points()
                    continue
                start = self.glyphs[old or new].copy()
                target = self.glyphs[new or old].copy()
                # Only genuine entry/removal collapses and fades. Ordinary
                # replacements remain opaque single outlines in existing slots.
                for glyph, char in ((start, old), (target, new)):
                    if char is None:
                        points = glyph.points.copy()
                        points[:, 0] = 0
                        glyph.set_points(points)
                        glyph.set_opacity(0)
                        # Stroke-expanded bounds shrink with the outline too,
                        # preserving clearance even at the start of sign entry.
                        glyph.set_stroke(width=0)
                if old != new:
                    # Bypass CE's equal-total-point contour-alignment shortcut
                    # on working copies only, never on the original cache.
                    if start.get_num_points() == target.get_num_points():
                        start.add_line_to(start.get_last_point())
                    start.align_points(target)
                self.transitions[column] = (
                    start, target, old_centers[column], new_centers[column],
                    old != new,
                )
            self.visual_key = key
        alpha = (phase - 0.7) / 0.3
        alpha = alpha * alpha * (3 - 2 * alpha)  # Zero-speed boundaries.
        for column, (start, target, x0, x1, changed) in self.transitions.items():
            slot = self.column_slots[column]
            if changed:
                slot.interpolate(start, target, alpha)
            else:
                # Unchanged shapes are never aligned or morphed.
                slot.set_points(start.points.copy())
                slot.match_style(start)
            slot.shift([x0 + alpha * (x1 - x0), 0, 0])


class SweepTimeline:
    """Deterministic quantization boundaries, independent of frame cadence."""

    def __init__(self, start, target, duration):
        self.start = start
        self.duration = duration
        self.seconds_per_unit = duration / abs(target - start)
        first, last = displayed_tenths(start), displayed_tenths(target)
        direction = 1 if last > first else -1
        self.targets = list(range(first, last + direction, direction))
        # Half-even ties belong to the even neighbor. Geometry still calls the
        # original round rule; visuals complete at each half-tenth crossing.
        self.boundaries = [0.0] + [
            abs((previous + following) / 20 - start) * self.seconds_per_unit
            for previous, following in zip(self.targets, self.targets[1:])
        ]

    def show(self, number, value):
        elapsed = min(self.duration, abs(value - self.start) * self.seconds_per_unit)
        index = min(len(self.targets) - 1,
                    bisect_right(self.boundaries, elapsed) - 1)
        if index == len(self.targets) - 1:
            # Final half interval and reading pause have no successor.
            number.show_exact(self.targets[-1])
        else:
            begin, end = self.boundaries[index:index + 2]
            number.show_interval(self.targets[index], self.targets[index + 1],
                                 (elapsed - begin) / (end - begin))


def update_arrow_geometry(slots, axis, tenths):
    """Update stable slots; each nonzero open head has two mirrored cubics."""
    shaft, head = slots
    if tenths == 0:
        shaft.clear_points()
        head.clear_points()
        return
    start = axis.n2p(0) + ARROW_OFFSET
    end = axis.n2p(tenths / 10) + ARROW_OFFSET
    length = abs(end[0] - start[0])
    direction = (end - start) / length
    transverse = direction[0] * UP
    # Smoothly approach nominal size while staying below 48% of the interval.
    # Both head dimensions scale together, without a minimum represented length.
    head_scale = length / (
        length ** 4 + (ARROW_TIP_LENGTH / ARROW_MAX_TIP_RATIO) ** 4
    ) ** 0.25
    head_length = ARROW_TIP_LENGTH * head_scale
    head_width = ARROW_TIP_WIDTH * head_scale
    proportion = min(1.0, length / ARROW_FULL_SIZE_LENGTH)

    def local(x, y):
        # Tip at (0, 0), rear at x=-1; rotate the whole convention by sign.
        return end + x * head_length * direction + y * head_width * transverse

    # Both centerline endpoints are exact; no shaft extends beyond the tip.
    # Scale the common stroke with short arrows rather than inventing length.
    stroke_width = ARROW_STROKE_WIDTH * proportion
    shaft.set_points_as_corners([start, end])
    shaft.set_fill(WHITE, opacity=0)
    shaft.set_stroke(WHITE, width=stroke_width, opacity=1)

    # Upper rear -> tip -> lower rear is ONE open stroked path, not a fill.
    # At x=-0.72/-0.28 the upper chord has y=0.36/0.14; handles at
    # y=0.20/0.12 lie strictly inward. The lower branch is its exact
    # reflection, with reversed traversal. Affine orientation preserves this
    # concavity and symmetry for either sign and every nonzero magnitude.
    head.clear_points()
    head.start_new_path(local(-1, 0.50))
    head.add_cubic_bezier_curve_to(
        local(-0.72, 0.20), local(-0.28, 0.12), end,
    )
    head.add_cubic_bezier_curve_to(
        local(-0.28, -0.12), local(-0.72, -0.20), local(-1, -0.50),
    )
    # CE 0.17.3 Cairo honors joint_type, but has no VMobject cap API and
    # never calls set_line_cap: exposed ends retain Cairo's butt caps.
    # MITER keeps the shared forward vertex sharp (not rounded/beveled).
    # As with any stroked miter, ink extends beyond the centerline vertex;
    # the mathematical tip anchor itself remains exactly at end.
    head.joint_type = LineJointType.MITER
    head.set_fill(WHITE, opacity=0)
    head.set_stroke(WHITE, width=stroke_width, opacity=1)


def render_section(self, *, standalone=False):
    start = self.lesson_seconds
    title = cmu_text("Números como vectores", font_size=40).move_to(UP * 3.12)
    tracker = ValueTracker(1)
    number = CenteredNumber()
    axis = NumberLine(
        x_range=[-5, 5, 1], length=12.1, include_numbers=False,
        include_tip=False, tick_size=0.055,
        color=WHITE, stroke_width=1.4,
    ).move_to(DOWN * 1.65).set_opacity(0.42)
    ticks = VGroup(*[
        axis_label(value, position=axis.n2p(value) + DOWN * 0.42)
        for value in (-5, 0, 5)
    ]).set_opacity(0.75)
    arrow = VGroup(VMobject(), VMobject())
    # Active only during motion; pauses never preview the following sweep.
    sweep_timing = {"timeline": None, "show_numbers": True}

    def synchronize(_number, dt=0):
        value = tracker.get_value()
        # Quantize once for geometry; the visual transition is not another
        # mathematical value and does not advance the arrow toward the future.
        _number.current_tenths = displayed_tenths(value)
        if not sweep_timing["show_numbers"]:
            return
        timeline = sweep_timing["timeline"]
        if timeline is None:
            _number.show_exact(_number.current_tenths)
        else:
            timeline.show(_number, value)

    def synchronize_arrow(_arrow, dt=0):
        tenths = number.current_tenths
        # Axis motion must invalidate geometry even while the value is held.
        geometry_key = (tenths, tuple(axis.n2p(0)), tuple(axis.n2p(1)))
        if geometry_key != getattr(_arrow, "geometry_key", None):
            update_arrow_geometry(_arrow, axis, tenths)
            _arrow.current_tenths = tenths
            _arrow.geometry_key = geometry_key

    self.move(FadeIn(title), seconds=0.8)
    # Reveal a = 1 together in the existing entrance, before either sweep.
    self.move(FadeIn(number), seconds=0.6)
    self.pause(0.8)
    number.add_updater(synchronize)

    def sweep():
        for target, duration in ((4, 3.3), (-4, 6.0), (1, 2.7)):
            sweep_timing["timeline"] = SweepTimeline(
                tracker.get_value(), target, duration,
            )
            self.move(tracker.animate(rate_func=linear).set_value(target),
                      seconds=duration)
            # Resolve the exact target before its reading pause.
            sweep_timing["timeline"] = None
            synchronize(number)
            if arrow.updaters:
                synchronize_arrow(arrow)
            self.pause(0.6)

    sweep()
    self.move(Create(axis), FadeIn(ticks), seconds=0.8)
    update_arrow_geometry(arrow, axis, 10)
    self.move(FadeIn(arrow), seconds=0.6)
    arrow.current_tenths = 10
    arrow.add_updater(synchronize_arrow)
    self.pause(0.8)
    sweep()
    synchronize(number)
    synchronize_arrow(arrow)
    self.pause(2.0)  # Preserve the original final a = 1 hold through 34 s.

    # Keep the existing variable and authoritative state updater; suppress all
    # numeric morphs before fading so later sweeps cannot restore hidden ink.
    sweep_timing["show_numbers"] = False

    def fade_equation(_number, alpha):
        _number.equals.set_opacity(1 - alpha)
        for slot in _number.column_slots.values():
            slot.set_opacity(1 - alpha)

    self.move(UpdateFromAlphaFunc(number, fade_equation), FadeOut(ticks),
              seconds=0.6)

    variable = number.variable
    initial_variable = variable.copy()
    label_scale = 48 / 108
    label_gap = 0.22
    axis_start = axis.get_center().copy()
    axis_end = axis_start.copy()
    axis_end[1] = 0
    axis_delta = axis_end - axis_start
    axis_path = bezier([
        axis_start, axis_start + axis_delta / 3,
        axis_end - axis_delta / 3, axis_end,
    ])

    def label_position():
        # Mathematical endpoints, never the head's bounds or a normalized
        # direction: well-defined at zero and symmetric for negative arrows.
        midpoint = (axis.n2p(0) + axis.n2p(number.current_tenths / 10)) / 2
        return midpoint + ARROW_OFFSET + UP * (label_gap + variable.height / 2)

    label_start = variable.get_center().copy()
    label_end = label_position() + axis_delta
    label_end += UP * (initial_variable.height * (label_scale - 1) / 2)
    label_delta = label_end - label_start
    label_path = bezier([
        label_start, label_start + label_delta / 3 + UP * 0.25,
        label_end - label_delta / 3 + UP * 0.25, label_end,
    ])

    def reposition_axis(_axis, alpha):
        _axis.move_to(axis_path(alpha))
        synchronize_arrow(arrow)

    def reposition_variable(_variable, alpha):
        # Rebuild from the original upright outline to avoid cumulative scale
        # error; easing is applied once by UpdateFromAlphaFunc.
        _variable.set_points(initial_variable.points.copy())
        _variable.scale(1 + alpha * (label_scale - 1))
        _variable.move_to(label_path(alpha))

    self.move(
        UpdateFromAlphaFunc(axis, reposition_axis, rate_func=smooth),
        UpdateFromAlphaFunc(variable, reposition_variable, rate_func=smooth),
        seconds=1.4,
    )

    def follow_arrow(_variable, dt=0):
        _variable.move_to(label_position())

    variable.add_updater(follow_arrow)
    follow_arrow(variable)
    sweep()
    synchronize(number)
    synchronize_arrow(arrow)
    follow_arrow(variable)
    self.pause(1.2)
    variable.clear_updaters()
    number.clear_updaters()
    arrow.clear_updaters()
    self.finish_beat(start, PLANNED_SECONDS)


class NumbersAsArrows(TopicScene):
    """Independent interlude using the shared section/clock conventions."""

    source_file = __file__
    output_identity = "algebra/stage1_arithmetic_foundations/01_numbers-arrows.mp4"
    section = render_section
    planned_seconds = PLANNED_SECONDS
