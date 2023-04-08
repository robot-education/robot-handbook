"""Defines entities which look like Onshape sketch entities.
"""
from __future__ import annotations

from typing import Callable, Self
from abc import ABC, abstractmethod
import enum

import manim as mn

from rc_lib.math_utils import vector
from rc_lib.style import color, animation
from rc_lib.design import constraint


# def get_key(base: Base, key: str | None) -> Base:
#     match key:
#         case None:
#             return base
#         case "middle":
#             throw_if_not(base, Circle | Arc)
#         case "start":
#             throw_if_not(base, Line | Arc)
#         case "end":
#             throw_if_not(base, Line | Arc)
#         case _:
#             raise_key_error()

#     return getattr(base, key)


# def throw_if(base: Base, type: type[Base] | UnionType) -> None:
#     if isinstance(base, type):
#         raise_key_error()


# def throw_if_not(base: Base, type: type[Base] | UnionType) -> None:
#     if not isinstance(base, type):
#         raise_key_error()


# def raise_key_error() -> NoReturn:
#     raise KeyError("A key passed to constraint is invalid")


class SketchState(color.Color, enum.Enum):
    NORMAL = color.Palette.BLUE.value
    CONSTRAINED = color.Palette.BLACK.value
    ERROR = color.Palette.RED.value


class Base(mn.VMobject, ABC):
    """An abstract base class for Sketch entities."""

    state = SketchState.NORMAL

    @abstractmethod
    def _create_override(self) -> mn.Animation:
        raise NotImplementedError

    @abstractmethod
    def _uncreate_override(self) -> mn.Animation:
        raise NotImplementedError

    @abstractmethod
    def coincident_target(self, point: vector.Point2d) -> mn.Animation:
        raise NotImplementedError


class ArcBase(Base, ABC):
    @mn.override_animation(constraint.Equal)
    def _equal_override(self, target: Self) -> mn.Animation:
        return target.animate.set_radius(self.radius)  # type: ignore

    def coincident_target(self, point: vector.Point2d) -> vector.Point2d:
        return self.get_center() + (
            vector.direction(self.get_center(), point) * self.radius
        )


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

    def coincident_target(self, _: vector.Point2d) -> vector.Point2d:
        return self.get_center()

    @mn.override_animation(mn.Create)
    def _create_override(self) -> mn.Animation:
        return mn.Animation(self, introducer=True, run_time=0)

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self) -> mn.Animation:
        return mn.Animation(self, introducer=True, remover=True, run_time=0)


class Line(mn.Line, Base):
    """Defines a Sketch line segment vertices at each end."""

    def __init__(self, line: mn.Line) -> None:
        super().__init__()
        self.become(line)

        self.start = _make_point().follow(self.get_start)
        self.end = _make_point().follow(self.get_end)

    def get_length(self) -> float:
        return vector.norm(self.get_end() - self.get_start())

    def get_direction(self) -> vector.Direction2d:
        return vector.normalize(self.get_end() - self.get_start())

    def move_start(self, point: vector.Point2d) -> Self:
        return self.put_start_and_end_on(point, self.get_end())  # type: ignore

    def move_end(self, point: vector.Point2d) -> Self:
        return self.put_start_and_end_on(self.get_start(), point)  # type: ignore

    @mn.override_animation(constraint.Equal)
    def _equal_override(self, target: Self) -> mn.Animation:
        midpoint = target.get_midpoint()
        offset = target.get_direction() * (self.get_length() / 2)
        animation = target.animate.put_start_and_end_on(
            midpoint - offset, midpoint + offset
        )
        return constraint.make(animation, self, target)

    @mn.override_animation(constraint.Coincident)
    def _coincident_override(self, target: Point, *, base_key: str) -> mn.Animation:
        animation = self.animate
        if base_key == "start":
            animation.move_start(target.coincident_target(self.get_start()))
        elif base_key == "end":
            animation.move_end(target.coincident_target(self.get_end()))
        else:
            raise KeyError("Expected start or end")
        return constraint.make(animation, getattr(self, base_key), target)

    def coincident_target(self, point: vector.Point2d) -> vector.Point2d:
        return self.get_projection(point)

    @mn.override_animation(mn.Create)
    def _create_override(self) -> mn.Animation:
        return mn.Succession(
            mn.Create(self.start),
            mn.Create(self.end),
            mn.Create(self, use_override=False, suspend_mobject_updating=False),
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self) -> mn.Animation:
        return mn.Succession(
            mn.Uncreate(self, use_override=False, suspend_mobject_updating=False),
            mn.Uncreate(self.start),
            mn.Uncreate(self.end),
        )


class Circle(mn.Circle, ArcBase):
    """Defines a Sketch circle with a vertex at its center."""

    def __init__(self, circle: mn.Circle):
        super().__init__()
        self.become(circle)
        self.radius = circle.radius

        # center is already used
        self.middle = _make_point().follow(self.get_center)

    def set_radius(self, radius: float) -> Self:
        self.scale(radius / self.radius)
        self.radius = radius
        return self

    @mn.override_animation(mn.Create)
    def _create_override(self) -> mn.Animation:
        return mn.Succession(mn.Create(self.middle), mn.GrowFromCenter(self))

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self) -> mn.Animation:
        return mn.Succession(animation.ShrinkToCenter(self), mn.Uncreate(self.middle))


class Arc(mn.Arc, ArcBase):
    """Defines a Sketch arc with vertices at each end and a vertex in the center."""

    def __init__(self, arc: mn.Arc) -> None:
        super().__init__()
        self.become(arc)
        self.radius = arc.radius

        self.start = _make_point().follow(self.get_start)
        self.end = _make_point().follow(self.get_end)
        # center is already used
        self.middle = _make_point().follow(self.get_arc_center)

    def get_center(self) -> vector.Point2d:
        return self.middle.get_center()

    def set_radius(self, radius: float) -> Self:
        self.scale(radius / self.radius)
        self.radius = radius
        return self

    @mn.override_animation(mn.Create)
    def _create_override(self) -> mn.Animation:
        return mn.Succession(
            mn.Create(self.start),
            mn.Create(self.end),
            mn.Create(self.middle),
            mn.GrowFromCenter(self),
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self) -> mn.Animation:
        return mn.Succession(
            animation.ShrinkToCenter(self),
            mn.Uncreate(self.start),
            mn.Uncreate(self.end),
            mn.Uncreate(self.middle),
        )


def _make_point(point: vector.Point2d = mn.ORIGIN) -> Point:
    return Point(mn.Dot(point, color=SketchState.NORMAL))


def make_line(start_point: vector.Point2d, end_point: vector.Point2d) -> Line:
    return Line(mn.Line(start_point, end_point, color=SketchState.NORMAL))


def make_circle(center: vector.Point2d, radius: float) -> Circle:
    return Circle(mn.Circle(radius, color=SketchState.NORMAL).move_to(center))


def make_arc(
    center: vector.Point2d, radius: float, start_angle: float, angle: float
) -> Arc:
    return Arc(
        # start_angle is typed incorrectly as int
        mn.Arc(radius, start_angle=start_angle, angle=angle, color=SketchState.NORMAL, arc_center=center)  # type: ignore
    )
