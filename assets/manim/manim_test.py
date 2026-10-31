
from manim import *

class MyFirstScene(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=GREEN)

        self.play(Create(circle))
        self.wait(1)

        self.play(Transform(circle, square))
        self.wait(1)

        self.play(FadeOut(circle))
