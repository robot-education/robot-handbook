"""
A module defining sketcher-like entities.
The following convention is adopted - a vertex is a physical entity (usually a dot), 
whereas a point is a piece of data.
"""
from typing import cast, Sequence, Self
from abc import ABC, abstractmethod
import enum
import math

import manim as mn

from rc_lib.math_utils import vector
from rc_lib.style import color
from rc_lib.style import animation

z_index = 100


def click(mobject: mn.VMobject) -> mn.Animation:
    """
    Represents clicking a mobject by setting its stroke width and playing an animation transforming it.
    """
    global z_index
    target = mobject.copy().set_stroke(width=4 * 3.5).set_color(color.Palette.YELLOW)  # type: ignore
    mobject.set_z_index(
        z_index
    )  # set z_index to make highlight go over the top (a bit suss)
    z_index += 1
    return mn.Transform(mobject, target, rate_func=mn.there_and_back, run_time=0.75)


class Sketch(mn.VGroup, ABC):
    """
    An abstract base class for Sketch entities.
    """

    @abstractmethod
    def create(self) -> mn.Animation:
        raise NotImplementedError

    @abstractmethod
    def uncreate(self) -> mn.Animation:
        raise NotImplementedError


class SketchCircle(Sketch):
    def __init__(self, circle: mn.Circle, vertex: mn.Dot) -> None:
        self.circle = circle
        self.vertex = vertex
        super().__init__(self.circle, self.vertex)

    def get_radius(self) -> float:
        return self.circle.radius

    def click_center(self) -> mn.Animation:
        return click(self.vertex)

    def click_circle(self) -> mn.Animation:
        return click(self.circle)

    def create(self) -> mn.Animation:
        return mn.Succession(
            mn.Create(self.vertex, run_time=0), mn.GrowFromCenter(self.circle)
        )

    def uncreate(self) -> mn.Animation:
        return mn.Succession(
            animation.ShrinkToCenter(self.circle),
            mn.Uncreate(self.vertex, run_time=0),
        )


class SketchPoint(Sketch):
    def __init__(self, vertex: mn.Dot) -> None:
        self.vertex = vertex
        super().__init__(self.get_point)

    def get_point(self) -> vector.Vector2d:
        return self.get_center()

    def click(self) -> mn.Animation:
        return click(self.vertex)

    def create(self) -> mn.Animation:
        return mn.Create(self)

    def uncreate(self) -> mn.Animation:
        return mn.Uncreate(self)


class LineEnd(enum.IntEnum):
    START = 0
    END = 1


class SketchLine(Sketch):
    def __init__(self, line: mn.Line, start_vertex: mn.Dot, end_vertex: mn.Dot) -> None:
        self.line = line
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        super().__init__(self.line, self.start_vertex, self.end_vertex)

    def set_position(self, new_point: vector.Point2d, line_end: LineEnd) -> Self:
        new_coords = cast(Sequence[float], new_point)
        if line_end == LineEnd.START:
            self.line.put_start_and_end_on(
                new_coords, cast(Sequence[float], self.get_end())
            )
        else:
            self.line.put_start_and_end_on(
                cast(Sequence[float], self.get_start()), new_coords
            )
        self.get_vertex(line_end).move_to(new_point)
        return self

    def get_length(self) -> float:
        return vector.norm(self.get_end() - self.get_start())
    
    def get_direction(self) -> vector.Direction2d:
        return vector.normalize(self.get_end() - self.get_start())

    def get_vertex(self, line_end: LineEnd) -> mn.Dot:
        return self.start_vertex if line_end == LineEnd.START else self.end_vertex

    def get_point(self, line_end: LineEnd) -> vector.Point2d:
        return self.get_vertex(line_end).get_center()

    def get_start(self) -> vector.Point2d:
        return self.get_point(LineEnd.START)

    def get_end(self) -> vector.Point2d:
        return self.get_point(LineEnd.END)

    def click_vertex(self, line_end: LineEnd) -> mn.Animation:
        return click(self.get_vertex(line_end))

    def click_start(self) -> mn.Animation:
        return self.click_vertex(LineEnd.START)

    def click_end(self) -> mn.Animation:
        return self.click_vertex(LineEnd.END)

    def click_line(self) -> mn.Animation:
        return click(self.line)

    def create(self) -> mn.Animation:
        return mn.Succession(
            mn.Create(self.start_vertex, run_time=0),
            mn.Create(self.line),
            mn.Create(self.end_vertex, run_time=0),
        )

    def uncreate(self) -> mn.Animation:
        return mn.Succession(
            mn.Uncreate(self.end_vertex, run_time=0),
            mn.Uncreate(self.line),
            mn.Uncreate(self.start_vertex, run_time=0),
        )

    def transform(
        self, new_point: vector.Point2d, line_end: LineEnd, **kwargs
    ) -> mn.Animation:
        """
        Transforms the line to the specified point.
        **kwargs: kwargs to be passed in to transform.
        """
        return mn.Transform(
            self, self.copy().set_position(new_point, line_end), **kwargs
        )


class SketchFactory:
    def __init__(self) -> None:
        self._color = color.FOREGROUND

    def set_color(self, color: color.Color) -> Self:
        self._color = color
        return self

    def make_point(self, point: vector.Point2d) -> SketchPoint:
        return SketchPoint(mn.Dot(point, color=self._color))

    def make_line(
        self, start_point: vector.Point2d, end_point: vector.Point2d
    ) -> SketchLine:
        return SketchLine(
            mn.Line(start_point, end_point, color=self._color),
            mn.Dot(start_point, color=self._color),
            mn.Dot(end_point, color=self._color),
        )

    def make_circle(self, center: vector.Point2d, radius: float) -> SketchCircle:
        return SketchCircle(
            mn.Circle(radius, color=self._color).move_to(center),
            mn.Dot(center, color=self._color),
        )
