from __future__ import annotations

from manim import *
from typing import List, Optional
from rc_lib.math_utils import tangent

__all__ = ["Plate", "PlateCircle"]


class PlateCircle(VGroup):
    def __init__(self, inner_circle: Circle, outer_circle: Circle) -> None:
        super().__init__(inner_circle, outer_circle)
        self._inner_circle = inner_circle
        self._outer_circle = outer_circle

    @staticmethod
    def make(radius: float, offset: float) -> PlateCircle:
        return PlateCircle(Circle(radius), Circle(radius + offset))

    @staticmethod
    def tangent_points(start, end) -> List[np.ndarray]:
        return tangent.circle_to_circle_tangent(start.center(), start.outer_radius(), end.center(), end.outer_radius())

    @staticmethod
    def tangent_line(start, end) -> List[np.ndarray]:
        return Line(*PlateCircle.tangent_points(start, end))

    def inner_circle(self):
        return self._inner_circle

    def outer_circle(self):
        return self._outer_circle

    def center(self) -> np.ndarray:
        return self.inner_circle().get_center()

    def inner_radius(self) -> float:
        return self.inner_circle().width / 2

    def outer_radius(self) -> float:
        return self.outer_circle().width / 2

    def copy(self, center: np.ndarray) -> PlateCircle:
        return super().copy().move_to(center)

    def draw_inner_circle(self) -> Animation:
        return GrowFromCenter(self.inner_circle())

    def draw_outer_circle(self) -> Animation:
        return GrowFromCenter(self.outer_circle())


class PlateGroup(VGroup):
    def __init__(self, points: List[PlateCircle], boundary_order: List[int]) -> None:
        self._points = points
        self._boundary = [points[i] for i in boundary_order]
        # self._boundary = list(filter(lambda p: p not in self._inside, self._points))
        self._boundary_segments = self._make_boundary_segments()

        super().__init__(*[*self._points, *self._boundary_segments])

    def _make_boundary_segments(self) -> List[Line]:
        return [PlateCircle.tangent_line(self._boundary[i - 1], self._boundary[i]) for i in range(len(self._boundary))]

    def draw_inner_circles(self, lag_ratio: Optional[float] = 0.75, **kwargs) -> Animation:
        return AnimationGroup(*[x.draw_inner_circle() for x in self._points], lag_ratio=lag_ratio, **kwargs)

    def draw_outer_circles(self, lag_ratio: Optional[float] = 0.75, **kwargs) -> Animation:
        return AnimationGroup(*[x.draw_outer_circle() for x in self._points], lag_ratio=lag_ratio, **kwargs)

    def draw_boundary(self, lag_ratio: Optional[float] = 0.75, **kwargs) -> Animation:
        return AnimationGroup(*[Create(x) for x in self._boundary_segments], lag_ratio=lag_ratio, **kwargs)
