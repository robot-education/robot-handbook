import manim as mn

from typing import Self
import enum

from rc_lib.math_utils import vector
from rc_lib import style


class LineEnd(enum.IntEnum):
    START = 0
    END = 1


class SketchLine(mn.VGroup):
    def __init__(
        self,
        start_point: vector.Point2d,
        end_point: vector.Point2d,
        color: style.Color = style.DEFAULT_COLOR,
    ) -> None:
        self._color = color
        self.line = mn.Line(start_point, end_point, color=color)
        self.start = mn.Dot(start_point, color=color)
        self.end = mn.Dot(end_point, color=color)
        super().__init__(self.line, self.start, self.end)

    def set_position(self, new_point: vector.Point2d, line_end: LineEnd) -> Self:
        if line_end == LineEnd.START:
            self.line.put_start_and_end_on(new_point, self.end_point())
        else:
            self.line.put_start_and_end_on(self.start_point(), new_point)
        self.tip(line_end).move_to(new_point)
        return self

    def tip(self, line_end: LineEnd):
        return getattr(self, ("start", "end")[line_end])

    def start_point(self) -> vector.Point2d:
        return self.start.get_center()

    def end_point(self) -> vector.Point2d:
        return self.end.get_center()

    def draw(self) -> mn.Animation:
        return mn.Succession(
            mn.Create(self.start, run_time=0),
            mn.Create(self.line),
            mn.Create(self.end, run_time=0),
        )
