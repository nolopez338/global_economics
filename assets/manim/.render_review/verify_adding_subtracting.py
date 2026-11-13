"""Geometry and shared-section review; run from the repository root."""
from importlib import import_module
from pathlib import Path
import json
import sys

import numpy as np
from manim import Arrow, Create, UpdateFromAlphaFunc, VGroup, config

sys.path.insert(0, str(Path.cwd()))
m = import_module('assets.manim.algebra.stage1_arithmetic_foundations.01_adding_subtracting')
common = import_module('assets.manim.algebra.stage1_arithmetic_foundations.common')
config.media_dir = str(Path('assets/manim/.render_review/adding_subtracting').resolve())
config.quality = 'low_quality'
config.dry_run = True
panels = []
original_init = m.EquationHeading.__init__


def remember(self, scene, panel):
    original_init(self, scene, panel)
    panels.append(panel)


m.EquationHeading.__init__ = remember


class GeometryReview(m.AddingSubtracting):
    def setup(self):
        super().setup()
        self.constructions = []
        self.swaps = 0
        self.resultants = None

    def move(self, *animations, seconds=0.65):
        swaps = [a for a in animations if isinstance(a, UpdateFromAlphaFunc)]
        for animation in swaps:
            term = animation.mobject
            original = term.get_center().copy()
            points = term.get_all_points() - original
            panel = min(panels, key=lambda p: abs(p.center_x - original[0]))
            heading = panel.heading
            plus_center = heading.plus.get_center().copy()
            for alpha in np.linspace(0, 1, 21):
                animation.update_function(term, alpha)
                np.testing.assert_allclose(term.get_all_points() - term.get_center(), points, atol=1e-7)
                np.testing.assert_allclose(np.linalg.norm(term.get_center() - heading.pivot), heading.radius)
                np.testing.assert_allclose(heading.plus.get_center(), plus_center)
                assert panel.center_x - 3 < term.get_left()[0] < term.get_right()[0] < panel.center_x + 3
                assert term.get_top()[1] < 2.65
                # Bounding boxes may intersect on a diagonal, but their glyphs
                # stay outside the plus's circumscribed circle at every sample.
                assert np.linalg.norm(term.get_center() - plus_center) > term.height / 2 + heading.plus.height / 2
            term.move_to(original)
            self.swaps += 1

        greens = [a.mobject for a in animations if isinstance(a, Create)
                  and isinstance(a.mobject, Arrow)
                  and a.mobject.get_color().get_hex_l().lower() == m.GREEN.lower()]
        if greens:
            construction = []
            for panel, arrow in zip(panels, greens):
                first, second = ((panel.blue, panel.red) if panel.heading.blue_first
                                 else (panel.red, panel.blue))
                np.testing.assert_allclose(first.arrow.get_end(), second.arrow.get_start(), atol=1e-7)
                np.testing.assert_allclose(arrow.get_start(), first.arrow.get_start(), atol=1e-7)
                np.testing.assert_allclose(arrow.get_end(), second.arrow.get_end(), atol=1e-7)
                total = first.value + second.value
                assert np.sign(arrow.get_end()[0] - arrow.get_start()[0]) == np.sign(total)
                assert arrow.z_index < min(first.arrow.z_index, second.arrow.z_index)
                construction.append([first.value, second.value, total])
            self.constructions.append({'seconds': round(self.lesson_seconds, 2), 'panels': construction})
            self.resultants = [(a, a.get_start().copy(), a.get_end().copy()) for a in greens]

        previous = self.resultants if not greens and seconds == 1.2 else None
        moving_labels = []
        if previous:
            for animation in animations:
                group = animation.mobject
                if isinstance(group, VGroup) and isinstance(group[0], Arrow):
                    moving_labels.append((group[1], group[1].get_center().copy(),
                                          -1.25 - group[0].get_start()[1]))
        super().move(*animations, seconds=seconds)
        if previous:
            for arrow, start, end in previous:
                np.testing.assert_allclose(arrow.get_start()[0], start[0], atol=1e-7)
                np.testing.assert_allclose(arrow.get_end()[0], end[0], atol=1e-7)
                np.testing.assert_allclose(arrow.get_vector(), end - start, atol=1e-7)
                np.testing.assert_allclose(arrow.get_start()[1], -1.25, atol=1e-7)
                assert arrow.get_start()[1] < start[1]
            for label, center, delta_y in moving_labels:
                np.testing.assert_allclose(label.get_center(), center + [0, delta_y, 0], atol=1e-7)
            self.resultants = None


scene = GeometryReview(skip_animations=True)
scene.render()
expected = [[[4, 3, 7], [-4, -3, -7]], [[3, 4, 7], [-3, -4, -7]],
            [[-4, 3, -1], [4, -3, 1]], [[3, -4, -1], [-3, 4, 1]]]
assert [item['panels'] for item in scene.constructions] == expected
assert scene.swaps == 12
scene.check_duration(common.ADDING_SUBTRACTING_SECONDS)
combined = import_module('assets.manim.algebra.stage1_arithmetic_foundations.00_preliminaries')
assert combined.adding_subtracting is m.render_section
assert combined.PLANNED_SECONDS == sum(common.BEAT_SECONDS)


class CombinedSectionReview(GeometryReview):
    video_number = 0

    def construct(self):
        self.pause(common.OPENING_SECONDS)
        combined.adding_subtracting(self)
        self.check_duration(common.OPENING_SECONDS + common.ADDING_SUBTRACTING_SECONDS)


panels.clear()
combined_scene = CombinedSectionReview(skip_animations=True)
combined_scene.render()
assert [item['panels'] for item in combined_scene.constructions] == expected
assert combined_scene.swaps == scene.swaps
report = {'duration': scene.lesson_seconds, 'term_swap_paths_checked': scene.swaps,
          'constructions': scene.constructions, 'shared_combined_section': True,
          'combined_section_end': combined_scene.lesson_seconds}
Path(config.media_dir, 'geometry_review.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
