"""Defines entities which look like Onshape sketch entities.
"""

from typing import Callable, Self
from abc import ABC
import enum

import manim as mn

from rc_lib.math_utils import vector
from rc_lib.style import color
from rc_lib.style import animation


class Sketch(mn.VGroup, ABC):
    """An abstract base class for Sketch entities."""

    def _create_override(self, **kwargs) -> mn.Animation:
        raise NotImplementedError

    def _uncreate_override(self, **kwargs) -> mn.Animation:
        raise NotImplementedError


class SketchArcBase(Sketch, ABC):
    """
    A class defining a sketch arc (or circle)  with a vertex at the center.

    This class uses the mix-in pattern to support multiple inheritance.
    """

    def __init__(self, *, arc: mn.Arc, center_vertex: mn.Dot, **kwargs: mn.VMobject):
        super().__init__(**kwargs)
        self.add(arc, center_vertex)
        self._arc = arc
        self.center_vertex = center_vertex

    def get_center(self) -> vector.Point2d:
        """Returns the center of the arc (as opposed to the center of its bounding box)."""
        return self.center_vertex.get_center()

    def get_radius(self) -> float:
        return self._arc.radius

    def set_radius(self, radius: float) -> Self:
        self._arc.scale(radius / self._arc.radius, about_point=self.get_center())
        return self


class LineEnd(enum.IntEnum):
    """An enum defining the start and end of a line (or other edge)."""

    START = 0
    END = 1


class SketchEdgeBase(Sketch, ABC):
    """A class defining a Sketch entity which has an edge with two end vertices.

    This class uses the mix-in pattern to support multiple inheritance.
    """

    def __init__(
        self, *, edge: mn.VMobject, start_vertex: mn.Dot, end_vertex: mn.Dot, **kwargs
    ):
        super().__init__(**kwargs)
        self.add(edge, start_vertex, end_vertex)
        self._edge = edge
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex

    def get_vertex(self, line_end: LineEnd) -> mn.Dot:
        """A programmatic getter for start_vertex and end_vertex."""
        return self.start_vertex if line_end == LineEnd.START else self.end_vertex

    def get_point(self, line_end: LineEnd) -> vector.Point2d:
        """A programmatic getter for start and end."""
        return self.get_vertex(line_end).get_center()

    def get_start(self) -> vector.Point2d:
        """Returns the start point of the line."""
        return self.get_point(LineEnd.START)

    def get_end(self) -> vector.Point2d:
        """Returns the end point of the line."""
        return self.get_point(LineEnd.END)


class Point(mn.Dot):
    """Defines a singlar Sketch vertex."""

    def __init__(self, dot: mn.Dot) -> None:
        super().__init__()
        self.become(dot)

    # def make_updater(self) -> Callable[[mn.Mobject], None]:
    #     """Constructs an updater function which causes a given mobject to follow this point."""

    #     def updater(mobject: mn.Mobject):
    #         mobject.move_to(self.get_center())

    #     return updater

    def follow(self, point_function: Callable[[], vector.Point2d]) -> None:
        """Adds an updater function which causes this point to track the specified input."""

        def updater(mobject: mn.Mobject):
            mobject.move_to(point_function())

        self.add_updater(updater)


def make_sketch_point(point: vector.Point2d) -> Point:
    return Point(mn.Dot(point))


class SketchCircle(SketchArcBase):
    """Defines a Sketch circle with a vertex at its center."""

    def __init__(self, circle: mn.Circle, center_vertex: mn.Dot):
        super().__init__(arc=circle, center_vertex=center_vertex)
        self.circle = circle

    @mn.override_animation(mn.Create)
    def _create_override(self, **kwargs) -> mn.Animation:
        return mn.Succession(
            mn.Create(self.center_vertex, run_time=0),
            mn.GrowFromPoint(self._arc, self.get_center(), **kwargs),
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, **kwargs) -> mn.Animation:
        return mn.Succession(
            animation.ShrinkToPoint(self._arc, self.get_center(), **kwargs),
            mn.Uncreate(self.center_vertex, run_time=0),
        )


