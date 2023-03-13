from manim import *

from typing import Self
import enum

from rc_lib import math_types as T
from rc_lib import style

__all__ = ["SketchLine"]


class LineEnd(enum.IntEnum):
    START = 0
    END = 1


class SketchLine(VGroup):
    def __init__(
        self,
        start_point: T.Point2d,
        end_point: T.Point2d,
        color: style.Color = style.DEFAULT_COLOR,
    ) -> None:
        self._color = color
        self._line = Line(start_point, end_point, color=color)
        self._start = Dot(start_point, color=color)
        self._end = Dot(end_point, color=color)
        super().__init__(self._line, self._start, self._end)

        # tip = ArrowCircleFilledTip(stroke_width=0.08, color=color)
        # self._start = tip.copy()
        # self._end = tip.copy()

        # self._line.add_tip(self._start, at_start=True)
        # self._line.add_tip(self._end, at_start=False)

    def set_position(self, new_point: T.Point2d, line_end: LineEnd) -> Self:
        if line_end == LineEnd.START:
            self._line.put_start_and_end_on(new_point, self.end_point())
        else:
            self._line.put_start_and_end_on(self.start_point(), new_point)
        self._tip(line_end).move_to(new_point)
        return self

    def line(self) -> Line:
        return self._line

    def _tip(self, line_end: LineEnd):
        return getattr(self, ("_start", "_end")[line_end])

    def start(self) -> VMobject:
        return self._tip(LineEnd.START)

    def end(self) -> VMobject:
        return self._tip(LineEnd.END)

    def start_point(self) -> T.Point2d:
        return self.start().get_center()

    def end_point(self) -> T.Point2d:
        return self.end().get_center()

    def create(self) -> Animation:
        return Succession(
            Create(self.start(), run_time=0),
            Create(self._line),
            Create(self.end(), run_time=0),
        )
