import manim as mn
from typing import Callable, Self

from rc_lib.style import color
from rc_lib.common_mobjects import sketch
from rc_lib.math_utils import tangent, vector


class PlateCircle(mn.VGroup):
    def __init__(self, inner_circle: mn.Circle, outer_circle: mn.Circle) -> None:
        super().__init__(inner_circle, outer_circle)
        self.inner_circle: mn.Circle = inner_circle
        self.outer_circle: mn.Circle = outer_circle

    def center(self) -> vector.Point2d:
        return self.get_center()

    def inner_radius(self) -> float:
        return self.inner_circle.width / 2

    def outer_radius(self) -> float:
        return self.outer_circle.width / 2


def plate_circle_tangent_points(
    start: PlateCircle, end: PlateCircle
) -> tuple[vector.Point2d, vector.Point2d]:
    return tangent.circle_to_circle_tangent(
        start.center(), start.outer_radius(), end.center(), end.outer_radius()
    )


def plate_circle_tangent_line(
    start: PlateCircle, end: PlateCircle, color: color.Color
) -> mn.Line:
    return mn.Line(*plate_circle_tangent_points(start, end), color=color)
    # return sketch_factory.make_line(*plate_circle_tangent_points(start, end))


PlateCircleGenerator = Callable[[vector.Point2d], PlateCircle]


class PlateCircleFactory:
    def __init__(self) -> None:
        self._inner_color: color.Color = color.FOREGROUND
        self._outer_color: color.Color = color.FOREGROUND

    def set_inner_color(self, color: color.Color) -> Self:
        self._inner_color = color
        return self

    def set_outer_color(self, color: color.Color) -> Self:
        self._outer_color = color
        return self

    def make_generator(self, radius: float, offset: float) -> PlateCircleGenerator:
        """
        Returns a generator function which may be used to create points of the given size.
        The generator function takes a location as an argument.
        """

        def generator(point: vector.Point2d) -> PlateCircle:
            return PlateCircle(
                mn.Circle(radius, color=self._inner_color),
                mn.Circle(radius + offset, color=self._outer_color),
            ).move_to(point)

        return generator

    def make(
        self, radius: float, offset: float, location: vector.Point2d
    ) -> PlateCircle:
        # get a generator and immediately pass it location
        return self.make_generator(radius, offset)(location)


class PlateGroup(mn.VGroup):
    def __init__(
        self,
        entities: list[PlateCircle],
        boundary_order: list[int],
        boundary_color: color.Color = color.FOREGROUND,
    ) -> None:
        self._entities: list[PlateCircle] = entities
        self._boundary: list[PlateCircle] = [self._entities[i] for i in boundary_order]
        self._boundary_lines: list[mn.Line] = self._make_boundary_lines(boundary_color)
        super().__init__(*[*self._entities, *self._boundary_lines])

    def _make_boundary_lines(self, color: color.Color) -> list[mn.Line]:
        return [
            plate_circle_tangent_line(self._boundary[i - 1], curr, color)
            for i, curr in enumerate(self._boundary)
        ]

    def draw_inner_circles(self) -> mn.Animation:
        return mn.Succession(
            *[mn.GrowFromCenter(x.inner_circle) for x in self._entities], lag_ratio=0.75
        )

    def draw_outer_circles(self) -> mn.Animation:
        return mn.Succession(
            *[mn.GrowFromCenter(x.outer_circle) for x in self._entities], lag_ratio=0.75
        )

    def draw_boundary(self) -> mn.Animation:
        return mn.Succession(
            *[mn.Create(line) for line in self._boundary_lines], lag_ratio=1
        )
