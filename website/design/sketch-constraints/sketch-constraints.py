"""Animations showcasing various Onshape sketch constraints."""

import math
from typing import Iterable

import manim as mn
from design import scene
from rc_lib.style import color
from rc_lib.math_utils import vector
from rc_lib.design import sketch, sketch_utils

sketch_color = color.Palette.BLUE
sketch_factory: sketch.SketchFactory = sketch.SketchFactory().set_color(sketch_color)


def coincident_common_mobjects() -> (
    tuple[sketch.SketchCircle, sketch.SketchLine, sketch.SketchLine]
):
    """Returns mobjects common to coincident."""
    return (
        sketch_factory.make_circle(vector.point_2d(-4.5, 0), 1.5),
        sketch_factory.make_line(
            vector.point_2d(5.25, 4 / 2), vector.point_2d(5.25, -4 / 2)
        ),
        sketch_factory.make_line(
            vector.point_2d(-1.75, 0.75), vector.point_2d(4.25, -1)
        ),
    )


class CoincidentPointsScene(scene.SketchScene):
    def construct(self) -> None:
        circle, line, move_line = coincident_common_mobjects()
        self.introduce(circle, line, move_line)

        self.run_group(
            sketch_utils.Click(move_line.start_vertex),
            sketch_utils.Click(circle.center_vertex),
            move_line.animate.move_start(circle.get_center()),
        )

        self.run_group(
            sketch_utils.Click(move_line.end_vertex),
            sketch_utils.Click(line.end_vertex),
            move_line.animate.move_end(line.get_end()),
        )


class CoincidentPointLineScene(scene.SketchScene):
    def construct(self) -> None:
        circle, line, move_line = coincident_common_mobjects()
        self.introduce(circle, line, move_line)

        point = (
            circle.get_center()
            + vector.direction(circle.get_center(), move_line.get_start())
            * circle.get_radius()
        )

        self.run_group(
            sketch_utils.Click(move_line.start_vertex),
            sketch_utils.Click(circle.circle),
            move_line.animate.move_start(point),
        )

        point = vector.project_to_line(
            move_line.get_end(),
            line.get_start(),
            line.get_end(),
        )

        self.run_group(
            sketch_utils.Click(move_line.end_vertex),
            sketch_utils.Click(line.line),
            move_line.animate.move_end(point),
        )


class CoincidentLineScene(scene.SketchScene):
    def construct(self) -> None:
        start_point = vector.point_2d(-5.75, 2.5)
        middle_point = vector.point_2d(-1.15, 0.5)  # closest to the middle
        fixed_line = sketch_factory.make_line(start_point, middle_point)

        slope = fixed_line.get_direction()
        angle = math.radians(38)
        start_line = sketch_factory.make_line(
            middle_point + mn.rotate_vector(slope * 2, angle),
            middle_point + mn.rotate_vector(slope * 7.5, angle),
        )

        self.introduce(fixed_line, start_line)
        self.run_group(
            sketch_utils.Click(start_line.line),
            sketch_utils.Click(fixed_line.line),
            mn.Rotate(
                start_line,
                angle=-angle,
                about_point=fixed_line.get_end(),
            ),
        )


def vh_common_line() -> tuple[sketch.SketchLine, float]:
    return (
        sketch_factory.make_line(
            vector.point_2d(-2.3, -2.3), vector.point_2d(2.3, 2.3)
        ),
        math.radians(45),
    )


class VerticalLineScene(scene.SketchScene):
    def construct(self) -> None:
        start_line, angle = vh_common_line()
        angle = math.radians(90) - angle

        self.introduce(start_line)

        self.run_group(
            sketch_utils.Click(start_line.line),
            mn.Rotate(start_line, angle=angle),
        )


class HorizontalLineScene(scene.SketchScene):
    def construct(self) -> None:
        start_line, angle = vh_common_line()
        angle = -angle
        self.introduce(start_line)

        self.run_group(
            sketch_utils.Click(start_line.line),
            mn.Rotate(start_line, angle=angle),
        )


