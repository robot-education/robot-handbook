from typing import Sequence, Tuple, cast
import math

import manim as mn
from rc_lib.style import color, animation
from rc_lib.math_utils import vector
from rc_lib.common_mobjects import sketch

sketch_color = color.Palette.BLUE

sketch_factory: sketch.SketchFactory = sketch.SketchFactory().set_color(sketch_color)

coincident_objects: Tuple[sketch.SketchCircle, sketch.SketchLine, sketch.SketchLine] = (
    sketch_factory.make_circle(vector.point_2d(-4.5, 0), 1.5),
    sketch_factory.make_line(
        vector.point_2d(5.25, 4 / 2), vector.point_2d(5.25, -4 / 2)
    ),
    sketch_factory.make_line(vector.point_2d(-1.75, 0.75), vector.point_2d(4.25, -1)),
)


class CoincidentPointToPointScene(mn.Scene):
    def setup(self) -> None:
        copies = [c.copy() for c in coincident_objects]
        self._circle, self._line, self._move_line = copies
        self.add(*copies)

    def construct(self) -> None:
        self.play(self._move_line.click_start())
        self.play(self._circle.click_center())
        self.play(
            self._move_line.transform(self._circle.get_center(), sketch.LineEnd.START)
        )
        self.wait(0.5)

        self.play(self._move_line.click_end())
        self.play(self._line.click_end())
        self.play(self._move_line.transform(self._line.get_end(), sketch.LineEnd.END))

        self.wait(animation.END_DELAY)


class CoincidentPointToLineScene(mn.Scene):
    def setup(self) -> None:
        copies = [c.copy() for c in coincident_objects]
        self._circle, self._line, self._move_line = copies
        self.add(*copies)

    def construct(self) -> None:
        self.play(self._move_line.click_start())
        self.play(self._circle.click_circle())

        point = (
            self._circle.get_center()
            + vector.normalize(self._move_line.get_start() - self._circle.get_center())
            * self._circle.get_radius()
        )
        self.play(self._move_line.transform(point, sketch.LineEnd.START))
        self.wait(0.5)

        self.play(self._move_line.click_end())
        self.play(self._line.click_line())

        point = vector.project_to_line(
            self._move_line.get_end(),
            self._line.get_start(),
            self._line.get_end(),
        )
        self.play(self._move_line.transform(point, sketch.LineEnd.END))
        self.wait(animation.END_DELAY)


class CoincidentLineToLineScene(mn.Scene):
    def setup(self) -> None:
        start_point = vector.point_2d(-6, 1.25)
        middle_point = vector.point_2d(-1.5, -0.25)  # closest to the middle
        self._fixed_line = sketch_factory.make_line(start_point, middle_point)

        slope = vector.normalize(middle_point - start_point)
        self._angle = math.radians(30)
        self._start_line = sketch_factory.make_line(
            middle_point + mn.rotate_vector(slope * 1.25, self._angle),
            middle_point + mn.rotate_vector(slope * 7, self._angle),
        )

    def construct(self) -> None:
        self.play(
            mn.AnimationGroup(self._fixed_line.create(), self._start_line.create())
        )
        self.wait(1)

        self.play(self._start_line.click_line())
        self.play(self._fixed_line.click_line())
        self.play(
            mn.Rotate(
                self._start_line,
                angle=-self._angle,
                about_point=cast(Sequence[float], self._fixed_line.get_end()),
            )
        )

        self.wait(animation.END_DELAY)
        self.play(
            mn.AnimationGroup(self._fixed_line.uncreate(), self._start_line.uncreate())
        )
        self.wait(1)


# class VerticalScene(mn.Scene):
#     def setup(self):
#         pass

#     def construct(self):
#         pass
