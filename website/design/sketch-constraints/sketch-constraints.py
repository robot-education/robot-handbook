from typing import Dict, Iterable, List, Sequence, Tuple, cast
import math

import manim as mn
from rc_lib.style import color, animation
from rc_lib.math_utils import vector
from rc_lib.view_utils import sketch_scene
from rc_lib.common_mobjects import sketch

sketch_color = color.Palette.BLUE
sketch_factory: sketch.SketchFactory = sketch.SketchFactory().set_color(sketch_color)


def coincident_common_mobjects() -> (
    Tuple[sketch.SketchCircle, sketch.SketchLine, sketch.SketchLine]
):
    return (
        sketch_factory.make_circle(vector.point_2d(-4.5, 0), 1.5),
        sketch_factory.make_line(
            vector.point_2d(5.25, 4 / 2), vector.point_2d(5.25, -4 / 2)
        ),
        sketch_factory.make_line(
            vector.point_2d(-1.75, 0.75), vector.point_2d(4.25, -1)
        ),
    )


class CoincidentPointToPointScene(sketch_scene.SketchScene):
    def setup(self) -> None:
        mobjects = coincident_common_mobjects()
        self._circle, self._line, self._move_line = mobjects
        self.set_static_mobjects(*mobjects)

    def construct(self) -> None:
        self.run_group(
            self._move_line.click_start(),
            self._circle.click_center(),
            self._move_line.transform(self._circle.get_center(), sketch.LineEnd.START),
        )

        self.run_group(
            self._move_line.click_end(),
            self._line.click_end(),
            self._move_line.transform(self._line.get_end(), sketch.LineEnd.END),
        )


class CoincidentPointToLineScene(sketch_scene.SketchScene):
    def setup(self) -> None:
        mobjects = coincident_common_mobjects()
        self._circle, self._line, self._move_line = mobjects
        self.set_static_mobjects(*mobjects)

    def construct(self) -> None:
        point = (
            self._circle.get_center()
            + vector.normalize(self._move_line.get_start() - self._circle.get_center())
            * self._circle.get_radius()
        )

        self.run_group(
            self._move_line.click_start(),
            self._circle.click_circle(),
            self._move_line.transform(point, sketch.LineEnd.START),
        )

        point = vector.project_to_line(
            self._move_line.get_end(),
            self._line.get_start(),
            self._line.get_end(),
        )

        self.run_group(
            self._move_line.click_end(),
            self._line.click_line(),
            self._move_line.transform(point, sketch.LineEnd.END),
        )


class CoincidentLineToLineScene(sketch_scene.SketchScene):
    def setup(self) -> None:
        start_point = vector.point_2d(-5.75, 2.5)
        middle_point = vector.point_2d(-1.15, 0.5)  # closest to the middle
        self._fixed_line = sketch_factory.make_line(start_point, middle_point)

        slope = vector.normalize(middle_point - start_point)
        self._angle = math.radians(38)
        self._start_line = sketch_factory.make_line(
            middle_point + mn.rotate_vector(slope * 2, self._angle),
            middle_point + mn.rotate_vector(slope * 7.5, self._angle),
        )
        self.set_static_mobjects(self._fixed_line, self._start_line)

    def construct(self) -> None:
        self.run_group(
            self._start_line.click_line(),
            self._fixed_line.click_line(),
            mn.Rotate(
                self._start_line,
                angle=-self._angle,
                about_point=cast(Sequence[float], self._fixed_line.get_end()),
            ),
        )


class VerticalScene(sketch_scene.SketchScene):
    def setup(self):
        pass

    def construct(self):
        pass