class VerticalPointsScene(scene.SketchScene):
    def construct(self) -> None:
        circle = sketch_factory.make_circle(vector.point_2d(-4, 1.5), 1.5)
        line = sketch_factory.make_line(
            vector.point_2d(0, 2.5), vector.point_2d(5.5, 1.5)
        )
        move_line = sketch_factory.make_line(
            vector.point_2d(-5.5, -2.5), vector.point_2d(3.5, -1.5)
        )

        self.introduce(circle, line, move_line)

        self.run_group(
            sketch_utils.Click(move_line.start_vertex),
            sketch_utils.Click(circle.center_vertex),
            move_line.animate.move_start(
                vector.point_2d(circle.get_center()[0], move_line.get_start()[1])
            ),
        )

        self.run_group(
            sketch_utils.Click(move_line.end_vertex),
            sketch_utils.Click(line.end_vertex),
            move_line.animate.move_end(
                vector.point_2d(line.get_end()[0], move_line.get_end()[1])
            ),
        )


class HorizontalPointsScene(scene.SketchScene):
    def construct(self) -> None:
        circle = sketch_factory.make_circle(vector.point_2d(-3.5, 1.5), 1.5)
        line = sketch_factory.make_line(
            vector.point_2d(-5, -0.75), vector.point_2d(-1, -2.5)
        )
        move_line = sketch_factory.make_line(
            vector.point_2d(2, -1.5), vector.point_2d(4.5, 3)
        )
        self.introduce(circle, line, move_line)

        self.run_group(
            sketch_utils.Click(move_line.start_vertex),
            sketch_utils.Click(line.end_vertex),
            move_line.animate.move_start(
                vector.point_2d(move_line.get_start()[0], line.get_end()[1])
            ),
        )

        self.run_group(
            sketch_utils.Click(move_line.end_vertex),
            sketch_utils.Click(circle.center_vertex),
            move_line.animate.move_end(
                vector.point_2d(
                    move_line.get_end()[0],
                    circle.get_center()[1],
                )
            ),
        )


class ParallelScene(scene.SketchScene):
    def construct(self) -> None:
        line = sketch_factory.make_line(
            vector.point_2d(-6, -3), vector.point_2d(6, 0.5)
        )
        direction = line.get_direction()

        end_point = vector.point_2d(5, 3)
        start_point = end_point - direction * 10.5
        angle = math.radians(16.26)
        start_line = sketch_factory.make_line(start_point, end_point).rotate(
            -angle, about_point=line.line.get_midpoint()  # type: ignore
        )

        self.introduce(line, start_line)
        self.run_group(
            sketch_utils.Click(start_line.line),
            sketch_utils.Click(line.line),
            start_line.animate.rotate(angle, about_point=line.line.get_midpoint()),
        )


class PerpendicularScene(scene.SketchScene):
    def construct(self) -> None:
        line = sketch_factory.make_line(
            vector.point_2d(-5, -2.75), vector.point_2d(5.5, 0.5)
        )
        direction = line.get_direction()
        rotation_point = line.get_start() + direction * 2
        perpendicular_direction = vector.direction_2d(-direction[1], direction[0])
        end_line = sketch_factory.make_line(
            rotation_point + perpendicular_direction * 1,
            rotation_point + perpendicular_direction * 5.25,
        )
        angle = math.radians(45)

        # move to start position
        start_line = end_line.rotate(-angle, about_point=rotation_point)

        self.introduce(start_line, line)
        self.run_group(
            sketch_utils.Click(start_line.line),
            sketch_utils.Click(line.line),
            # rotate to end position
            mn.Rotate(start_line, angle, about_point=rotation_point),
        )


def centered_line(line: sketch.SketchLine, length: float) -> sketch.SketchLine:
    """Returns a line centered on the given line with the specified length."""
    center = line.line.get_midpoint()
    offset = line.get_direction() * length / 2
    return sketch_factory.make_line(center - offset, center + offset)


class EqualLineScene(scene.SketchScene):
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
            sketch_utils.Click(base.line),
            sketch_utils.Click(first.line),
            mn.Transform(first, centered_line(first, length)),
        )

        self.run_group(
            sketch_utils.Click(base.line),
            sketch_utils.Click(second.line),
            mn.Transform(second, centered_line(second, length)),
        )


class EqualCircleScene(scene.SketchScene):
    def construct(self) -> None:
        base = sketch_factory.make_circle(vector.point_2d(0, -1.5), 1.5)
        circle = sketch_factory.make_circle(vector.point_2d(-3.5, 1), 2)
        arc = sketch_factory.make_arc(
            vector.point_2d(3.5, 1), 2, math.radians(90), math.radians(-225)
        )

        self.introduce(base, arc, circle)
        self.run_group(
            sketch_utils.Click(base.circle),
            sketch_utils.Click(circle.circle),
            circle.animate.set_radius(1.5),
        )
        self.run_group(
            sketch_utils.Click(base.circle),
            sketch_utils.Click(arc.arc),
            arc.animate.set_radius(1.5),
        )


