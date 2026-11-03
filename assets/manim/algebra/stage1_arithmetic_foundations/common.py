"""Shared appearance, layout, animation and explicit clocks (Manim 0.17.3).

Render a topic through its module, or the complete video through 00_preliminaries.py.
Videos: San Bartolo/manim_media/videos/algebra/stage1.
The scene numbers are declared in each video module; paths are file-relative.
"""

from pathlib import Path

from manim import (
    UP, WHITE, Create, FadeIn, FadeOut, Line, MathTex, Scene, Text, VGroup, config,
)

config.media_dir = str(Path(__file__).resolve().parents[5] / "manim_media")
config.background_color = "#0B1426"
config.frame_width = 128 / 9
config.frame_height = 8

MUTED = "#B8C6DA"
GOLD = "#F4C968"
BLUE = "#62AEFF"
GREEN = "#62D69A"

# Each section owns its incoming transition, including signed multiplication.
OPENING_SECONDS = 7
ADDING_SUBTRACTING_SECONDS = 7.65
SIGNED_MULTIPLICATION_SECONDS = 40
FRACTIONS_SECONDS = 40
RATIOS_SECONDS = 32
ORDER_SECONDS = 26
POWERS_SECONDS = 48
PROPERTIES_SECONDS = 42
CLOSING_SECONDS = 13
BEAT_SECONDS = (OPENING_SECONDS, ADDING_SUBTRACTING_SECONDS,
                SIGNED_MULTIPLICATION_SECONDS, PROPERTIES_SECONDS, FRACTIONS_SECONDS,
                RATIOS_SECONDS, POWERS_SECONDS, ORDER_SECONDS, CLOSING_SECONDS)
PLANNED_SECONDS = sum(BEAT_SECONDS)


class ArithmeticScene(Scene):
    """All plays and waits use the explicit lesson clock, including reading pauses."""

    stage_number = 1

    def __init__(self, *args, **kwargs):
        config.video_dir = "{media_dir}/videos/algebra/stage1"
        # Match the source filename so the videos sort in the lesson order.
        source_name = {
            0: "preliminaries", 1: "adding_subtracting",
            2: "signed_multiplication_absolute_value", 3: "real_number_properties",
            4: "fractions_decimals", 5: "ratios_percentages",
            6: "powers_roots", 7: "order_of_operations",
        }[self.video_number]
        config.output_file = f"{self.video_number:02d}_{source_name}"
        super().__init__(*args, **kwargs)

    def setup(self):
        super().setup()
        self.lesson_seconds = 0.0
        self.beat_end_seconds = []

    def check_duration(self, expected):
        if abs(self.lesson_seconds - expected) > 1e-6:
            raise ValueError(f"Duración inesperada: {self.lesson_seconds} != {expected}")

    def words(self, message, size=30, color=WHITE):
        result = Text(message, font="Segoe UI", font_size=size, color=color,
                      disable_ligatures=True, line_spacing=1.15)
        if result.width > 12.3:
            result.scale_to_fit_width(12.3)
        return result

    def math(self, *pieces, size=49):
        result = MathTex(*pieces, font_size=size)
        if result.width > 12:
            result.scale_to_fit_width(12)
        return result

    def move(self, *animations, seconds=0.65):
        self.play(*animations, run_time=seconds)
        self.lesson_seconds += seconds

    def pause(self, seconds):
        self.wait(seconds)
        self.lesson_seconds += seconds

    def finish_beat(self, start, budget):
        remaining = budget - (self.lesson_seconds - start)
        if remaining < -1e-6:
            raise ValueError("El bloque excede su presupuesto de tiempo")
        if remaining > 1e-6:
            self.pause(remaining)
        self.beat_end_seconds.append(self.lesson_seconds)

    def topic(self, label):
        start = self.lesson_seconds
        old = list(self.mobjects)
        heading = self.words(label, 32).move_to(UP * 3.12)
        rule = Line([-6.2, 2.65, 0], [6.2, 2.65, 0],
                    stroke_color="#30415A", stroke_width=1)
        self.move(*[FadeOut(obj) for obj in old], FadeIn(heading),
                  Create(rule), seconds=0.8)
        self.header = (heading, rule)
        return start

    def replace_body(self, new, seconds=0.65):
        # FadeIn registers each later reveal separately in Manim 0.17.3.
        # Animate those actual scene objects, rather than a subsequently
        # enlarged VGroup whose cached family may omit the later reveals.
        previous = [obj for obj in self.mobjects if obj not in self.header]
        self.move(*[FadeOut(obj) for obj in previous], FadeIn(new), seconds=seconds)

    def chain(self, pieces, y=0.3, size=49, hold=1.8):
        """Lay out the full equality first, then reveal intact semantic chunks."""
        row = self.math(*pieces, size=size).move_to(UP * y)
        for part in row[1:-1]:
            part.set_color(BLUE)
        row[-1].set_color(GREEN)
        self.replace_body(VGroup(row[0]))
        self.pause(hold)
        for part in row[1:]:
            self.move(FadeIn(part))
            self.pause(hold)
        return row


class TopicScene(ArithmeticScene):
    """A standalone topic runs exactly the same section as the complete video."""

    section = None
    planned_seconds = None

    def construct(self):
        self.section(standalone=True)
        self.check_duration(self.planned_seconds)




