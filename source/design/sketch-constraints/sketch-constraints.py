from typing import List, Tuple, Any
import operator

import manim as mn
from rc_lib.style import color, animation
from rc_lib.math_utils import vector
from rc_lib.view_utils import title_sequence
from rc_lib.common_mobjects import plate, sketch

sketch_color = color.Palette.BLUE

sketch_factory: sketch.SketchFactory = sketch.SketchFactory().set_color(sketch_color)

title: title_sequence.TitleSequence = title_sequence.TitleSequence(
    default_color=sketch_color, add_numbers=False
)


class CoincidentScene(mn.Scene):
    def setup(self):
        self.add_two_lines()
        title.reset()

    def add_two_lines(self):
        self._first = sketch_factory.make_line(
            vector.point_2d(-10, -8), vector.point_2d(10, 8)
        )
        # self._second = sketch_factory.make_line(vector.point_2d(-2, -2), vector.point_2d(-2, 2))

    def construct(self):
        self.play(title.next("Coincident constraint - two points"))
        self.add(self._first)
        # Coincident two line end points together

        self.wait(2)
        self.play(title.next("Coincident constraint - point and straight edge"))

        self.wait(2)
        self.play(title.next("Coincident constraint - two straight edges"))

        self.wait(animation.END_DELAY)
