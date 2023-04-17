"""Defines entities which look like Onshape sketch entities.
"""
from __future__ import annotations
from multiprocessing import Value

from typing import Callable, Self, Any
from abc import ABC, abstractmethod
import enum

import manim as mn

from rc_lib.math_utils import vector, tangent
from rc_lib.style import color
from rc_lib.design import constraint


class SketchState(color.Color, enum.Enum):
    NORMAL = color.Palette.BLUE.value
    CONSTRAINED = color.Palette.BLACK.value


class Base(mn.VMobject, ABC):
    """An abstract base class for Sketch entities."""

    state = SketchState.NORMAL

    def _create_override(self) -> mn.Animation:
        raise NotImplementedError

    def _uncreate_override(self) -> mn.Animation:
        raise NotImplementedError

    # @abstractmethod
    # def set_state(self, state: SketchState) -> Self:
    #     self.state = state
    #     return self

    @abstractmethod
    def coincident_target(self, point: vector.Point2d) -> mn.Animation:
        raise NotImplementedError


class Point(mn.Dot, Base):
    """Defines a singlar Sketch vertex."""

    def __init__(self, dot: mn.Dot) -> None:
        super().__init__()
        self.become(dot)

    def follow(self, point_function: Callable[[], vector.Point2d]) -> Self:
        """Adds an updater function which causes this point to track the specified input."""

        def updater(mobject: mn.Mobject):
            mobject.move_to(point_function())

        self.add_updater(updater, call_updater=True)
        return self

    @mn.override_animation(constraint.Coincident)
    def _coincident_override(self, target: Base) -> mn.Animation:
        return self.animate.move_to(target.coincident_target(self.get_center())).build()

    def coincident_target(self, _: vector.Point2d) -> vector.Point2d:
        return self.get_center()

    @mn.override_animation(constraint.Midpoint)
    def _midpoint_override(self, *args: Point | Line) -> mn.Animation:
        if len(args) == 1:
            assert isinstance(args[0], Line)
            return self.animate.move_to(args[0].line.get_midpoint()).build()
        elif len(args) == 2:
            assert isinstance(args[0], Point) and isinstance(args[1], Point)
            return self.animate.move_to(
                (args[0].get_center() + args[1].get_center()) / 2
            ).build()
        else:
            raise ValueError("Expected a line or two points.")

    @mn.override_animation(constraint.Concentric)
    def _concentric_override(self, target: ArcBase) -> Any:
        return self._coincident_override(target.middle)

    @mn.override_animation(constraint.Vertical)
    def _vertical_override(self, target: Point) -> mn.Animation:
        return self._align_override(target, constraint.AlignType.VERTICAL)

    @mn.override_animation(constraint.Horizontal)
    def _horizontal_override(self, target: Point) -> mn.Animation:
        return self._align_override(target, constraint.AlignType.HORIZONTAL)

    def _align_override(
        self, target: Point, type: constraint.AlignType
    ) -> mn.Animation:
        if type == constraint.AlignType.VERTICAL:
            values = (target, self)
        else:
            values = (self, target)

        target_point = vector.point_2d(
            values[0].get_center()[0], values[1].get_center()[1]
        )
        return self.animate.move_to(target_point).build()


