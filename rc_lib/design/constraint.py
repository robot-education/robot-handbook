from abc import ABC
import enum
from types import UnionType
from typing import NoReturn

import manim as mn
from rc_lib.design import sketch, sketch_utils
from rc_lib.math_utils import vector


def get_key(base: sketch.Base, key: str | None) -> sketch.Base:
    match key:
        case None:
            return base
        case "middle":
            throw_if_not(base, sketch.Circle | sketch.Arc)
        case "start":
            throw_if_not(base, sketch.Line | sketch.Arc)
        case "end":
            throw_if_not(base, sketch.Line | sketch.Arc)
        case _:
            key_error()

    return getattr(base, key)


def throw_if(base: sketch.Base, type: type[sketch.Base] | UnionType) -> None:
    if isinstance(base, type):
        key_error()


def throw_if_not(base: sketch.Base, type: type[sketch.Base] | UnionType) -> None:
    if not isinstance(base, type):
        key_error()


def move_line(
    base: sketch.Line, base_key: str | None, point: vector.Point2d
) -> mn.Animation:
    if base_key is None or (base_key != "start" and base_key != "end"):
        key_error()
    return getattr(base.animate, "move_" + base_key)(point)


def key_error() -> NoReturn:
    raise KeyError("A key passed to constraint is invalid")


class Coincident(mn.Succession):
    """Constrains a point to a target using a coincident constraint."""

    def __init__(
        self, base: sketch.Base, target: sketch.Base, base_key: str | None = None
    ) -> None:
        if base_key is None:
            throw_if(base, sketch.Line | sketch.Arc | sketch.Circle)

        base_element = get_key(base, base_key)
        target_point = self._get_target(target, base_element.get_center())

        animation = base.animate
        if isinstance(base, sketch.Line):
            animation = move_line(base, base_key, target_point)
        else:
            animation.move_to(target_point)

        super().__init__(
            sketch_utils.Click(base_element),
            sketch_utils.Click(target),
            mn.prepare_animation(animation),
        )

    def _get_target(self, target: sketch.Base, point: vector.Point2d) -> vector.Point2d:
        if isinstance(target, sketch.Circle | sketch.Arc):
            return target.get_center() + (
                vector.direction(target.get_center(), point) * target.radius
            )
        elif isinstance(target, sketch.Line):
            return target.get_projection(point)
        elif isinstance(target, sketch.Point):
            return target.get_center()


# class Horizontal(mn.Succession):
#     def __init__(
#         self, base: sketch.Line
#     ) -> None:


# class VerticalLine(mn.Succession):
#     def __init__(self, base: sketch.Line) -> None:
#         angle = base.get_angle()
#         pass


class AlignType(enum.IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1


class AlignPointBase(mn.Succession, ABC):
    def __init__(
        self, base: sketch.Base, target: sketch.Point, *, base_key: str, type: AlignType
    ) -> None:
        base_element = get_key(base, base_key)

        if type == AlignType.VERTICAL:
            values = (target, base_element)
        else:
            values = (base_element, target)

        target_point = vector.point_2d(
            values[0].get_center()[0], values[1].get_center()[1]
        )
        if isinstance(base, sketch.Line):
            animation = move_line(base, base_key, target_point)
        else:
            animation = base.animate.move_to(target_point)

        super().__init__(
            sketch_utils.Click(base_element),
            sketch_utils.Click(target),
            mn.prepare_animation(animation),
        )


class VerticalPoint(AlignPointBase):
    def __init__(
        self, base: sketch.Base, target: sketch.Point, *, base_key: str
    ) -> None:
        super().__init__(base, target, base_key=base_key, type=AlignType.VERTICAL)


class HorizontalPoint(AlignPointBase):
    def __init__(
        self, base: sketch.Base, target: sketch.Point, *, base_key: str
    ) -> None:
        super().__init__(base, target, base_key=base_key, type=AlignType.HORIZONTAL)


class Tangent(mn.Succession):
    """Constrains a point to a target using a tangent constraint.

    The move performed is a straight line transform to the closest tangent position.
    """

    def __init__(
        self,
        base: sketch.Line | sketch.Arc | sketch.Circle,
        target: sketch.Arc | sketch.Circle,
    ) -> None:
        """Constructs a tangent constraint animation."""
        if isinstance(base, sketch.Line):
            translation = self._get_line_translation(base, target)
        else:
            translation = self._get_circle_translation(base, target)
        animation = base.animate.shift(translation)

        super().__init__(
            sketch_utils.Click(base),
            sketch_utils.Click(target),
            mn.prepare_animation(animation),
        )

    def _get_line_translation(
        self, base: sketch.Line, target: sketch.Circle | sketch.Arc
    ) -> vector.Vector2d:
        projection: vector.Point2d = base.get_projection(target.get_center())  # type: ignore
        return vector.direction(projection, target.get_center()) * (
            vector.norm(target.get_center() - projection) - target.radius
        )

    def _get_circle_translation(
        self, base: sketch.Circle | sketch.Arc, target: sketch.Circle | sketch.Arc
    ) -> vector.Vector2d:
        vec = target.get_center() - base.get_center()
        return vector.normalize(vec) * (vector.norm(vec) - base.radius - target.radius)