class SketchLine(SketchEdgeBase):
    """Defines a Sketch line segment vertices at each end."""

    def __init__(self, line: mn.Line, start_vertex: mn.Dot, end_vertex: mn.Dot) -> None:
        super().__init__(edge=line, start_vertex=start_vertex, end_vertex=end_vertex)
        self.line = line

    def get_length(self) -> float:
        return vector.norm(self.get_end() - self.get_start())

    def get_direction(self) -> vector.Direction2d:
        return vector.normalize(self.get_end() - self.get_start())

    def move_point(self, point: vector.Point2d, line_end: LineEnd) -> Self:
        self.get_vertex(line_end).move_to(point)
        self.line.put_start_and_end_on(self.get_start(), self.get_end())
        return self

    def move_start(self, point: vector.Point2d) -> Self:
        return self.move_point(point, LineEnd.START)

    def move_end(self, point: vector.Point2d) -> Self:
        return self.move_point(point, LineEnd.END)

    @mn.override_animation(mn.Create)
    def _create_override(self, **kwargs) -> mn.Animation:
        end = self.get_end()
        return mn.Succession(
            mn.Create(self.start_vertex, run_time=0),
            mn.AnimationGroup(
                mn.Create(self.line),
                mn.prepare_animation(
                    self.end_vertex.move_to(self.get_start()).animate.move_to(end)
                ),
            ),
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, **kwargs) -> mn.Animation:
        return mn.Succession(
            mn.AnimationGroup(
                mn.Uncreate(self.line),
                mn.prepare_animation(
                    self.end_vertex.animate(remover=True).move_to(self.get_start())
                ),
            ),
            mn.Uncreate(self.start_vertex, run_time=0),
        )


class Arc(mn.Arc):
    """Defines a Sketch arc with vertices at each end and a vertex in the center."""

    def __init__(self, arc: mn.Arc) -> None:
        super().__init__()
        self.become(arc)

        self.start = make_sketch_point(self.get_start())
        self.end = make_sketch_point(self.get_end())
        # center is already a function...
        self.middle = make_sketch_point(self.get_arc_center())

        self.end.follow(self.get_start)
        self.start.follow(self.get_end)
        self.middle.follow(self.get_arc_center)

    def get_center(self) -> vector.Point2d:
        return self.middle.get_center()

    def set_radius(self, radius: float) -> Self:
        self.scale(radius / self.radius, about_point=self.get_center())
        return self

    @mn.override_animation(mn.Create)
    def _create_override(self, **kwargs) -> mn.Animation:
        return mn.Succession(
            mn.Create(mn.VGroup(self.middle, self.start, self.end), run_time=0),
            mn.GrowFromCenter(self),
        )

    @mn.override_animation(mn.Uncreate)
    def _uncreate_override(self, **kwargs) -> mn.Animation:
        return mn.Succession(
            animation.ShrinkToCenter(self),
            mn.Uncreate(self.middle, run_time=0),
            mn.Create(self.start, reverse_rate_function=True, remover=True, run_time=0),
            mn.Create(self.end, reverse_rate_function=True, remover=True, run_time=0),
        )


class SketchFactory:
    """A factory for Sketch objects."""

    def __init__(self) -> None:
        self._color = color.FOREGROUND

    def set_color(self, color: color.Color) -> Self:
        self._color = color
        return self

    # def make_point(self, point: vector.Point2d) -> Point:
    #     return Point(self._make_dot(point))

    def make_line(
        self, start_point: vector.Point2d, end_point: vector.Point2d
    ) -> SketchLine:
        return SketchLine(
            mn.Line(start_point, end_point, color=self._color),
            self._make_dot(start_point),
            self._make_dot(end_point),
        )

    def make_circle(self, center: vector.Point2d, radius: float) -> SketchCircle:
        return SketchCircle(
            mn.Circle(radius, color=self._color).move_to(center), self._make_dot(center)
        )

    def _make_dot(self, center: vector.Point2d) -> mn.Dot:
        return mn.Dot(center, color=self._color)

    def make_arc(
        self, center: vector.Point2d, radius: float, start_angle: float, angle: float
    ) -> Arc:
        # start_angle is typed incorrectly as int
        arc = mn.Arc(radius, start_angle=start_angle, angle=angle, color=self._color, arc_center=center)  # type: ignore
        return Arc(arc)