class Line(mn.VGroup, Base):
    """Defines a Sketch line segment vertices at each end."""

    def __init__(self, line: mn.Line) -> None:
        self.line = line
        self.start = _make_point(point=self.line.get_start())
        self.end = _make_point(point=self.line.get_end())
        super().__init__(self.start, self.end)

        def updater(mobject: mn.Mobject) -> None:
            mobject.put_start_and_end_on(self.start.get_center(), self.end.get_center())

        self.line.add_updater(updater)

    def get_start(self) -> vector.Point2d:
        return self.start.get_center()

    def get_end(self) -> vector.Point2d:
        return self.end.get_center()

    def get_length(self) -> float:
        return vector.norm(self.get_end() - self.get_start())

    def get_direction(self) -> vector.Direction2d:
        return vector.normalize(self.get_end() - self.get_start())

    def move_start(self, point: vector.Point2d) -> Self:
        self.start.move_to(point)
        return self

    def move_end(self, point: vector.Point2d) -> Self:
        self.end.move_to(point)
        return self

    @mn.override_animation(constraint.Vertical)
    def _vertical_override(self) -> mn.Animation:
        return self._align_override(constraint.AlignType.VERTICAL)

    @mn.override_animation(constraint.Horizontal)
    def _horizontal_override(self) -> mn.Animation:
        return self._align_override(constraint.AlignType.HORIZONTAL)

    def _align_override(self, type: constraint.AlignType) -> mn.Animation:
        curr_angle = self.line.get_angle()
        if type == constraint.AlignType.VERTICAL:
            if curr_angle >= 0 and curr_angle < mn.PI:
                angle = (mn.PI / 2) - curr_angle
            else:
                angle = -(mn.PI / 2) - curr_angle
        else:
            if curr_angle >= -mn.PI / 2 and curr_angle < mn.PI / 2:
                angle = -curr_angle
            else:
                angle = -mn.PI - curr_angle
        return mn.Rotate(self, angle=angle, about_point=self.line.get_midpoint())  # type: ignore

    @mn.override_animation(constraint.Equal)
    def _equal_override(self, target: Self) -> mn.Animation:
        midpoint = target.line.get_midpoint()
        offset = target.get_direction() * (self.get_length() / 2)
        return (
            target.animate.move_start(midpoint - offset)
            .move_end(midpoint + offset)
            .build()
        )

    def coincident_target(self, point: vector.Point2d) -> vector.Point2d:
        return self.line.get_projection(point)

    @mn.override_animation(constraint.Tangent)
    def _tangent_override(
        self, target: ArcBase, rotate: bool = False, reverse: bool = False
    ) -> Any:
        if not rotate:
            translation = self._get_line_translation(target)
            return self.animate.shift(translation)
        else:
            start = self._is_start_touching(target)
            close, far = (self.start, self.end) if start else (self.end, self.start)
            close_point, far_point = close.get_center(), far.get_center()

            if reverse:
                tangent_point = tangent.point_to_circle_tangent(
                    far_point, target.get_center(), target.radius
                )
            else:
                tangent_point = tangent.circle_to_point_tangent(
                    target.get_center(), target.radius, far_point
                )

            angle = vector.angle_between_points(
                close_point, tangent_point, target.get_center()
            )

            if reverse:
                angle *= -1

            return close.animate(
                path_arc=angle, path_arg_centers=[target.get_center()]
            ).move_to(tangent_point)

    def _get_line_translation(self, target: ArcBase) -> vector.Vector2d:
        projection: vector.Point2d = self.get_projection(target.get_center())  # type: ignore
        return vector.direction(projection, target.get_center()) * (
            vector.norm(target.get_center() - projection) - target.radius
        )

    def _is_start_touching(self, target: ArcBase) -> bool:
        """Returns whether the line is closer to the start or the end."""
        return vector.norm(self.get_start() - target.get_center()) < vector.norm(
            self.get_end() - target.get_center()
        )

    @mn.override_animation(mn.Create)
    def _create_override(self) -> mn.Animation:
        end = self.get_end()
        self.move_end(self.get_start() + vector.ZERO_LENGTH_VECTOR)
        return mn.Succession(
            constraint.Add(self.line),
            self.animate(introducer=True).move_end(end).build(),
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self) -> mn.Animation:
        start = self.get_start() + vector.ZERO_LENGTH_VECTOR
        # return self.animate(remover=True, introducer=True).move_end(start).build()
        return mn.Succession(
            self.animate(remover=True, introducer=True).move_end(start).build(),
            constraint.Remove(self.line),
        )


