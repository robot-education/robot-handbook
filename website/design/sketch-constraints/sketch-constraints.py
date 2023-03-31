from typing import Sequence, cast
import math

import manim as mn
from rc_lib.style import color
from rc_lib.math_utils import vector
from rc_lib.view_utils import sketch_scene
from rc_lib.common_mobjects import sketch

sketch_color = color.Palette.BLUE
sketch_factory: sketch.SketchFactory = sketch.SketchFactory().set_color(sketch_color)  # type: ignore


def coincident_common_mobjects() -> (
    tuple[sketch.SketchCircle, sketch.SketchLine, sketch.SketchLine]
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
            + vector.direction(circle.get_center(), move_line.get_start())
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


def vh_common_line() -> tuple[sketch.SketchLine, float]:
    return (
        sketch_factory.make_line(
            vector.point_2d(-2.3, -2.3), vector.point_2d(2.3, 2.3)
        ),
        math.radians(45),
    )


class VerticalLineScene(sketch_scene.SketchScene):
    def construct(self) -> None:
        start_line, angle = vh_common_line()
        angle = math.radians(90) - angle

        self.introduce(start_line)

        self.run_group(
            start_line.click(),
            mn.Rotate(start_line, angle=angle),
        )


class HorizontalLineScene(sketch_scene.SketchScene):
    def construct(self) -> None:
        start_line, angle = vh_common_line()
        angle = -angle
        self.introduce(start_line)

        self.run_group(
            start_line.click(),
            mn.Rotate(start_line, angle=angle),
        )


class VerticalPointsScene(sketch_scene.SketchScene):
    def setup(self) -> None:
        self._circle = sketch_factory.make_circle(vector.point_2d(-4, 1.5), 1.5)
        self._line = sketch_factory.make_line(
            vector.point_2d(0, 2.5), vector.point_2d(5.5, 1.5)
        )
        self._move_line = sketch_factory.make_line(
            vector.point_2d(-5.5, -2.5), vector.point_2d(3.5, -1.5)
        )
        self.introduce(self._circle, self._line, self._move_line)

    def construct(self) -> None:
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
            ),
        )


class HorizontalPointsScene(sketch_scene.SketchScene):
    def setup(self) -> None:
        self._circle = sketch_factory.make_circle(vector.point_2d(-3.5, 1.5), 1.5)
        self._line = sketch_factory.make_line(
            vector.point_2d(-5, -0.75), vector.point_2d(-1, -2.5)
        )
        self._move_line = sketch_factory.make_line(
            vector.point_2d(2, -1.5), vector.point_2d(4.5, 3)
        )
        self.introduce(self._circle, self._line, self._move_line)

    def construct(self) -> None:
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
    def setup(self) -> None:
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

    def construct(self) -> None:
        self.introduce(self._line, self._start_line)
        self.run_group(
            self._start_line.click(),
            self._line.click(),
            mn.Rotate(self._start_line, self._angle, about_point=self._mid_point),  # type: ignore
        )


class PerpendicularScene(sketch_scene.SketchScene):
    def construct(self) -> None:
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
    center = line.line.get_midpoint()
    offset = line.get_direction() * length / 2
    return sketch_factory.make_line(center - offset, center + offset)


class EqualLineScene(sketch_scene.SketchScene):
    def construct(self) -> None:
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
    def construct(self) -> None:
        base = sketch_factory.make_circle(vector.point_2d(0, -1.5), 1.5)
        circle = sketch_factory.make_circle(vector.point_2d(-3.5, 1), 2)
        arc = sketch_factory.make_arc(
            vector.point_2d(3.5, 1), 2, math.radians(90), math.radians(-225)
        )

        self.introduce(base, arc, circle)
        self.run_group(base.click(), circle.click(), circle.animate.set_radius(1.5))
        self.run_group(base.click(), arc.click(), arc.animate.set_radius(1.5))


class MidpointLineScene(sketch_scene.SketchScene):
    def construct(self) -> None:
        top = sketch_factory.make_line(vector.point_2d(-6, 3), vector.point_2d(6, 1.25))
        bottom = sketch_factory.make_line(
            vector.point_2d(-6, -3), vector.point_2d(6, -1.25)
        )
        middle = sketch_factory.make_line(
            vector.point_2d(-1, 1.5), vector.point_2d(1, -1.5)
        )

        self.introduce(top, bottom, middle)
        self.run_group(
            middle.click_start(),
            top.click(),
            middle.animate.set_position(top.line.get_midpoint(), sketch.LineEnd.START),
        )
        self.run_group(
            middle.click_end(),
            bottom.click(),
            middle.animate.set_position(bottom.line.get_midpoint(), sketch.LineEnd.END),
        )


