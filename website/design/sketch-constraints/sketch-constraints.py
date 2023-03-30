from typing import Sequence, Tuple, cast
import math

import manim as mn
from rc_lib.style import color
from rc_lib.math_utils import vector
from rc_lib.view_utils import sketch_scene
from rc_lib.common_mobjects import sketch

sketch_color = color.Palette.BLUE
sketch_factory: sketch.SketchFactory = sketch.SketchFactory().set_color(sketch_color) # type: ignore


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
    def construct(self) -> None:
        circle, line, move_line = coincident_common_mobjects()
        self.introduce(circle, line, move_line)

        self.run_group(
            move_line.click_start(),
            circle.click_center(),
            move_line.animate.set_position(circle.get_center(), sketch.LineEnd.START),
        )

        self.run_group(
            move_line.click_end(),
            line.click_end(),
            move_line.animate.set_position(line.get_end(), sketch.LineEnd.END),
        )


class CoincidentPointToLineScene(sketch_scene.SketchScene):
    def construct(self) -> None:
        circle, line, move_line = coincident_common_mobjects()
        self.introduce(circle, line, move_line)

        point = (
            circle.get_center()
            + vector.normalize(move_line.get_start() - circle.get_center())
            * circle.get_radius()
        )

        self.run_group(
            move_line.click_start(),
            circle.click(),
            move_line.transform(point, sketch.LineEnd.START),
        )

        point = vector.project_to_line(
            move_line.get_end(),
            line.get_start(),
            line.get_end(),
        )

        self.run_group(
            move_line.click_end(),
            line.click(),
            move_line.transform(point, sketch.LineEnd.END),
        )


class CoincidentLineToLineScene(sketch_scene.SketchScene):
    def setup(self) -> None:
        start_point = vector.point_2d(-5.75, 2.5)
        middle_point = vector.point_2d(-1.15, 0.5)  # closest to the middle
        self._fixed_line = sketch_factory.make_line(start_point, middle_point)

        slope = self._fixed_line.get_direction()
        self._angle = math.radians(38)
        self._start_line = sketch_factory.make_line(
            middle_point + mn.rotate_vector(slope * 2, self._angle),
            middle_point + mn.rotate_vector(slope * 7.5, self._angle),
        )
        self.introduce(self._fixed_line, self._start_line)

    def construct(self) -> None:
        self.run_group(
            self._start_line.click(),
            self._fixed_line.click(),
            mn.Rotate(
                self._start_line,
                angle=-self._angle,
                about_point=cast(Sequence[float], self._fixed_line.get_end()),
            ),
        )


def vh_common_line() -> Tuple[sketch.SketchLine, float]:
    return (
        sketch_factory.make_line(
            vector.point_2d(-2.3, -2.3), vector.point_2d(2.3, 2.3)
        ),
        math.radians(45),
    )


class VerticalLineScene(sketch_scene.SketchScene):
    def construct(self):
        start_line, angle = vh_common_line()
        angle = math.radians(90) - angle

        self.introduce(start_line)

        self.run_group(
            start_line.click(),
            mn.Rotate(start_line, angle=angle),
        )


class HorizontalLineScene(sketch_scene.SketchScene):
    def construct(self):
        start_line, angle = vh_common_line()
        angle = -angle
        self.introduce(start_line)

        self.run_group(
            start_line.click(),
            mn.Rotate(start_line, angle=angle),
        )


class VerticalPointsScene(sketch_scene.SketchScene):
    def setup(self):
        self._circle = sketch_factory.make_circle(vector.point_2d(-4, 1.5), 1.5)
        self._line = sketch_factory.make_line(
            vector.point_2d(0, 2.5), vector.point_2d(5.5, 1.5)
        )
        self._move_line = sketch_factory.make_line(
            vector.point_2d(-5.5, -2.5), vector.point_2d(3.5, -1.5)
        )
        self.introduce(self._circle, self._line, self._move_line)

    def construct(self):
        self.run_group(
            self._move_line.click_start(),
            self._circle.click_center(),
            self._move_line.animate.set_position(
                vector.point_2d(
                    self._circle.get_center()[0], self._move_line.get_start()[1]
                ),
                sketch.LineEnd.START,
            ),
        )

        self.run_group(
            self._move_line.click_end(),
            self._line.click_end(),
            self._move_line.animate.set_position(
                vector.point_2d(self._line.get_end()[0], self._move_line.get_end()[1]),
                sketch.LineEnd.END,
            )
        )


