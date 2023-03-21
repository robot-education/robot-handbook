"""
A module defining sketcher-like entities.
The following convention is adopted - a vertex is a physical entity (usually a dot), 
whereas a point is a piece of data.
"""
import manim as mn

from typing import cast, Sequence, Self
from abc import ABC, abstractmethod
import enum

from rc_lib.math_utils import vector
from rc_lib.style import color


class Sketch(ABC):
    """
    An abstract base class for Sketch entities.
    """

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

    def draw(self) -> mn.Animation:
        return mn.Create(self)


class LineEnd(enum.IntEnum):
    START = 0
    END = 1


class SketchLine(Sketch, mn.VGroup):
    def __init__(self, line: mn.Line, start_vertex: mn.Dot, end_vertex: mn.Dot) -> None:
        self._color = color
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
        return getattr(self, ("start", "end")[line_end])

    def point(self, line_end: LineEnd) -> vector.Point2d:
        return self.vertex(line_end).get_center()

    def start_point(self) -> vector.Point2d:
        return self.point(LineEnd.START)

    def end_point(self) -> vector.Point2d:
        return self.point(LineEnd.END)

    def draw(self) -> mn.Animation:
        return mn.Succession(
            mn.Create(self.start_vertex, run_time=0),
            mn.Create(self.line),
            mn.Create(self.end_vertex, run_time=0),
        )
