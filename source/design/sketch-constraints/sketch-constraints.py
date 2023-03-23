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
        title.reset()

    def setup_two_points(self):
        self._circle: sketch.SketchCircle = sketch_factory.make_circle(
            vector.point_2d(-4.5, 0), 1.5
        )
        self._line: sketch.SketchLine = sketch_factory.make_line(
            vector.point_2d(5.25, 4.5 / 2), vector.point_2d(5.25, -4.5 / 2)
        )
        self._move_line: sketch.SketchLine = sketch_factory.make_line(
            vector.point_2d(-1.75, 0.75), vector.point_2d(4.25, -1)
        )
        self.add(self._circle, self._line, self._move_line)

    def play_two_points(self):
        self.play(title.next("Two points"))
        self.play(self._move_line.click_vertex(sketch.LineEnd.START))
        self.play(self._circle.click_center())
        self.play(
            mn.Transform(
                self._move_line,
                self._move_line.copy().set_position(
                    self._circle.center(), sketch.LineEnd.START
                ),
            )
        )

        self.play(self._move_line.click_vertex(sketch.LineEnd.END))
        self.play(self._line.click_vertex(sketch.LineEnd.END))
        self.play(
            mn.Transform(
                self._move_line,
                self._move_line.copy().set_position(
                    self._line.end_point(), sketch.LineEnd.END
                ),
            )
        )

        self.play(self._line.click_line())

    def setup_point_to_line(self):
        self._first = sketch_factory.make_line(
            vector.point_2d(-10, -8), vector.point_2d(10, 8)
        )
        self._second = sketch_factory.make_line(
            vector.point_2d(-2, -2), vector.point_2d(-2, 2)
        )

    def setup_line_to_line(self):
        pass

    def construct(self):
        self.setup_two_points()
        self.play_two_points()
        self.wait(2)
        self.clear()

        self.play(title.next("Point and a line"))
        self.wait(2)
        self.clear()
        self.play(title.next("Two lines"))

        self.wait(animation.END_DELAY)


# class VerticalScene(mn.Scene):
#     def setup(self):
#         pass

#     def construct(self):
#         pass