class HorizontalPointsScene(sketch_scene.SketchScene):
    def setup(self):
        self._circle = sketch_factory.make_circle(vector.point_2d(-3.5, 1.5), 1.5)
        self._line = sketch_factory.make_line(
            vector.point_2d(-5, -0.75), vector.point_2d(-1, -2.5)
        )
        self._move_line = sketch_factory.make_line(
            vector.point_2d(2, -1.5), vector.point_2d(4.5, 3)
        )
        self.introduce(self._circle, self._line, self._move_line)

    def construct(self):
        self.run_group(
            self._move_line.click_start(),
            self._line.click_end(),
            self._move_line.animate.set_position(
                vector.point_2d(
                    self._move_line.get_start()[0], self._line.get_end()[1]
                ),
                sketch.LineEnd.START,
            ),
        )

        self.run_group(
            self._move_line.click_end(),
            self._circle.click_center(),
            self._move_line.animate.set_position(
                vector.point_2d(
                    self._move_line.get_end()[0],
                    self._circle.get_center()[1],
                ),
                sketch.LineEnd.END,
            ),
        )


class ParallelScene(sketch_scene.SketchScene):
    def setup(self):
        self._line = sketch_factory.make_line(
            vector.point_2d(-6, -3), vector.point_2d(6, 0.5)
        )
        direction = self._line.get_direction()

        end_point = vector.point_2d(5, 3)
        start_point = end_point - direction * 10.5
        self._mid_point = (start_point + end_point) / 2
        end_line = sketch_factory.make_line(start_point, end_point)
        self._angle = math.radians(16.26)
        self._start_line = end_line.rotate(-self._angle, about_point=self._mid_point)  # type: ignore

    def construct(self):
        self.introduce(self._line, self._start_line)
        self.run_group(
            self._start_line.click(),
            self._line.click(),
            mn.Rotate(self._start_line, self._angle, about_point=self._mid_point),  # type: ignore
        )


class PerpendicularScene(sketch_scene.SketchScene):
    def construct(self):
        line = sketch_factory.make_line(
            vector.point_2d(-5, -2.75), vector.point_2d(5.5, 0.5)
        )
        direction = line.get_direction()
        rotation_point = line.get_start() + direction * 2
        perpendicular_direction = vector.direction_2d(-direction[1], direction[0])  # type: ignore
        end_line = sketch_factory.make_line(
            rotation_point + perpendicular_direction * 1,
            rotation_point + perpendicular_direction * 5.25,
        )
        angle = math.radians(45)

        # move to start position
        start_line = end_line.rotate(-angle, about_point=rotation_point)  # type: ignore

        self.introduce(start_line, line)
        self.run_group(
            start_line.click(),
            line.click(),
            # rotate to end position
            mn.Rotate(start_line, angle, about_point=rotation_point),  # type: ignore
        )


def centered_line(line: sketch.SketchLine, length: float) -> sketch.SketchLine:
    """Returns a line centered on the given line with the specified length."""
    center = (line.get_start() + line.get_end()) / 2
    offset = line.get_direction() * length / 2
    return sketch_factory.make_line(center - offset, center + offset)


class EqualLineScene(sketch_scene.SketchScene):
    def construct(self):
        base = sketch_factory.make_line(
            vector.point_2d(-5.5, -1.5), vector.point_2d(-1.25, 2)
        )
        first = sketch_factory.make_line(
            vector.point_2d(-5, -3), vector.point_2d(5, -1)
        )
        second = sketch_factory.make_line(
            vector.point_2d(-0.5, 2.75), vector.point_2d(6, 0.5)
        )

        length = base.get_length()

        self.introduce(base, first, second)
        self.run_group(
            base.click(),
            first.click(),
            mn.Transform(first, centered_line(first, length)),
        )

        self.run_group(
            base.click(),
            second.click(),
            mn.Transform(second, centered_line(second, length)),
        )


class EqualCircleScene(sketch_scene.SketchScene):
    def construct(self):
        circle = sketch_factory.make_circle(vector.point_2d(-4, 1), 2)
        base = sketch_factory.make_circle(vector.point_2d(0, -1.5), 1.5)
        arc = sketch_factory.make_arc(
            vector.point_2d(4, 1), 2, math.radians(90), math.radians(-225)
        )

        self.introduce(base, arc, circle)
        self.run_group(
            base.click(), circle.click(), circle.animate.set_radius(1.5)
        )
        self.run_group(
            base.click(), arc.click(), arc.animate.set_radius(1.5)
        )