class MidpointLineScene(scene.SketchScene):
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
            sketch_utils.Click(middle.start_vertex),
            sketch_utils.Click(top.line),
            middle.animate.move_start(top.line.get_midpoint()),
        )
        self.run_group(
            sketch_utils.Click(middle.end_vertex),
            sketch_utils.Click(bottom.line),
            middle.animate.move_end(bottom.line.get_midpoint()),
        )


class MidpointPointScene(scene.SketchScene):
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
            sketch_utils.Click(line.start_vertex),
            sketch_utils.Click(first_line.start_vertex),
            sketch_utils.Click(circle.center_vertex),
            first_line.animate.move_start((line.get_start() + circle.get_center()) / 2),
        )
        self.run_group(
            sketch_utils.Click(line.end_vertex),
            sketch_utils.Click(first_line.end_vertex),
            sketch_utils.Click(circle.center_vertex),
            first_line.animate.move_end((line.get_end() + circle.get_center()) / 2),
        )

        self.introduce(second_line)
        self.run_group(
            sketch_utils.Click(line.start_vertex),
            sketch_utils.Click(second_line.start_vertex),
            sketch_utils.Click(line.end_vertex),
            second_line.animate.move_start(line.line.get_midpoint()),
        )
        self.run_group(
            sketch_utils.Click(first_line.start_vertex),
            sketch_utils.Click(second_line.end_vertex),
            sketch_utils.Click(first_line.end_vertex),
            second_line.animate.move_end(first_line.line.get_midpoint()),
        )


def get_translation(
    line: sketch.SketchLine, circle: sketch.SketchCircle
) -> sketch.SketchLine:
    projection: vector.Point2d = line.line.get_projection(circle.get_center())
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
        sketch_utils.Click(line.line),
        sketch_utils.Click(circle.circle),
        mn.Transform(line, get_translation(line, circle)),
    )


class TangentLineScene(scene.SketchScene):
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
    base: sketch.SketchArcBase, target: sketch.SketchCircle
) -> vector.Vector2d:
    vec = target.get_center() - base.get_center()
    return vector.normalize(vec) * (
        vector.norm(vec) - base.get_radius() - target.get_radius()
    )


def tangent_circle_transform(
    base: sketch.SketchArcBase, target: sketch.SketchCircle
) -> Iterable[mn.Animation]:
    return (
        sketch_utils.Click(base._arc),
        sketch_utils.Click(target.circle),
        mn.prepare_animation(base.animate.shift(get_circle_translation(base, target))),
    )


class TangentCircleScene(scene.SketchScene):
    def construct(self) -> None:
        circle = sketch_factory.make_circle(mn.ORIGIN, 1.5)
        left = sketch_factory.make_circle(vector.point_2d(-4, 1), 1.5)
        right = sketch_factory.make_arc(
            vector.point_2d(6, -1.125), 3.5, math.radians(105), math.radians(75)
        )

        self.introduce(circle, left, right)
        self.run_group(*tangent_circle_transform(left, circle))
        self.run_group(*tangent_circle_transform(right, circle))


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


class ConcentricEdgeScene(scene.SketchScene):
    def construct(self) -> None:
        circle, left, right = concentric_common()
        self.introduce(circle, left, right)
        # move to origin using shift
        self.run_group(
            sketch_utils.Click(left.circle),
            sketch_utils.Click(circle.circle),
            left.animate.shift(-left.get_center()),
        )
        self.run_group(
            sketch_utils.Click(right.arc),
            sketch_utils.Click(circle.circle),
            right.animate.shift(-right.get_center()),
        )


class ConcentricPointScene(scene.SketchScene):
    def construct(self) -> None:
        circle, left, right = concentric_common()
        self.introduce(circle, left, right)

        # move to origin using shift
        self.run_group(
            sketch_utils.Click(left.center_vertex),
            sketch_utils.Click(circle.circle),
            left.animate.shift(-left.get_center()),
        )

        self.run_group(
            sketch_utils.Click(right.center_vertex),
            sketch_utils.Click(circle.circle),
            right.animate.shift(-right.get_center()),
        )
