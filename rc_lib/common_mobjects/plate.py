import manim as mn
from typing import Callable, List, Self, Tuple

from rc_lib import style
from rc_lib.style import color
from rc_lib.math_utils import tangent, vector


class PlateCircle(mn.VGroup):
    def __init__(self, inner_circle: mn.Circle, outer_circle: mn.Circle) -> None:
        super().__init__(inner_circle, outer_circle)
        self.inner_circle: mn.Circle = inner_circle
        self.outer_circle: mn.Circle = outer_circle

    def center(self) -> vector.Point2d:
        return self.inner_circle.get_center()

    def inner_radius(self) -> float:
        return self.inner_circle.width / 2

    def outer_radius(self) -> float:
        return self.outer_circle.width / 2


def plate_circle_tangent_points(
    start: PlateCircle, end: PlateCircle
) -> Tuple[vector.Point2d, vector.Point2d]:
    return tangent.circle_to_circle_tangent(
        start.center(), start.outer_radius(), end.center(), end.outer_radius()
    )


def plate_circle_tangent_line(
    start: PlateCircle, end: PlateCircle, color: style.Color = style.DEFAULT_COLOR
) -> mn.Line:
    return mn.Line(*plate_circle_tangent_points(start, end), color=color)


class PlateCircleFactory:
    def __init__(self) -> None:
        self._inner_color: style.Color = style.DEFAULT_COLOR
        self._outer_color: style.Color = style.DEFAULT_COLOR

    def set_inner_color(self, color: style.Color) -> Self:
        self._inner_color: style.Color = color
        return self

    def set_outer_color(self, color: style.Color) -> Self:
        self._outer_color: style.Color = color
        return self

    def make_generator(
        self, radius: float, offset: float
    ) -> Callable[[vector.Point2d], PlateCircle]:
        """
        Returns a generator function which may be used to create points of the given size.
        The generator function takes a location as an argument.
        """

        def generator(location: vector.Point2d) -> PlateCircle:
            return PlateCircle(
                mn.Circle(radius, color=self._inner_color),
                mn.Circle(radius + offset, color=self._outer_color),
            ).move_to(location)

        return generator

    def make(
        self, radius: float, offset: float, location: vector.Point2d
    ) -> PlateCircle:
        # get a generator and immediately pass it location
        return self.make_generator(radius, offset)(location)


class PlateGroup(mn.VGroup):
    def __init__(
        self,
        entities: List[PlateCircle],
        boundary_order: List[int],
        boundary_color: color.Color = color.FOREGROUND,
    ) -> None:
        self._entities: List[PlateCircle] = entities
        self._boundary: List[PlateCircle] = [self._entities[i] for i in boundary_order]
        self._boundary_lines: List[mn.Line] = self._make_boundary_lines(boundary_color)
        super().__init__(*[*self._entities, *self._boundary_lines])

    def _make_boundary_lines(self, color: style.Color) -> List[mn.Line]:
        return [
            plate_circle_tangent_line(self._boundary[i - 1], curr, color=color)
            for i, curr in enumerate(self._boundary)
        ]

    def draw_inner_circles(self, lag_ratio: float = 1, **kwargs) -> mn.Animation:
        return mn.AnimationGroup(
            *[mn.GrowFromCenter(x.inner_circle) for x in self._entities],
            lag_ratio=lag_ratio,
            **kwargs
        )

    def draw_outer_circles(self, lag_ratio: float = 1, **kwargs) -> mn.Animation:
        return mn.AnimationGroup(
            *[mn.GrowFromCenter(x.outer_circle) for x in self._entities],
            lag_ratio=lag_ratio,
            **kwargs
        )

    def draw_boundary(self, lag_ratio: float = 1, **kwargs) -> mn.Animation:
        return mn.AnimationGroup(
            *[mn.Create(x) for x in self._boundary_lines], lag_ratio=lag_ratio, **kwargs
        )
