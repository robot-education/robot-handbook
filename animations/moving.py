import manim as mn


class MovingAround(mn.Scene):
    def construct(self):
        square = mn.Square(color=mn.BLUE, fill_opacity=1)

        self.play(square.animate.shift(mn.LEFT))
        self.play(square.animate.set_fill(mn.ORANGE))
        self.play(square.animate.scale(0.3))
        self.play(square.animate.rotate(0.4))
