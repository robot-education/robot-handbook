from types import UnionType
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
            raise KeyError("The key is not valid for any entity.")

    return getattr(base, key)


def throw_if_not(base: sketch.Base, type: type[sketch.Base] | UnionType) -> None:
    if not isinstance(base, type):
        raise KeyError("The key did not correspond to a point in sketch.Base")


class PointCoincident(mn.Succession):
    """Performs an animation which constrains a point to a target using a coincident constraint."""

    def __init__(self, base: sketch.Line, base_key: str, target: sketch.Base):
        base_element = get_key(base, base_key)
        target_point = self._get_target(target, base_element.get_center())

        animation = base.animate
        if base_key == "start":
            animation.move_start(target_point)
        else:
            animation.move_end(target_point)

        super().__init__(
            sketch_utils.Click(base_element),
            sketch_utils.Click(target),
            mn.prepare_animation(animation),
        )

    def _get_target(self, target: sketch.Base, point: vector.Point2d) -> vector.Point2d:
        if isinstance(target, sketch.Circle | sketch.Arc):
            return (
                target.get_center()
                + (vector.direction(target.get_center(), point) * target.radius)
            )
        elif isinstance(target, sketch.Line):
            return target.get_projection(point)
        elif isinstance(target, sketch.Point):
            return target.get_center()
