from manim import *

from rc_lib import math_types as T
from rc_lib import style

__all__ = ["SketchLine"]


class SketchLine(VGroup):
    def __init__(self, start_point: T.Point2d, end_point: T.Point2d, color: style.Color = style.DEFAULT_COLOR) -> None:
        self._color = color
        self._line = Line(start_point, end_point, color=color)
        self._start = Dot(start_point, color=color)
        self._end = Dot(end_point, color=color)
        super().__init__(self._line, self._start, self._end)

    def line(self) -> Line:
        return self._line

    def start(self) -> Dot:
        return self._start

    def end(self) -> Dot:
        return self._end
    
    def start_point(self) -> T.Point2d:
        return self._start.get_center()

    def end_point(self) -> T.Point2d:
        return self._end.get_center()

    def create(self) -> Animation:
        return Succession(
            Create(self.start(), run_time=0), 
            Create(self._line),
            Create(self.end(), run_time=0))

    def move_start(self, new_start_point: T.Point2d, **kwargs) -> Animation:
        """
        Move the start point to a given start point using a Transform.
        """
        return Transform(self, SketchLine(new_start_point, self.end_point(), color=self._color), **kwargs)

    def move_end(self, new_end_point: T.Point2d, **kwargs) -> Animation:
        """
        Move the end point to a given start point using a Transform.
        """
        return Transform(self, SketchLine(self.start_point(), new_end_point, color=self._color), **kwargs)
