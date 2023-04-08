"""Animations showcasing various Onshape sketch constraints."""

import math

import manim as mn
from rc_lib.math_utils import vector
from rc_lib.design import sketch, sketch_utils, sketch_scene, constraint


def coincident_common_mobjects() -> tuple[sketch.Circle, sketch.Line, sketch.Line]:
    """Returns mobjects common to coincident point scenes."""
    return (
        sketch.make_circle(vector.point_2d(-4.5, 0), 1.5),
        sketch.make_line(vector.point_2d(5.25, 4 / 2), vector.point_2d(5.25, -4 / 2)),
        sketch.make_line(vector.point_2d(-1.75, 0.75), vector.point_2d(4.25, -1)),
    )


class CoincidentPointsScene(sketch_scene.Scene):
    def construct(self) -> None:
        circle, line, move_line = coincident_common_mobjects()
        self.introduce(circle, line, move_line)
        self.run_group(
            constraint.Coincident(move_line, circle.middle, base_key="start")
        )
        self.run_group(constraint.Coincident(move_line, line.end, base_key="end"))


class CoincidentPointLineScene(sketch_scene.Scene):
    def construct(self) -> None:
        circle, line, move_line = coincident_common_mobjects()
        self.introduce(circle, line, move_line)
        self.run_group(constraint.Coincident(move_line, circle, base_key="start"))
        self.run_group(constraint.Coincident(move_line, line, base_key="end"))


class CoincidentLineScene(sketch_scene.Scene):
    def construct(self) -> None:
        start_point = vector.point_2d(-5.75, 2.5)
        middle_point = vector.point_2d(-1.15, 0.5)  # closest to the middle
        fixed_line = sketch.make_line(start_point, middle_point)

        slope = fixed_line.get_direction()
        angle = math.radians(38)
        start_line = sketch.make_line(
            middle_point + mn.rotate_vector(slope * 2, angle),
            middle_point + mn.rotate_vector(slope * 7.5, angle),
        )

        self.introduce(fixed_line, start_line)
        self.run_group(
            sketch_utils.Click(start_line),
            sketch_utils.Click(fixed_line),
            start_line.animate.rotate(-angle, about_point=fixed_line.get_end()),  # type: ignore
        )


def vh_common_line() -> tuple[sketch.Line, float]:
    return (
        sketch.make_line(vector.point_2d(-2.3, -2.3), vector.point_2d(2.3, 2.3)),
        math.radians(45),
    )


class VerticalLineScene(sketch_scene.Scene):
    def construct(self) -> None:
        start_line, angle = vh_common_line()
        angle = math.radians(90) - angle

        self.introduce(start_line)

        self.run_group(
            sketch_utils.Click(start_line),
            mn.Rotate(start_line, angle=angle),
        )


class HorizontalLineScene(sketch_scene.Scene):
    def construct(self) -> None:
        start_line, angle = vh_common_line()
        angle = -angle
        self.introduce(start_line)

        self.run_group(
            sketch_utils.Click(start_line),
            mn.Rotate(start_line, angle=angle),
        )


class VerticalPointsScene(sketch_scene.Scene):
    def construct(self) -> None:
        circle = sketch.make_circle(vector.point_2d(-4, 1.5), 1.5)
        line = sketch.make_line(vector.point_2d(0, 2.5), vector.point_2d(5.5, 1.5))
        move_line = sketch.make_line(
            vector.point_2d(-5.5, -2.5), vector.point_2d(3.5, -1.5)
        )

        self.introduce(circle, line, move_line)
        self.run_group(
            constraint.VerticalPoint(move_line, circle.middle, base_key="start")
        )
        self.run_group(constraint.VerticalPoint(move_line, line.end, base_key="end"))


