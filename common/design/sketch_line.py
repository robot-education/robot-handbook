from manim import *

__all__ = ["SketchLine"]


class SketchLine(VGroup):
    def __init__(self, start_point: np.ndarray, end_point: np.ndarray) -> None:
        self._line = Line(start_point, end_point)
        self._start = Dot(start_point)
        self._end = Dot(end_point)
        super().__init__(self._line, self._start, self._end)

    def line(self) -> Line:
        return self._line

    def start_point(self) -> Dot:
        return self._start

    def end_point(self) -> Dot:
        return self._end

    def create(self) -> Animation:
        return Succession(Create(self.start_point(), run_time=0.05), Create(self._line), Create(self.end_point(), run_time=0.05))

    def move_start(self, new_start_point: np.ndarray, **kwargs) -> Animation:
        """
        Move the start point to a given start point using a Transform.
        """
        return Transform(self, SketchLine(new_start_point, self._end.get_center()), **kwargs)

    def move_end(self, new_end_point: np.ndarray, **kwargs) -> Animation:
        """
        Move the end point to a given start point using a Transform.
        """
        return Transform(self, SketchLine(self._start.get_center(), new_end_point), **kwargs)
