from abc import ABC
from types import UnionType
from typing import Any, NoReturn
import enum

import manim as mn
import numpy as np

from rc_lib.design import sketch, sketch_utils
from rc_lib.math_utils import vector, tangent


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
            raise_key_error()

    return getattr(base, key)


def throw_if(base: sketch.Base, type: type[sketch.Base] | UnionType) -> None:
    if isinstance(base, type):
        raise_key_error()


def throw_if_not(base: sketch.Base, type: type[sketch.Base] | UnionType) -> None:
    if not isinstance(base, type):
        raise_key_error()


def raise_key_error() -> NoReturn:
    raise KeyError("A key passed to constraint is invalid")


def move_line(
    base: sketch.Line, base_key: str | None, point: vector.Point2d, **anim_kwargs
) -> mn.Animation:
    if base_key is None or (base_key != "start" and base_key != "end"):
        raise_key_error()
    return getattr(base.animate(**anim_kwargs), "move_" + base_key)(point)


class ConstraintBase(mn.Succession, ABC):
    def __init__(
        self, base: mn.VMobject, target: mn.VMobject, builder: mn.Animation | Any
    ):
        super().__init__(
            sketch_utils.Click(base),
            sketch_utils.Click(target),
            mn.prepare_animation(builder),
        )


class Coincident(ConstraintBase):
    """Constrains a point to a target using a coincident constraint."""

    def __init__(
        self, base: sketch.Base, target: sketch.Base, base_key: str | None = None
    ) -> None:
        if base_key is None:
            throw_if(base, sketch.Line | sketch.Arc | sketch.Circle)

        base_element = get_key(base, base_key)
        target_point = self._get_target(target, base_element.get_center())

        if isinstance(base, sketch.Line):
            animation = move_line(base, base_key, target_point)
        else:
            animation = base.animate.move_to(target_point)

        super().__init__(base_element, target, animation)

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


class AlignPointBase(ConstraintBase, ABC):
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

        super().__init__(base_element, target, animation)


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


class Tangent(ConstraintBase):
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

        super().__init__(base, target, animation)

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


class Equal(ConstraintBase):
    def __init__(
        self,
        base: sketch.Line | sketch.Circle | sketch.Line,
        target: sketch.Line | sketch.Circle | sketch.Arc,
    ) -> None:
        """Sets target to be equal to length.

        This constraint is moderately counterintuitive in that base is preserved while target is modified.
        However, this matches the behavior of equal for multiple targets.
        """
        animation = target.animate
        if isinstance(base, sketch.Line) and isinstance(target, sketch.Line):
            midpoint = target.get_midpoint()
            offset = target.get_direction() * (base.get_length() / 2)
            animation.put_start_and_end_on(midpoint - offset, midpoint + offset)
        elif isinstance(base, sketch.Circle | sketch.Arc) and isinstance(
            target, sketch.Circle | sketch.Arc
        ):
            animation.set_radius(base.radius)
        else:
            raise TypeError("Equal entities must be compatible")

        super().__init__(base, target, animation)


class TangentRotate(ConstraintBase):
    """Applies a tangent constraint to a line which is already coincident to a circle or arc."""

    def __init__(
        self, base: sketch.Line, target: sketch.Circle | sketch.Arc, reverse=False
    ) -> None:
        key = self._get_touching_key(base, target)
        opposite_key = "end" if key == "start" else "start"
        close_point = getattr(base, "get_" + key)()
        far_point = getattr(base, "get_" + opposite_key)()

        if reverse:
            tangent_point = tangent.point_to_circle_tangent(
                far_point, target.get_center(), target.radius
            )
        else:
            tangent_point = tangent.circle_to_point_tangent(
                target.get_center(), target.radius, far_point
            )

        angle = vector.angle_between_points(
            close_point, tangent_point, target.get_center()
        )

        if reverse:
            angle *= -1

        animation = move_line(
            base,
            key,
            tangent_point,
            path_arc=angle,
            path_arg_centers=[target.get_center()],
        )
        super().__init__(base, target, animation)

    def _get_touching_key(
        self, base: sketch.Line, target: sketch.Circle | sketch.Arc
    ) -> str:
        if np.isclose(
            vector.norm(base.get_start() - target.get_center()), target.radius
        ):
            return "start"
        elif np.isclose(
            vector.norm(base.get_end() - target.get_center()), target.radius
        ):
            return "end"
        raise ValueError("Expected line to touch target")
