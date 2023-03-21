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


# class SketchState(color.Color, enum.Enum):
#     NORMAL = color.Palette.BLUE
#     ERROR = color.Palette.RED


class Sketch(ABC):
    """
    An abstract base class for Sketch entities.
    """

    # @abstractmethod
    # def set_state(self) -> Self:
    #     pass

    @abstractmethod
    def draw(self) -> mn.Animation:
        pass


class SketchCircle(Sketch, mn.VGroup):
    def __init__(self, circle: mn.Circle, vertex: mn.Dot) -> None:
        self.circle = circle
        self.vertex = vertex
        super().__init__(self.circle, self.point)

    def center_point(self) -> vector.Vector2d:
        return self.get_center()

    def click_center(self) -> mn.Animation:
        return mn.Flash(self.vertex, run_time=0.75)

    def click_circle(self) -> mn.Animation:
        return mn.Flash(
            self.vertex,
            flash_radius=mn.SMALL_BUFF + self.circle.radius,
            num_lines=math.floor(12 * self.circle.radius),
            run_time=0.75,
        )

    def draw(self) -> mn.Animation:
        return mn.Succession(
            mn.Create(self.vertex, run_time=0), mn.GrowFromCenter(self.circle)
        )


class SketchPoint(Sketch, mn.VGroup):
    def __init__(self, vertex: mn.Dot) -> None:
        self.vertex = vertex
        super().__init__(self.point)

    def point(self) -> vector.Vector2d:
        return self.get_center()

    def click(self) -> mn.Animation:
        return mn.Flash(self.vertex, run_time=0.75)

    def draw(self) -> mn.Animation:
        return mn.Create(self)


class LineEnd(enum.IntEnum):
    START = 0
    END = 1


class SketchLine(Sketch, mn.VGroup):
    def __init__(self, line: mn.Line, start_vertex: mn.Dot, end_vertex: mn.Dot) -> None:
        self.line = line
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        super().__init__(self.line, self.start_vertex, self.end_vertex)

    def set_position(self, new_point: vector.Point2d, line_end: LineEnd) -> Self:
        new_coords = cast(Sequence[float], new_point)
        if line_end == LineEnd.START:
            self.line.put_start_and_end_on(
                new_coords, cast(Sequence[float], self.end_point())
            )
        else:
            self.line.put_start_and_end_on(
                cast(Sequence[float], self.start_point()), new_coords
            )
        self.vertex(line_end).move_to(new_point)
        return self

    def vertex(self, line_end: LineEnd) -> mn.Dot:
        return self.start_vertex if line_end == LineEnd.START else self.end_vertex

    def point(self, line_end: LineEnd) -> vector.Point2d:
        return self.vertex(line_end).get_center()

    def start_point(self) -> vector.Point2d:
        return self.point(LineEnd.START)

    def end_point(self) -> vector.Point2d:
        return self.point(LineEnd.END)

    def click_vertex(self, line_end: LineEnd) -> mn.Animation:
        return mn.Flash(self.vertex(line_end), run_time=0.75)

    def click_line(self) -> mn.Animation:
        return mn.Flash(self.line, run_time=0.75)

    def uncreate(self) -> mn.Animation:
        return mn.Succession(
            mn.Uncreate(self.end_vertex, run_time=0),
            mn.Uncreate(self.line),
            mn.Uncreate(self.start_vertex, run_time=0),
        )

    def draw(self) -> mn.Animation:
        return mn.Succession(
            mn.Create(self.start_vertex, run_time=0),
            mn.Create(self.line),
            mn.Create(self.end_vertex, run_time=0),
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

    def make_circle(self, center_point: vector.Point2d, radius: float) -> SketchCircle:
        return SketchCircle(
            mn.Circle(radius, color=self._color).move_to(center_point),
            mn.Dot(center_point, color=self._color),
        )
