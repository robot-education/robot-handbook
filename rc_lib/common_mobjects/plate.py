from manim import *
from typing import List, Self
from rc_lib import math_types as T

from rc_lib import style
from rc_lib.math_utils import tangent

__all__ = ["Plate", "PlateCircle"]


class PlateCircle(VGroup):
    def __init__(self, inner_circle: Circle, outer_circle: Circle) -> None:
        super().__init__(inner_circle, outer_circle)
        self._inner_circle = inner_circle
        self._outer_circle = outer_circle

    @staticmethod
    def tangent_points(start, end) -> List[T.Point2d]:
        return tangent.circle_to_circle_tangent(
            start.center(), start.outer_radius(), end.center(), end.outer_radius()
        )

    @staticmethod
    def tangent_line(start, end, color: style.Color = style.DEFAULT_COLOR) -> Line:
        return Line(*PlateCircle.tangent_points(start, end), color=color)

    def inner_circle(self) -> Self:
        return self._inner_circle

    def outer_circle(self) -> Self:
        return self._outer_circle

    def center(self) -> T.Point2d:
        return self.inner_circle().get_center()

    def inner_radius(self) -> float:
        return self.inner_circle().width / 2

    def outer_radius(self) -> float:
        return self.outer_circle().width / 2

    def draw_inner_circle(self) -> Animation:
        return GrowFromCenter(self.inner_circle())

    def draw_outer_circle(self) -> Animation:
        return GrowFromCenter(self.outer_circle())


class PlateCircleFactory:
    def __init__(self) -> None:
        self._inner_color = style.DEFAULT_COLOR
        self._outer_color = style.DEFAULT_COLOR

    def set_inner_color(self, color: style.Color) -> Self:
        self._inner_color = color
        return self

    def set_outer_color(self, color: style.Color) -> Self:
        self._outer_color = color
        return self

    def make_generator(self, radius: float, offset: float):
        """
        Returns a generator function which may be used to create points of the given size.
        The generator function takes a location as an argument.
        """

        def generator(location: T.Point2d) -> PlateCircle:
            return PlateCircle(
                Circle(radius, color=self._inner_color),
                Circle(radius + offset, color=self._outer_color),
            ).move_to(location)

        return generator

    def make(self, radius: float, offset: float, location: T.Point2d) -> PlateCircle:
        # get a generator and immediately pass it location
        return self.make_generator(radius, offset)(location)


class PlateGroup(VGroup):
    def __init__(
        self,
        entities: List[PlateCircle],
        boundary_order: List[int],
        boundary_color: style.Color = style.DEFAULT_COLOR,
    ) -> None:
        self._entities = entities
        self._boundary = [self._entities[i] for i in boundary_order]
        self._boundary_lines = self._make_boundary_lines(boundary_color)
        super().__init__(*[*self._entities, *self._boundary_lines])

    def _make_boundary_lines(self, color: style.Color) -> List[Line]:
        return [
            PlateCircle.tangent_line(self._boundary[i - 1], curr, color=color)
            for i, curr in enumerate(self._boundary)
        ]

    def draw_inner_circles(self, lag_ratio: float = 1, **kwargs) -> Animation:
        return AnimationGroup(
            *[x.draw_inner_circle() for x in self._entities],
            lag_ratio=lag_ratio,
            **kwargs
        )

    def draw_outer_circles(self, lag_ratio: float = 1, **kwargs) -> Animation:
        return AnimationGroup(
            *[x.draw_outer_circle() for x in self._entities],
            lag_ratio=lag_ratio,
            **kwargs
        )

    def draw_boundary(self, lag_ratio: float = 1, **kwargs) -> Animation:
        return AnimationGroup(
            *[Create(x) for x in self._boundary_lines], lag_ratio=lag_ratio, **kwargs
        )