class ArcBase(mn.VGroup, Base, ABC):
    def __init__(self, arc: mn.Arc):
        self.arc = arc
        self.radius = self.arc.radius
        self.middle = _make_point(point=self.arc.arc_center)
        super().__init__(self.middle)

    def get_center(self) -> vector.Point2d:
        return self.middle.get_center()

    def set_radius(self, radius: float) -> Self:
        self.arc.scale(radius / self.radius)
        self.radius = radius
        return self

    @mn.override_animation(constraint.Equal)
    def _equal_override(self, target: Self) -> mn.Animation:
        return target.animate.set_radius(self.radius).build()

    def coincident_target(self, point: vector.Point2d) -> vector.Point2d:
        return self.get_center() + (
            vector.direction(self.get_center(), point) * self.radius
        )

    @mn.override_animation(constraint.Tangent)
    def _tangent_override(self, target: ArcBase) -> mn.Animation:
        translation = self._get_circle_translation(target)
        return self.middle.animate().shift(translation).build()

    def _get_circle_translation(self, target: ArcBase) -> vector.Vector2d:
        vec = target.get_center() - self.get_center()
        return vector.normalize(vec) * (vector.norm(vec) - self.radius - target.radius)

    @mn.override_animation(constraint.Concentric)
    def _concentric_override(self, target: Self | Point) -> mn.Animation:
        if isinstance(target, ArcBase):
            target = target.middle
        return self.middle._coincident_override(target)


class Circle(ArcBase):
    """Defines a Sketch circle with a vertex at its center."""

    def __init__(self, circle: mn.Circle):
        self.circle = circle
        super().__init__(self.circle)

        def updater(mobject: mn.Mobject) -> None:
            mobject.move_to(self.middle.get_center())

        self.arc.add_updater(updater)

    @mn.override_animation(mn.Create)
    def _create_override(self) -> mn.Animation:
        return mn.Succession(
            constraint.Add(self.middle),
            mn.GrowFromCenter(self.arc),
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self) -> mn.Animation:
        return mn.Succession(
            mn.GrowFromCenter(self.arc, reverse_rate_function=True, remover=True),
            constraint.Remove(self.middle),
        )


class Arc(ArcBase):
    """Defines a Sketch arc with vertices at each end and a vertex in the center."""

    def __init__(self, arc: mn.Arc) -> None:
        self.arc = arc
        self.start = _make_point().follow(self.arc.get_start)
        self.end = _make_point().follow(self.arc.get_end)
        super().__init__(self.arc)

        def updater(mobject: mn.Mobject) -> None:
            mobject.move_arc_center_to(self.middle.get_center())
            self.start.update()
            self.end.update()

        self.arc.add_updater(updater)

    @mn.override_animation(mn.Create)
    def _create_override(self) -> mn.Animation:
        return mn.Succession(
            constraint.Add(self.start, self.end, self.middle),
            mn.GrowFromCenter(self.arc),
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self) -> mn.Animation:
        return mn.Succession(
            mn.GrowFromCenter(self.arc, reverse_rate_function=True, remover=True),
            constraint.Remove(self.start, self.end, self.middle),
        )


def _make_point(point: vector.Point2d = mn.ORIGIN) -> Point:
    return Point(mn.Dot(point, color=SketchState.NORMAL))


def make_line(start_point: vector.Point2d, end_point: vector.Point2d) -> Line:
    return Line(mn.Line(start_point, end_point, color=SketchState.NORMAL))


def make_circle(center: vector.Point2d, radius: float) -> Circle:
    return Circle(mn.Circle(radius, color=SketchState.NORMAL, arc_center=center))


def make_arc(
    center: vector.Point2d, radius: float, start_angle: float, angle: float
) -> Arc:
    return Arc(
        mn.Arc(
            radius,
            start_angle=start_angle,  # type: ignore
            angle=angle,
            color=SketchState.NORMAL,
            arc_center=center,
        )
    )