class HorizontalPointsScene(sketch_scene.Scene):
    def construct(self) -> None:
        circle = sketch.make_circle(vector.point_2d(-3.5, 1.5), 1.5)
        line = sketch.make_line(vector.point_2d(-5, -0.75), vector.point_2d(-1, -2.5))
        move_line = sketch.make_line(vector.point_2d(2, -1.5), vector.point_2d(4.5, 3))
        self.introduce(circle, line, move_line)
        self.run_group(
            constraint.HorizontalPoint(move_line, line.end, base_key="start")
        )
        self.run_group(
            constraint.HorizontalPoint(move_line, circle.middle, base_key="end")
        )


class ParallelScene(sketch_scene.Scene):
    def construct(self) -> None:
        line = sketch.make_line(vector.point_2d(-6, -3), vector.point_2d(6, 0.5))
        direction = line.get_direction()

        end_point = vector.point_2d(5, 3)
        start_point = end_point - direction * 10.5
        angle = math.radians(16.26)
        start_line = sketch.make_line(start_point, end_point).rotate(
            -angle, about_point=line.get_midpoint()  # type: ignore
        )

        self.introduce(line, start_line)
        self.run_group(
            sketch_utils.Click(start_line),
            sketch_utils.Click(line),
            start_line.animate.rotate(angle, about_point=line.get_midpoint()),
        )


class PerpendicularScene(sketch_scene.Scene):
    def construct(self) -> None:
        line = sketch.make_line(vector.point_2d(-5, -2.75), vector.point_2d(5.5, 0.5))
        direction = line.get_direction()
        rotation_point = line.get_start() + direction * 2
        perpendicular_direction = vector.direction_2d(-direction[1], direction[0])

        angle = math.radians(45)
        start_line = sketch.make_line(
            rotation_point + perpendicular_direction * 1,
            rotation_point + perpendicular_direction * 5.25,
        ).rotate(-angle, about_point=rotation_point)

        self.introduce(start_line, line)
        self.run_group(
            sketch_utils.Click(start_line),
            sketch_utils.Click(line),
            # rotate to end position
            start_line.animate.rotate(angle, about_point=rotation_point),
        )


class EqualLineScene(sketch_scene.Scene):
    def construct(self) -> None:
        base = sketch.make_line(vector.point_2d(-5.5, -1.5), vector.point_2d(-1.25, 2))
        first = sketch.make_line(vector.point_2d(-5, -3), vector.point_2d(5, -1))
        second = sketch.make_line(vector.point_2d(-0.5, 2.75), vector.point_2d(6, 0.5))

        self.introduce(base, first, second)
        self.run_group(constraint.Equal(base, first))

        self.run_group(constraint.Equal(base, second))


class EqualCircleScene(sketch_scene.Scene):
    def construct(self) -> None:
        base = sketch.make_circle(vector.point_2d(0, -1.5), 1.5)
        circle = sketch.make_circle(vector.point_2d(-3.5, 1), 2)
        arc = sketch.make_arc(
            vector.point_2d(3.5, 1), 2, math.radians(90), math.radians(-225)
        )

        self.introduce(base, arc, circle)
        self.run_group(constraint.Equal(base, circle))
        self.run_group(constraint.Equal(base, arc))


class MidpointLineScene(sketch_scene.Scene):
    def construct(self) -> None:
        top = sketch.make_line(vector.point_2d(-6, 3), vector.point_2d(6, 1.25))
        bottom = sketch.make_line(vector.point_2d(-6, -3), vector.point_2d(6, -1.25))
        middle = sketch.make_line(vector.point_2d(-1, 1.5), vector.point_2d(1, -1.5))

        self.introduce(top, bottom, middle)
        self.run_group(
            sketch_utils.Click(middle.start),
            sketch_utils.Click(top),
            middle.animate.move_start(top.get_midpoint()),
        )
        self.run_group(
            sketch_utils.Click(middle.end),
            sketch_utils.Click(bottom),
            middle.animate.move_end(bottom.get_midpoint()),
        )


