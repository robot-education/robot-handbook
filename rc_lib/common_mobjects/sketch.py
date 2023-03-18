import manim as mn

from typing import cast, Sequence, Self
import enum

from rc_lib.math_utils import vector
from rc_lib.style import color


class LineEnd(enum.IntEnum):
    START = 0
    END = 1


class SketchLine(mn.VGroup):
    def __init__(
        self,
        start_point: vector.Point2d,
        end_point: vector.Point2d,
        color: color.Color = color.FOREGROUND,
    ) -> None:
        self._color = color
        self.line = mn.Line(start_point, end_point, color=color)
        self.start = mn.Dot(start_point, color=color)
        self.end = mn.Dot(end_point, color=color)
        super().__init__(self.line, self.start, self.end)

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
