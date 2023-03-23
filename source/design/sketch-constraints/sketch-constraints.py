from typing import Sequence, cast
import math

import manim as mn
from rc_lib.style import color, animation
from rc_lib.math_utils import vector
from rc_lib.view_utils import title_sequence
from rc_lib.common_mobjects import sketch

sketch_color = color.Palette.BLUE

sketch_factory: sketch.SketchFactory = sketch.SketchFactory().set_color(sketch_color)

title: title_sequence.TitleSequence = title_sequence.TitleSequence(
    default_color=sketch_color, add_numbers=False
)


class CoincidentScene(mn.Scene):
    def setup(self) -> None:
        title.reset()

    def setup_first_scene(self) -> None:
        self._circle: sketch.SketchCircle = sketch_factory.make_circle(
            vector.point_2d(-4.5, 0), 1.5
        )
        self._line: sketch.SketchLine = sketch_factory.make_line(
            vector.point_2d(5.25, 4 / 2), vector.point_2d(5.25, -4 / 2)
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

        self.wait(0.5)

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

        self.wait(2)
        self.clear()

    # def setup_point_to_line(self):
    #     self._first = sketch_factory.make_line(
    #         vector.point_2d(-10, -8), vector.point_2d(10, 8)
    #     )
    #     self._second = sketch_factory.make_line(
    #         vector.point_2d(-2, -2), vector.point_2d(-2, 2)
    #     )

    def play_point_to_line(self) -> None:
        self.play(title.next("Point and a line, circle, or arc"))

        self.play(self._move_line.click_vertex(sketch.LineEnd.START))
        self.play(self._circle.click_circle())

        point = (
            self._circle.center()
            + vector.normalize(self._move_line.start_point() - self._circle.center())
            * self._circle.radius()
        )
        self.play(self._move_line.transform(point, sketch.LineEnd.START))

        self.play(self._move_line.click_vertex(sketch.LineEnd.END))
        self.play(self._line.click_line())
        self.play(
            self._move_line.transform(
                vector.project_to_line(
                    self._move_line.end_point(),
                    self._line.start_point(),
                    self._line.end_point(),
                ),
                sketch.LineEnd.END,
            )
        )

        self.wait(1)
        self.clear()

    def setup_line_to_line(self) -> None:
        start_point = vector.point_2d(-6, 1.25)
        middle_point = vector.point_2d(-1.5, -0.25)  # closest to the middle
        self._fixed_line = sketch_factory.make_line(start_point, middle_point)
        slope = vector.normalize(middle_point - start_point)

        rotation_axis = mn.OUT
        self._angle = math.radians(30)
        self._start_line = sketch_factory.make_line(
            middle_point
            + mn.rotate_vector(slope * 1.25, self._angle, axis=rotation_axis),
            middle_point + mn.rotate_vector(slope * 7, self._angle, axis=rotation_axis),
        )

        self.add(self._fixed_line, self._start_line)

    def play_line_to_line(self) -> None:
        self.play(title.next("Two lines"))
        self.play(self._start_line.click_line())
        self.play(self._fixed_line.click_line())
        self.play(
            mn.Rotate(
                self._start_line,
                angle=-self._angle,
                about_point=cast(Sequence[float], self._fixed_line.end_point()),
            )
        )

    def construct(self) -> None:
        self.setup_first_scene()
        self.play_two_points()

        self.setup_first_scene()
        self.play_point_to_line()

        self.setup_line_to_line()
        self.play_line_to_line()

        self.wait(animation.END_DELAY)


# class VerticalScene(mn.Scene):
#     def setup(self):
#         pass

#     def construct(self):
#         pass
