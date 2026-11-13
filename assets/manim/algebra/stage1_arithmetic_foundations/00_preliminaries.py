"""Complete arithmetic reminder; Manim Community 0.17.3.

From the repository root (or use absolute script paths from any directory):
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries
    python -m manim -qh --fps 60 assets/manim/algebra/stage1_arithmetic_foundations/00_preliminaries.py ArithmeticPreliminaries
Standalone example (each topic module documents its own command):
    python -m manim -ql assets/manim/algebra/stage1_arithmetic_foundations/03_adding_subtracting.py AddingSubtracting

Final MP4 (repository-relative):
    ../manim_media/videos/algebra/stage1_arithmetic_foundations/00_preliminaries.mp4
common.py resolves this destination independently of cwd, for either quality.
Runtime plan: BEAT_SECONDS and PLANNED_SECONDS in common.py.
RealNumberProperties contributes 42 seconds, identically standalone and combined.
SignedMultiplication contributes 70 seconds, standalone and combined.
OrderOfOperations contributes 26 seconds, identically standalone and combined.
FractionsDecimals contributes 40 seconds, identically standalone and combined.
PowersRoots contributes 48 seconds, identically standalone and combined.
RatiosPercentages contributes 32 seconds, identically standalone and combined.
No audio or external assets are needed.
"""

from pathlib import Path
import sys
from importlib import import_module

# Manim loads files by path; anchor package imports to the file, never to cwd.
REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from manim import DOWN, UP, FadeIn, Indicate, VGroup
from assets.manim.algebra.stage1_arithmetic_foundations.common import (
    ArithmeticScene, BLUE, MUTED, OPENING_SECONDS, CLOSING_SECONDS, PLANNED_SECONDS,
)
adding_subtracting = import_module("assets.manim.algebra.stage1_arithmetic_foundations.02_adding_subtracting").render_section
signed_multiplication = import_module("assets.manim.algebra.stage1_arithmetic_foundations.03_signed_multiplication").render_section
fractions_decimals = import_module("assets.manim.algebra.stage1_arithmetic_foundations.06_fractions_decimals").render_section
ratios_percentages = import_module("assets.manim.algebra.stage1_arithmetic_foundations.07_ratios_percentages").render_section
order_of_operations = import_module("assets.manim.algebra.stage1_arithmetic_foundations.09_order_of_operations").render_section
powers_roots = import_module("assets.manim.algebra.stage1_arithmetic_foundations.08_powers_roots").render_section
real_number_properties = import_module("assets.manim.algebra.stage1_arithmetic_foundations.05_real_number_properties").render_section


class ArithmeticPreliminaries(ArithmeticScene):
    """Complete video: shared topic sections framed by the original opening/closing."""

    video_number = 0
    source_file = __file__
    output_identity = "algebra/stage1_arithmetic_foundations/00_preliminaries.mp4"

    def construct(self):
        # 0–7: opening, with a wide safe margin for the full Spanish title.
        start = self.lesson_seconds
        title = self.words("Antes de empezar: herramientas de aritmética", 40)
        title.move_to(UP * 0.65)
        caption = self.words("Un repaso de lo que usaremos", 29, MUTED)
        caption.move_to(DOWN * 0.55)
        self.move(FadeIn(title), FadeIn(caption), seconds=1)
        self.finish_beat(start, OPENING_SECONDS)

        adding_subtracting(self)
        signed_multiplication(self)
        real_number_properties(self)
        fractions_decimals(self)
        ratios_percentages(self)
        powers_roots(self)
        order_of_operations(self)

        # The changing numerical input bridges to the next video.
        start = self.topic("Una cantidad que cambia")
        first = self.math("120+3(", "20", ")=180", size=52).move_to(UP * 1.25)
        second = self.math("120+3(", "30", ")=210", size=52).move_to(DOWN * 0.15)
        first[1].set_color(BLUE)
        second[1].set_color(BLUE)
        self.replace_body(VGroup(first))
        self.pause(1.6)
        self.move(FadeIn(second))
        self.pause(1.6)
        self.move(Indicate(first[1], color=BLUE), Indicate(second[1], color=BLUE), seconds=1)
        closing = self.words("Después, una letra representará la cantidad que cambia.", 29)
        closing.move_to(DOWN * 2.15)
        self.move(FadeIn(closing))
        self.finish_beat(start, CLOSING_SECONDS)
        self.check_duration(PLANNED_SECONDS)






