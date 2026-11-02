"""Una expresión para explorar planetas lejanos (unos 104 segundos).

Manim Community 0.17.3. Desde la raíz del repositorio:
    manim -ql assets/manim/algebra/stage2_algebraic_expressions/exoplanet_transit.py ExoplanetTransit
    manim -qh --fps 60 assets/manim/algebra/stage2_algebraic_expressions/exoplanet_transit.py ExoplanetTransit

Medios: San Bartolo/manim_media, resuelto desde este archivo, como en
restaurant_bill.py. Sin imágenes externas ni dependencias adicionales.
Modelo: https://heasarc.gsfc.nasa.gov/W3Browse/star-catalog/exoplanodb.html
(Transit_Depth). La intersección de discos solo sincroniza la animación;
no se presenta como contenido de la lección.
Videos: San Bartolo/manim_media/videos/algebra/stage2_2/{quality}.
"""

from math import acos, pi, sqrt
from pathlib import Path
import sys

# Manim loads scripts by path; imports must also work outside the repository.
REPOSITORY_ROOT = str(Path(__file__).resolve().parents[4])
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from assets.manim.algebra.output_config import AlgebraScene

import numpy as np
from manim import (
    DOWN, RIGHT, WHITE, Circle, Create, Dot, FadeIn, FadeOut, Indicate,
    Line, MathTex, Scene, Text, Transform, TransformFromCopy, ValueTracker,
    VGroup, VMobject, config, linear,
)

config.media_dir = str(Path(__file__).resolve().parents[5] / "manim_media")
config.background_color = "#0B1426"
config.frame_width = 128 / 9
config.frame_height = 8

MUTED = "#B8C6DA"
GOLD = "#F4C968"                 # R: estrella
BLUE = "#62AEFF"                 # r: planeta
GREEN = "#62D69A"                # d: luz bloqueada
PLANET = "#070C16"


def blocked_fraction(separation, ratio):
    """Área solapada / área estelar; estrella de radio unidad y luz uniforme."""
    distance = abs(separation)
    if distance >= 1 + ratio:
        return 0.0
    if distance <= 1 - ratio:
        return ratio ** 2
    a = acos(np.clip((distance ** 2 + 1 - ratio ** 2) / (2 * distance), -1, 1))
    b = acos(np.clip((distance ** 2 + ratio ** 2 - 1)
                     / (2 * distance * ratio), -1, 1))
    radical = ((-distance + 1 + ratio) * (distance + 1 - ratio)
               * (distance - 1 + ratio) * (distance + 1 + ratio))
    return (a + ratio ** 2 * b - 0.5 * sqrt(max(0, radical))) / pi