class MidpointPointScene(sketch_scene.Scene):
    def construct(self) -> None:
        line = sketch.make_line(vector.point_2d(-6, 5 / 2), vector.point_2d(-6, -5 / 2))
        circle = sketch.make_circle(vector.point_2d(4.5, 0), 1.5)
        first_line = sketch.make_line(vector.point_2d(-1.5, 2), vector.point_2d(0, -2))
        second_line = sketch.make_line(
            vector.point_2d(-5.25, -0.5), vector.point_2d(-1.5, 0.5)
        )

        self.introduce(line, circle, first_line)
        self.run_group(
            sketch_utils.Click(line.start),
            sketch_utils.Click(first_line.start),
            sketch_utils.Click(circle.middle),
            first_line.animate.move_start((line.get_start() + circle.get_center()) / 2),
        )
        self.run_group(
            sketch_utils.Click(line.end),
            sketch_utils.Click(first_line.end),
            sketch_utils.Click(circle.middle),
            first_line.animate.move_end((line.get_end() + circle.get_center()) / 2),
        )

        self.introduce(second_line)
        self.run_group(
            sketch_utils.Click(line.start),
            sketch_utils.Click(second_line.start),
            sketch_utils.Click(line.end),
            second_line.animate.move_start(line.get_midpoint()),
        )
        self.run_group(
            sketch_utils.Click(first_line.start),
            sketch_utils.Click(second_line.end),
            sketch_utils.Click(first_line.end),
            second_line.animate.move_end(first_line.get_midpoint()),
        )


class TangentLineScene(sketch_scene.Scene):
    def construct(self) -> None:
        circle = sketch.make_circle(mn.ORIGIN, 1.5)
        left = sketch.make_line(vector.point_2d(-6, 0), vector.point_2d(0, 2.75))
        right = sketch.make_line(vector.point_2d(2, -2.5), vector.point_2d(6, -2))

        self.introduce(circle, left, right)
        self.run_group(constraint.Tangent(left, circle))
        self.run_group(constraint.Tangent(right, circle))


class TangentCircleScene(sketch_scene.Scene):
    def construct(self) -> None:
        circle = sketch.make_circle(mn.ORIGIN, 1.5)
        left = sketch.make_circle(vector.point_2d(-4, 1), 1.5)
        right = sketch.make_arc(
            vector.point_2d(6, -1.125), 3.5, math.radians(105), math.radians(75)
        )

        self.introduce(circle, left, right)
        self.run_group(constraint.Tangent(left, circle))
        self.run_group(constraint.Tangent(right, circle))


def concentric_common() -> tuple[sketch.Circle, sketch.Circle, sketch.Arc]:
    return (
        sketch.make_circle(mn.ORIGIN, 1.5),
        sketch.make_circle(vector.point_2d(-4, 0), 2),
        sketch.make_arc(vector.point_2d(3, 0), 3, math.radians(70), math.radians(-140)),
    )


class ConcentricEdgeScene(sketch_scene.Scene):
    def construct(self) -> None:
        circle, left, right = concentric_common()
        self.introduce(circle, left, right)
        # move to origin using shift
        self.run_group(
            sketch_utils.Click(left),
            sketch_utils.Click(circle),
            left.animate.shift(-left.get_center()),
        )
        self.run_group(
            sketch_utils.Click(right),
            sketch_utils.Click(circle),
            right.animate.shift(-right.get_center()),
        )


class ConcentricPointScene(sketch_scene.Scene):
    def construct(self) -> None:
        circle, left, right = concentric_common()
        self.introduce(circle, left, right)

        # move to origin using shift
        self.run_group(
            sketch_utils.Click(left.middle),
            sketch_utils.Click(circle),
            left.animate.shift(-left.get_center()),
        )

        self.run_group(
            sketch_utils.Click(right.middle),
            sketch_utils.Click(circle),
            right.animate.shift(-right.get_center()),
        )