class MidpointPointScene(sketch_scene.SketchScene):
    def construct(self) -> None:
        line = sketch_factory.make_line(
            vector.point_2d(-6, 5 / 2), vector.point_2d(-6, -5 / 2)
        )
        circle = sketch_factory.make_circle(vector.point_2d(4.5, 0), 1.5)
        first_line = sketch_factory.make_line(
            vector.point_2d(-1.5, 2), vector.point_2d(0, -2)
        )
        second_line = sketch_factory.make_line(
            vector.point_2d(-5.25, -0.5), vector.point_2d(-1.5, 0.5)
        )

        self.introduce(line, circle, first_line)
        self.run_group(
            line.click_start(),
            first_line.click_start(),
            circle.click_center(),
            first_line.animate.set_position(
                (line.get_start() + circle.get_center()) / 2, sketch.LineEnd.START
            ),
        )
        self.run_group(
            line.click_end(),
            first_line.click_end(),
            circle.click_center(),
            first_line.animate.set_position(
                (line.get_end() + circle.get_center()) / 2, sketch.LineEnd.END
            ),
        )

        self.introduce(second_line)
        self.run_group(
            line.click_start(),
            second_line.click_start(),
            line.click_end(),
            second_line.animate.set_position(
                line.line.get_midpoint(), sketch.LineEnd.START
            ),
        )
        self.run_group(
            first_line.click_start(),
            second_line.click_end(),
            first_line.click_end(),
            second_line.animate.set_position(
                first_line.line.get_midpoint(), sketch.LineEnd.END
            ),
        )


def get_translation(
    line: sketch.SketchLine, circle: sketch.SketchCircle
) -> sketch.SketchLine:
    projection: vector.Point2d = line.line.get_projection(circle.get_center())  # type: ignore
    translation: vector.Vector2d = vector.direction(projection, circle.get_center()) * (
        vector.norm(circle.get_center() - projection) - circle.get_radius()
    )
    return sketch_factory.make_line(
        line.get_start() + translation, line.get_end() + translation
    )


def tangent_transform(
    line: sketch.SketchLine, circle: sketch.SketchCircle
) -> mn.Animation:
    return mn.Succession(
        line.click(), circle.click(), mn.Transform(line, get_translation(line, circle))
    )


class TangentLineScene(sketch_scene.SketchScene):
    def construct(self) -> None:
        circle = sketch_factory.make_circle(mn.ORIGIN, 1.5)
        left = sketch_factory.make_line(
            vector.point_2d(-6, 0), vector.point_2d(0, 2.75)
        )
        right = sketch_factory.make_line(
            vector.point_2d(2, -2.5), vector.point_2d(6, -2)
        )

        self.introduce(circle, left, right)
        self.run_group(tangent_transform(left, circle))
        self.run_group(tangent_transform(right, circle))


def get_circle_translation(
    base: sketch.SketchCircleBase, target: sketch.SketchCircle
) -> sketch.SketchCircleBase:
    vec = target.get_center() - base.get_center()
    translation = vector.normalize(vec) * (
        vector.norm(vec) - base.get_radius() - target.get_radius()
    )
    return base.copy().shift(translation)


def tangent_circle_transform(
    base: sketch.SketchCircleBase, target: sketch.SketchCircle
) -> mn.Animation:
    return mn.Succession(
        base.click(),
        target.click(),
        mn.Transform(base, get_circle_translation(base, target)),
    )


class TangentCircleScene(sketch_scene.SketchScene):
    def construct(self) -> None:
        circle = sketch_factory.make_circle(mn.ORIGIN, 1.5)
        left = sketch_factory.make_circle(vector.point_2d(-4, 1), 1.5)
        right = sketch_factory.make_arc(
            vector.point_2d(6, -1.125), 3.5, math.radians(105), math.radians(75)
        )

        self.introduce(circle, left, right)
        self.run_group(tangent_circle_transform(left, circle))
        self.run_group(tangent_circle_transform(right, circle))


def concentric_common() -> (
    tuple[sketch.SketchCircle, sketch.SketchCircle, sketch.SketchArc]
):
    return (
        sketch_factory.make_circle(mn.ORIGIN, 1.5),
        sketch_factory.make_circle(vector.point_2d(-4, 0), 2),
        sketch_factory.make_arc(
            vector.point_2d(3, 0), 3, math.radians(70), math.radians(-140)
        ),
    )


class ConcentricEdgeScene(sketch_scene.SketchScene):
    def construct(self) -> None:
        circle, left, right = concentric_common()
        self.introduce(circle, left, right)
        # move to origin using shift
        self.run_group(
            left.click(), circle.click(), left.animate.shift(-left.get_center())
        )
        self.run_group(
            right.click(), circle.click(), right.animate.shift(-right.get_center())
        )


class ConcentricPointScene(sketch_scene.SketchScene):
    def construct(self) -> None:
        circle, left, right = concentric_common()
        self.introduce(circle, left, right)

        # move to origin using shift
        self.run_group(
            left.click_center(), circle.click(), left.animate.shift(-left.get_center())
        )

        self.run_group(
            right.click_center(),
            circle.click(),
            right.animate.shift(-right.get_center()),
        )