class ExoplanetTransit(AlgebraScene):
    """Cantidades, expresión y sustitución, sin resolver ecuaciones."""

    stage_number = 2
    video_number = 2

    def words(self, message, size=28, color=WHITE):
        obj = Text(message, font="Segoe UI", font_size=size, color=color,
                   disable_ligatures=True, line_spacing=1.15)
        if obj.width > 12.5:
            obj.scale_to_fit_width(12.5)
        return obj

    def move(self, *animations, seconds=1):
        self.play(*animations, run_time=seconds)
        self.lesson_seconds += seconds

    def pause(self, seconds):
        self.wait(seconds)
        self.lesson_seconds += seconds

    def caption(self, message, hold=3):
        note = self.words(message, 26, MUTED).move_to([0, -3.15, 0])
        if self.note is not None:
            # Evitar palabras superpuestas durante un cambio de pie de escena.
            self.move(FadeOut(self.note), seconds=0.4)
            self.move(FadeIn(note), seconds=0.6)
        else:
            self.move(FadeIn(note))
        self.note = note
        self.pause(hold)

    def formula(self, size=48):
        result = MathTex("d", r"\approx", r"\left(", "r", "/", "R",
                         r"\right)^2", font_size=size)
        for index, color in ((0, GREEN), (3, BLUE), (5, GOLD)):
            result[index].set_color(color)
        return result

    def graph_point(self, time, depth):
        # Una pérdida de 0.01 ocupa 1.5 unidades: desviación vertical ×100
        # frente a una escala donde una fracción de 1 ocuparía 1.5 unidades.
        return np.array([0.9 + 4.9 * time, 1.25 - 150 * depth, 0])

    def make_diagram(self):
        self.star_center = np.array([-3.8, 0.55, 0])
        self.star_radius = 1.15
        self.star = Circle(radius=self.star_radius, color=GOLD,
                           fill_color=GOLD, fill_opacity=1, stroke_width=1)
        self.star.move_to(self.star_center)
        star_label = self.words("Estrella", 24, GOLD).move_to([-3.8, 2.1, 0])
        axes = VGroup(Line([0.9, -0.65, 0], [0.9, 1.7, 0], color=MUTED),
                      Line([0.9, -0.65, 0], [6.05, -0.65, 0], color=MUTED))
        labels = VGroup(
            self.words("Brillo observado", 24).move_to([3.4, 2.1, 0]),
            self.words("Tiempo", 22).move_to([3.4, -1.05, 0]),
            self.words("100%", 18, MUTED).move_to([0.35, 1.25, 0]),
            self.words("99%", 18, MUTED).move_to([0.35, -0.25, 0]),
            self.words("Variación vertical ampliada ×100", 20, MUTED)
                .move_to([3.4, -1.65, 0]),
        )
        baseline = Line(self.graph_point(0, 0), self.graph_point(1, 0),
                        color=MUTED, stroke_width=1, stroke_opacity=0.45)
        return VGroup(self.star, star_label, axes, labels, baseline)

    def transit(self, ratio, seconds=6):
        """El mismo reloj controla posición, área bloqueada y trazo del gráfico."""
        clock = ValueTracker(0)
        planet = Circle(radius=self.star_radius * ratio, stroke_width=1,
                        stroke_color=BLUE, fill_color=PLANET, fill_opacity=1)

        def separation(time):
            return -1.5 + 3 * time

        def planet_update(obj):
            obj.move_to(self.star_center + RIGHT * self.star_radius
                        * separation(clock.get_value()))

        def point(time):
            return self.graph_point(time, blocked_fraction(separation(time), ratio))

        curve = VMobject(color=GREEN, stroke_width=3)

        def curve_update(obj):
            end = max(clock.get_value(), 0.00001)
            obj.set_points_as_corners([point(t) for t in np.linspace(0, end, 181)])

        cursor = Dot(radius=0.055, color=GREEN)
        planet.add_updater(planet_update)
        curve.add_updater(curve_update)
        cursor.add_updater(lambda obj: obj.move_to(point(clock.get_value())))
        planet_update(planet)
        curve_update(curve)
        cursor.move_to(point(0))
        self.add(planet, curve, cursor)
        self.play(clock.animate.set_value(1), run_time=seconds, rate_func=linear)
        self.lesson_seconds += seconds
        for obj in (planet, curve, cursor):
            obj.clear_updaters()
        return VGroup(planet, curve, cursor)

    def construct(self):
        self.lesson_seconds = 0
        self.note = None
        opening = self.words(
            "¿Cómo estudiar un planeta\nque no podemos ver directamente?", 40)
        self.move(FadeIn(opening), seconds=1.5)
        self.pause(4)
        bridge = self.words("De una cuenta cotidiana a una estrella lejana", 28, MUTED)
        bridge.move_to([0, -1.8, 0])
        self.move(FadeIn(bridge))
        self.pause(2)
        header = self.words("LEER LA LUZ CON ÁLGEBRA", 28, MUTED).move_to([0, 3.45, 0])
        self.move(FadeOut(opening), FadeOut(bridge), FadeIn(header))

        diagram = self.make_diagram()
        model = self.words("Modelo simplificado: planeta oscuro; estrella de brillo uniforme.",
                           20, MUTED).move_to([0, -2.3, 0])
        self.move(FadeIn(diagram), FadeIn(model))
        self.caption("Al pasar delante de la estrella, el planeta bloquea parte de su luz.", hold=2)
        trace = self.transit(0.10, seconds=7)
        self.caption("El brillo baja durante el paso y luego recupera su nivel inicial.", hold=2)
        self.move(FadeOut(trace))

        # Comparación cualitativa con la misma estrella y la misma escala.
        size_label = self.words("Planeta pequeño", 25, BLUE).move_to([-3.8, -1.1, 0])
        self.move(FadeIn(size_label))
        small_trace = self.transit(0.05, seconds=4)
        self.caption("Un planeta mayor bloquea más luz de la misma estrella.", hold=2)
        larger = self.words("Planeta mayor", 25, BLUE).move_to(size_label)
        self.move(FadeOut(small_trace), Transform(size_label, larger))
        large_trace = self.transit(0.10, seconds=4)
        self.pause(1)
        self.move(FadeOut(large_trace), FadeOut(size_label), FadeOut(diagram), FadeOut(model),
                  FadeOut(self.note))
        self.note = None

        # Primero palabras, después símbolos con referentes geométricos.
        word_relation = VGroup(
            self.words("fracción de luz bloqueada", 32, GREEN),
            self.words("≈ (radio del planeta / radio de la estrella)²", 30),
        ).arrange(DOWN, buff=0.3).move_to([0, 1.8, 0])
        self.move(FadeIn(word_relation))
        self.caption("Con el planeta completamente delante de la estrella,\ncomparamos los radios y elevamos la razón al cuadrado.", hold=5)

        star = Circle(radius=0.95, color=GOLD, fill_opacity=0.18).move_to([-4.5, -0.5, 0])
        planet = Circle(radius=0.28, color=BLUE, fill_color=PLANET, fill_opacity=1)
        planet.move_to([-1.3, -0.5, 0])
        r_line = Line(planet.get_center(), planet.get_right(), color=BLUE, stroke_width=4)
        R_line = Line(star.get_center(), star.get_right(), color=GOLD, stroke_width=4)
        scale_note = self.words("Esquema de radios", 18, MUTED).move_to([-3, -1.8, 0])
        self.move(FadeIn(star), FadeIn(planet), FadeIn(scale_note))
        definitions = VGroup()
        for tex, description, color, y, source in (
            ("r", "radio del planeta", BLUE, 0.3, r_line),
            ("R", "radio de la estrella", GOLD, -0.45, R_line),
            ("d", "fracción de luz bloqueada", GREEN, -1.2, None),
        ):
            symbol = MathTex(tex, color=color, font_size=38).move_to([0.8, y, 0])
            label = self.words(description, 25, color).next_to(symbol, RIGHT, buff=0.3)
            row = VGroup(symbol, label)
            if source is not None:
                self.move(Create(source), TransformFromCopy(source, symbol), FadeIn(label))
            else:
                self.move(TransformFromCopy(word_relation[0], symbol), FadeIn(label))
            definitions.add(row)
            self.pause(2)
        self.caption("Los dos radios usan las mismas unidades.\nd es una fracción; todavía no es un porcentaje.", hold=4)
        formula = self.formula().move_to([0, 1.8, 0])
        self.move(TransformFromCopy(definitions[0][0], formula[3]),
                  TransformFromCopy(definitions[1][0], formula[5]),
                  TransformFromCopy(definitions[2][0], formula[0]),
                  *[FadeIn(formula[i]) for i in (1, 2, 4, 6)], FadeOut(word_relation))
        self.pause(3)
        self.move(*[FadeOut(obj) for obj in (star, planet, r_line, R_line, scale_note, definitions)],
                  formula.animate.move_to([0, 2.65, 0]), FadeOut(self.note))
        self.note = None

        # Los tamaños reales del dibujo y las profundidades tienen razón 2 y 4.
        self.move(FadeIn(diagram))
        hypothetical = self.words("Ejemplos hipotéticos · misma estrella", 20, MUTED)
        hypothetical.move_to([0, -2.25, 0])
        self.move(FadeIn(hypothetical))
        for ratio, ratio_tex, fraction_tex, percent_tex in (
            (0.10, "0.10", "0.01", r"1\%"),
            (0.05, "0.05", "0.0025", r"0.25\%"),
        ):
            substitution = MathTex(r"r/R = " + ratio_tex, font_size=28, color=BLUE)
            substitution.move_to([-3.8, -1.25, 0])
            calculation = MathTex("d", r"\approx", "(" + ratio_tex + ")^2",
                                  "=", fraction_tex, "=", percent_tex, font_size=37)
            calculation[0].set_color(GREEN)
            calculation[2].set_color(BLUE)
            calculation[4].set_color(GREEN)
            calculation[6].set_color(GREEN)
            calculation.move_to([0, -3.15, 0])
            self.move(FadeIn(substitution), TransformFromCopy(formula, calculation))
            trace = self.transit(ratio, seconds=5)
            self.pause(3)
            self.move(FadeOut(trace), FadeOut(substitution), FadeOut(calculation))

        self.move(FadeOut(diagram), FadeOut(hypothetical),
                  formula.animate.move_to([0, 0.9, 0]).scale(1.3))
        self.caption("Una misma expresión describe muchos planetas posibles.\nAl cambiar las cantidades, cambia la predicción.", hold=4)
        self.move(Indicate(formula[3], color=BLUE), Indicate(formula[0], color=GREEN))
        self.move(FadeOut(formula), FadeOut(self.note), FadeOut(header))
        self.note = None
        closing = self.words("Una expresión conecta cantidades.\nEl álgebra nos permite trabajar con esa relación.", 35)
        self.move(FadeIn(closing), seconds=1.5)
        self.pause(5)
        self.move(FadeOut(closing))
        # También permite comprobar el ritmo sin depender de la calidad del render.
        print(f"ExoplanetTransit: {self.lesson_seconds:.1f} segundos")
