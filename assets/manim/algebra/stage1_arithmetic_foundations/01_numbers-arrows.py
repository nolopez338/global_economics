"""Numbers as signed arrows; Manim Community 0.17.3.

Standalone render from the repository root:
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/01_numbers-arrows.py NumbersAsArrows

Uses TopicScene's section and explicit clock, without adding this standalone
interlude to the combined lesson. Uses the shared source-based output configuration.
Final MP4 (repository-relative, independent of cwd):
    ../manim_media/videos/algebra/stage1_arithmetic_foundations/01_numbers-arrows.mp4
"""

from pathlib import Path
import sys

import numpy as np

REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import (
    DOWN, UP, WHITE, Arrow, Create, FadeIn, NumberLine, Text,
    ValueTracker, VGroup, VMobject, linear,
)
from assets.manim.algebra.stage1_arithmetic_foundations.common import TopicScene


FONT = "Segoe UI Variable Display"
WEIGHT = "SEMIBOLD"
PLANNED_SECONDS = 34.0
ARROW_OFFSET = 0.18 * UP


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
    """Cached glyphs, fixed baseline and tabular digit advances; no TeX needed."""

    def __init__(self, tenths=10):
        alphabet = "0123456789−."
        source = Text(alphabet, font=FONT, weight=WEIGHT, font_size=108,
                      color=WHITE, disable_ligatures=True)
        # Preserve the font's shared baseline, even when a decimal or sign enters.
        source.shift(UP * (0.9 - source[0].get_y()))
        self.glyphs = dict(zip(alphabet, source))
        self.advance = max(glyph.width for glyph in source[:10]) + 0.035
        self.current_tenths = None
        # Keep the family fixed: Cairo caches the moving family for each play.
        super().__init__(*[VMobject() for _ in range(5)])
        self.show_value(tenths)

    def show_value(self, tenths):
        if tenths == self.current_tenths:
            return
        text = number_string(tenths)
        advances = [self.advance * (0.40 if c == "." else 1) for c in text]
        cursor = -sum(advances) / 2
        glyphs = []
        for char, advance in zip(text, advances):
            glyph = self.glyphs[char].copy()
            glyph.set_x(cursor + advance / 2)
            glyphs.append(glyph)
            cursor += advance
        group = VGroup(*glyphs)
        # Center the visible ink horizontally, without changing its baseline.
        group.shift(-group.get_x() * np.array([1.0, 0.0, 0.0]))
        for index, slot in enumerate(self.submobjects):
            if index < len(group):
                slot.set_points(group[index].points)
                slot.match_style(group[index])
            else:
                slot.clear_points()
        self.current_tenths = tenths


def signed_arrow(axis, tenths):
    """Rebuild signed horizontal geometry; zero has no shaft OR arrowhead."""
    if tenths == 0:
        return VGroup()
    return VGroup(Arrow(
        axis.n2p(0) + ARROW_OFFSET,
        axis.n2p(tenths / 10) + ARROW_OFFSET,
        buff=0, color=WHITE, stroke_width=6, tip_length=0.16,
        max_tip_length_to_length_ratio=0.38,
        max_stroke_width_to_length_ratio=12,
    ))


def update_arrow_geometry(slots, axis, tenths):
    """Stable shaft/tip slots prevent stale geometry in Cairo's moving family."""
    geometry = signed_arrow(axis, tenths)
    if not geometry:
        for slot in slots:
            slot.clear_points()
        return
    shaft = geometry[0]
    for slot, part in zip(slots, (shaft, shaft.tip)):
        slot.set_points(part.points)
        slot.match_style(part)


def render_section(self, *, standalone=False):
    start = self.lesson_seconds
    title = Text("Números como vectores", font=FONT, weight=WEIGHT,
                 font_size=40, color=WHITE).move_to(UP * 3.12)
    tracker = ValueTracker(1)
    number = CenteredNumber()
    axis = NumberLine(
        x_range=[-11, 11, 1], length=12.1, include_numbers=False,
        include_tip=False, tick_size=0.055,
        color=WHITE, stroke_width=1.4,
    ).move_to(DOWN * 1.65).set_opacity(0.42)
    ticks = VGroup(*[
        Text(str(value).replace("-", "−"), font=FONT, weight=WEIGHT,
             font_size=22, color=WHITE).move_to(axis.n2p(value) + DOWN * 0.42)
        for value in (-10, -5, 0, 5, 10)
    ]).set_opacity(0.75)
    arrow = VGroup(VMobject(), VMobject())

    # A single updater computes the displayed value once per frame. The arrow
    # consumes that exact integer count of tenths, never the unrounded tracker.
    def synchronize(_number, dt=0):
        tenths = displayed_tenths(tracker.get_value())
        _number.show_value(tenths)

    def synchronize_arrow(_arrow, dt=0):
        tenths = number.current_tenths
        if tenths != _arrow.current_tenths:
            update_arrow_geometry(_arrow, axis, tenths)
            _arrow.current_tenths = tenths

    self.move(FadeIn(title), seconds=0.8)
    self.move(FadeIn(number), seconds=0.6)
    self.pause(0.8)
    number.add_updater(synchronize)

    def sweep():
        for target, duration in ((-10, 3.3), (10, 6.0), (1, 2.7)):
            self.move(tracker.animate(rate_func=linear).set_value(target),
                      seconds=duration)
            # Resolve the exact target before its reading pause.
            synchronize(number)
            self.pause(0.6)

    sweep()
    self.move(Create(axis), FadeIn(ticks), seconds=0.8)
    update_arrow_geometry(arrow, axis, 10)
    self.move(FadeIn(arrow), seconds=0.6)
    arrow.current_tenths = 10
    arrow.add_updater(synchronize_arrow)
    self.pause(0.8)
    sweep()
    number.clear_updaters()
    arrow.clear_updaters()
    self.finish_beat(start, PLANNED_SECONDS)


class NumbersAsArrows(TopicScene):
    """Independent interlude using the shared section/clock conventions."""

    source_file = __file__
    output_identity = "algebra/stage1_arithmetic_foundations/01_numbers-arrows.mp4"
    section = render_section
    planned_seconds = PLANNED_SECONDS
