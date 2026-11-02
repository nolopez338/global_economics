"""Repartir una cuenta: pagos iguales, sin incógnitas algebraicas.

Manim Community 0.17.3. Renderizar desde la raíz del repositorio:
    manim -qh --fps 60 assets/manim/restaurant_bill.py RestaurantBillShares

Los medios se guardan fuera del repositorio, en San Bartolo/manim_media.
"""

from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, UP, WHITE, Brace, Circle, Create, FadeIn, FadeOut,
    Indicate, LaggedStart, Line, MathTex, RoundedRectangle, Scene, Text,
    Transform, TransformFromCopy, VGroup, config,
)

config.media_dir = str(Path(__file__).resolve().parents[5] / "manim_media")
config.background_color = "#0B1426"
config.frame_width = 128 / 9
config.frame_height = 8
# La resolución y los fps se eligen con el comando de renderizado.
NAVY_CARD = "#14243C"
MUTED = "#B8C6DA"
GOLD = "#F4C968"
A_COLOR = "#62AEFF"
B_COLOR = "#62D69A"
C_COLOR = "#FFA45C"
COLORS = (A_COLOR, B_COLOR, C_COLOR)


class RestaurantBillShares(Scene):
    """Una explicación pausada con palabras, cuatro bloques y aritmética."""

    def words(self, message, size=28, color=WHITE, colors=None):
        obj = Text(message, font="Segoe UI", font_size=size, color=color,
                   t2c=colors or {}, disable_ligatures=True, line_spacing=1.15)
        # Mantener márgenes incluso si la fuente se sustituye en otro equipo.
        if obj.width > 12.5:
            obj.scale_to_fit_width(12.5)
        return obj

    def move(self, *animations, seconds=2):
        # Conservar la curva propia de Indicate: debe volver al color original.
        # Transform y FadeIn ya usan una curva suave de forma predeterminada.
        self.play(*animations, run_time=seconds)
        self.lesson_seconds += seconds

    def pause(self, seconds=4):
        self.wait(seconds)
        self.lesson_seconds += seconds

    def explain(self, message, hold=4):
        new = self.words(message, 27, MUTED).move_to([0, -3.16, 0])
        # Un solo lugar de lectura; los cálculos cambian después de la pausa.
        if self.note is None:
            self.move(FadeIn(new))
        else:
            self.move(FadeOut(self.note), FadeIn(new))
        self.note = new
        if hold:
            self.pause(hold)

    def card(self, person, color, xpos):
        panel = RoundedRectangle(
            width=3.85, height=1.65, corner_radius=0.16,
            stroke_color=color, stroke_width=1.6,
            fill_color=NAVY_CARD, fill_opacity=1,
        ).move_to([xpos, 1.85, 0])
        head = Circle(radius=0.11, stroke_width=0,
                      fill_color=color, fill_opacity=1).move_to([xpos, 2.38, 0])
        shoulders = RoundedRectangle(
            width=0.5, height=0.17, corner_radius=0.07, stroke_width=0,
            fill_color=color, fill_opacity=1,
        ).move_to([xpos, 2.15, 0])
        name = self.words("Persona " + person, 28, color).move_to([xpos, 1.85, 0])
        payment = self.words("pago persona " + person, 24)
        payment.move_to([xpos, 1.38, 0])
        # Separar la estructura y el pago evita revivir etiquetas reemplazadas.
        return VGroup(panel, head, shoulders, name), payment

    def term(self, wording, color):
        label = self.words(wording, 26)
        border = RoundedRectangle(
            width=label.width + 0.34, height=0.55, corner_radius=0.08,
            stroke_color=color, stroke_width=1.3,
            fill_color=color, fill_opacity=0.06,
        ).move_to(label)
        return VGroup(border, label)

    def block(self, color, point):
        box = RoundedRectangle(
            width=0.9, height=0.5, corner_radius=0.07,
            stroke_color=color, stroke_width=1.6,
            fill_color=color, fill_opacity=0.2,
        )
        label = self.words("pago", 21)
        return VGroup(box, label).move_to(point)

    def arithmetic(self, pieces, size=40):
        # Cada símbolo y cada número es un objeto semántico independiente.
        parts = VGroup(*[MathTex(tex, font_size=size, color=color)
                         for tex, color in pieces])
        return parts.arrange(RIGHT, buff=0.18)

    def construct(self):
        self.lesson_seconds = 0
        self.note = None

        # 1. Revelar el problema por secciones, con tiempo para leerlas.
        title = self.words("Compartimos la cuenta", 43).move_to(UP * 3)
        opening = VGroup(
            self.words("Tres amigos comparten una cuenta de restaurante de", 31),
            self.words("$96.000 COP.", 40, GOLD),
        ).arrange(DOWN, buff=0.22).move_to(UP * 1.5)
        observation = VGroup(
            self.words("Uno de ellos paga el doble", 33,
                       colors={"el doble": C_COLOR}),
            self.words("que cada uno de los otros dos.", 33),
        ).arrange(DOWN, buff=0.22).move_to(DOWN * 0.25)
        question = self.words("¿Cuánto paga cada persona?", 36).move_to(DOWN * 2)
        self.move(FadeIn(title), FadeIn(opening))
        self.pause()
        self.move(FadeIn(observation))
        self.pause()
        self.move(FadeIn(question))
        self.pause()

        header = self.words("TRES AMIGOS / UNA CUENTA", 25, MUTED)
        header.move_to([-3.8, 3.53, 0])
        total = self.words("$96.000 COP", 29, GOLD).move_to([4.95, 3.53, 0])
        rule = Line([-6.45, 3.18, 0], [6.45, 3.18, 0],
                    stroke_color="#30415A", stroke_width=1)
        self.move(Transform(title, header), TransformFromCopy(opening[1], total),
                  FadeOut(opening), FadeOut(observation), FadeOut(question), Create(rule))

        # 2. Cambiar la unidad explícitamente antes de usar 96.
        self.explain("Trabajaremos en miles de pesos colombianos.")
        conversion = VGroup(
            self.words("$96.000 COP", 37, GOLD), self.words("→", 37),
            self.words("96 mil COP", 37, GOLD),
        ).arrange(RIGHT, buff=0.4).move_to(UP * 0.65)
        self.move(TransformFromCopy(total, conversion[0]),
                  FadeIn(conversion[1]), FadeIn(conversion[2]))
        units = self.words("Cantidades en miles de COP", 22, MUTED)
        units.move_to([0, 2.93, 0])
        self.explain("96 mil COP sigue siendo el total de la cuenta.")
        small_total = self.words("96 mil COP", 29, GOLD).move_to(total)
        self.move(Transform(total, small_total), FadeOut(conversion), FadeIn(units))

        # 3. Identificar los pagos completos antes de abreviarlos.
        cards, payments = [], []
        for person, color, xpos in zip("ABC", COLORS, (-4.25, 0, 4.25)):
            structure, payment = self.card(person, color, xpos)
            cards.append(structure)
            payments.append(payment)
        self.move(*[FadeIn(c) for c in cards], *[FadeIn(p) for p in payments])
        self.explain("Los tres pagos completan el total de la cuenta.")
        terms = [self.term("pago persona " + person, color)
                 for person, color in zip("ABC", COLORS)]
        plus1, plus2 = self.words("+", 31), self.words("+", 31)
        equals, bill = self.words("=", 32), self.words("96", 36, GOLD)
        top_row = VGroup(terms[0], plus1, terms[1], plus2)
        top_row.arrange(RIGHT, buff=0.22).move_to([0, -0.85, 0])
        bottom_row = VGroup(terms[2], equals, bill)
        bottom_row.arrange(RIGHT, buff=0.22).move_to([0, -1.65, 0])
        self.move(LaggedStart(*[
            TransformFromCopy(payments[index], terms[index]) for index in range(3)
        ], lag_ratio=0.2), FadeIn(plus1), FadeIn(plus2), FadeIn(equals), FadeIn(bill),
                  seconds=3)

        # 4. Observar, demostrar y solamente después sustituir el pago de B.
        self.explain("Las personas A y B pagan lo mismo.")
        self.move(Indicate(cards[0][0], color=A_COLOR, scale_factor=1.025))
        self.move(Indicate(cards[1][0], color=B_COLOR, scale_factor=1.025))
        relation = self.words("pago persona B = pago persona A", 28)
        relation.move_to([0, -0.05, 0])
        blocks = [self.block(A_COLOR, [-4.25, 0.6, 0]),
                  self.block(B_COLOR, [0, 0.45, 0])]
        self.move(FadeIn(relation), FadeIn(blocks[0]), FadeIn(blocks[1]))
        self.move(blocks[1].animate.move_to([0, 0.6, 0]))
        self.pause(2)
        replacement = self.term("pago persona A", B_COLOR).move_to(terms[1])
        self.move(TransformFromCopy(terms[0], replacement), FadeOut(terms[1]))
        terms[1] = replacement
        # El borde verde mantiene la conexión con la persona B.

        # 5. Dos bloques iguales forman el pago de C.
        self.explain("La persona C paga el doble que la persona A.")
        double_relation = self.words("pago persona C = 2 × pago persona A", 28)
        double_relation.move_to(relation)
        orange1 = self.block(C_COLOR, [4.25, 0.6, 0])
        self.move(FadeOut(relation), FadeIn(double_relation),
                  TransformFromCopy(blocks[0], orange1), seconds=3)
        relation = double_relation
        orange2 = self.block(C_COLOR, [4.8, 0.6, 0])
        self.move(orange1.animate.move_to([3.7, 0.6, 0]),
                  TransformFromCopy(orange1, orange2))
        blocks.extend([orange1, orange2])
        self.pause(2)
        replacement = self.term("2 × pago persona A", C_COLOR)
        wider_row = VGroup(replacement, equals.copy(), bill.copy())
        wider_row.arrange(RIGHT, buff=0.22).move_to([0, -1.65, 0])
        self.move(TransformFromCopy(relation, replacement), FadeOut(terms[2]),
                  equals.animate.move_to(wider_row[1]), bill.animate.move_to(wider_row[2]))
        terms[2] = replacement

        # 6. «pago» es una palabra para un monto, nunca una letra desconocida.
        self.explain("Para escribir menos, llamaremos «pago»\nal monto que paga la persona A.")
        short_demo = VGroup(self.words("pago persona A", 27),
                            self.words("→", 29), self.words("pago", 29))
        short_demo.arrange(RIGHT, buff=0.3).move_to([0, -0.05, 0])
        self.move(FadeOut(relation), FadeIn(short_demo))
        self.explain("La persona B también paga un pago.\nLa persona C paga dos pagos.")
        reference = self.words("pago = monto que paga la persona A", 22, MUTED)
        reference.move_to([0, -2.3, 0])
        self.move(FadeOut(short_demo), FadeIn(reference))
        for term, wording, color in zip(terms, ("pago", "pago", "2 × pago"), COLORS):
            self.move(Transform(term, self.term(wording, color).move_to(term)))

        # 7. Reunir los cuatro bloques y contarlos sin perder sus colores.
        all_terms = VGroup(terms[0], plus1, terms[1], plus2, terms[2], equals, bill)
        compact = all_terms.copy().arrange(RIGHT, buff=0.2).move_to([0, -1.25, 0])
        row_positions = (-1.65, -0.55, 0.55, 1.65)
        self.move(*[term.animate.move_to(target)
                    for term, target in zip(all_terms, compact)],
                  *[block.animate.move_to([pos, 0.6, 0])
                    for block, pos in zip(blocks, row_positions)])
        counter = self.words("1", 31).move_to([0, -0.15, 0])
        for index, block in enumerate(blocks):
            target = self.words(str(index + 1), 31).move_to(counter)
            change = FadeIn(counter) if index == 0 else Transform(counter, target)
            self.move(Indicate(block[0], color=block[0].get_stroke_color(),
                               scale_factor=1.07), change)
        self.explain("En total hay cuatro pagos iguales.")
        four_payments = VGroup(self.words("4 ×", 37), self.words("pago", 37),
                               self.words("=", 37), self.words("96", 40, GOLD))
        four_payments.arrange(RIGHT, buff=0.22).move_to([0, -1.25, 0])
        self.move(TransformFromCopy(counter, four_payments[0]),
                  TransformFromCopy(terms[0][1], four_payments[1]),
                  TransformFromCopy(equals, four_payments[2]),
                  TransformFromCopy(bill, four_payments[3]),
                  FadeOut(all_terms), FadeOut(counter))

        # 8. Repartir 96 entre los cuatro bloques; no hay cancelación simbólica.
        self.explain("Dividimos el total entre los cuatro pagos iguales.")
        brace = Brace(VGroup(*blocks), DOWN, buff=0.1, color=GOLD)
        brace_label = self.words("96 en total", 25, GOLD).next_to(brace, DOWN, buff=0.08)
        self.move(Create(brace), TransformFromCopy(four_payments[3], brace_label))
        division = VGroup(self.words("pago", 38), self.words("=", 38),
                          self.words("96", 40, GOLD), self.words("÷", 38),
                          self.words("4", 40))
        division.arrange(RIGHT, buff=0.22).move_to([0, -1.25, 0])
        self.move(FadeOut(four_payments), FadeIn(division))
        result = VGroup(self.words("pago", 38), self.words("=", 38), self.words("24", 40))
        result.arrange(RIGHT, buff=0.22).move_to(division)
        self.move(TransformFromCopy(division[0], result[0]),
                  TransformFromCopy(division[1], result[1]),
                  TransformFromCopy(VGroup(*division[2:]), result[2]), FadeOut(division))
        self.move(*[Transform(block[1], self.words("24", 25).move_to(block[1]))
                    for block in blocks])
        self.explain("Cada pago equivale a 24 mil COP.")

        # 9. Devolver los bloques a sus personas y revelar cada monto por turno.
        self.move(FadeOut(brace), FadeOut(brace_label),
                  *[block.animate.move_to(point) for block, point in zip(
                      blocks, ([-4.25, 0.6, 0], [0, 0.6, 0],
                               [3.7, 0.6, 0], [4.8, 0.6, 0]))])
        for index in (0, 1):
            new_payment = self.words("24 mil COP", 29, COLORS[index]).move_to(payments[index])
            self.move(TransformFromCopy(blocks[index][1], new_payment), FadeOut(payments[index]))
            payments[index] = new_payment
            self.pause(2)
        multiply = self.arithmetic([("2", C_COLOR), (r"\times", C_COLOR),
                                    ("24", C_COLOR)], 32).move_to(payments[2])
        self.move(TransformFromCopy(VGroup(blocks[2][1], blocks[3][1]), multiply),
                  FadeOut(payments[2]))
        self.pause(2)
        c_result = self.words("2 × 24 = 48 mil COP", 25, C_COLOR).move_to(multiply)
        self.move(Transform(multiply, c_result))
        payments[2] = multiply

        # 10. Comprobar primero en miles y luego volver a pesos completos.
        check_sum = self.arithmetic([
            ("24", A_COLOR), ("+", WHITE), ("24", B_COLOR), ("+", WHITE),
            ("48", C_COLOR), ("=", WHITE), ("96", GOLD),
        ], 44).move_to([0, -1.25, 0])
        self.move(FadeOut(result), FadeOut(reference),
                  *[TransformFromCopy(payments[i], check_sum[j])
                    for i, j in enumerate((0, 2, 4))],
                  *[FadeIn(check_sum[i]) for i in (1, 3, 5, 6)])
        self.wait(1)