from abc import ABC
import inspect

import manim as mn

from rc_lib.style import color


class Click(mn.Succession):
    """Defines an animation which represents an object getting clicked."""

    Z_INDEX = 500

    def __init__(self, mobject: mn.Mobject):
        target = mobject.copy().set_stroke(width=4 * 3.5).set_color(color.Palette.YELLOW)  # type: ignore

        # set z_index to make highlight go over the top (a bit suss)
        mobject.set_z_index(self.Z_INDEX)
        self.Z_INDEX += 1

        super().__init__(
            mn.Transform(mobject, target, rate_func=mn.there_and_back, run_time=0.75)
        )


class ConstraintBase(mn.Animation, ABC):
    def __new__(cls, base: mn.Mobject, *args, mobjects: list[mn.Mobject], **kwargs):
        func = base.animation_override_for(cls)
        if not callable(func):
            raise TypeError("Equal must be overridden")

        mobjects.insert(0, base)  # base always comes first

        # arg_spec = inspect.getfullargspec(func)
        # if arg_spec.varkw != None:

        return mn.Succession(
            *[Click(mobject) for mobject in mobjects], func(base, *args, **kwargs)
        )


class Equal(ConstraintBase):
    def __new__(cls, base: mn.Mobject, target: mn.Mobject):
        return super().__new__(cls, base, target, mobjects=[target])

    def __init__(self, base: mn.Mobject, target: mn.Mobject) -> None:
        pass


# def get_key(base: sketch.Base, key: str | None) -> sketch.Base:
#     match key:
#         case None:
#             return base
#         case "middle":
#             throw_if_not(base, sketch.Circle | sketch.Arc)
#         case "start":
#             throw_if_not(base, sketch.Line | sketch.Arc)
#         case "end":
#             throw_if_not(base, sketch.Line | sketch.Arc)
#         case _:
#             raise_key_error()

#     return getattr(base, key)


# def throw_if(base: sketch.Base, type: type[sketch.Base] | UnionType) -> None:
#     if isinstance(base, type):
#         raise_key_error()


# def throw_if_not(base: sketch.Base, type: type[sketch.Base] | UnionType) -> None:
#     if not isinstance(base, type):
#         raise_key_error()


# def raise_key_error() -> NoReturn:
#     raise KeyError("A key passed to constraint is invalid")


# def move_line(
#     base: sketch.Line, base_key: str | None, point: vector.Point2d, **anim_kwargs
# ) -> mn.Animation:
#     if base_key is None or (base_key != "start" and base_key != "end"):
#         raise_key_error()
#     return getattr(base.animate(**anim_kwargs), "move_" + base_key)(point)


# class ConstraintBase(mn.Succession, ABC):
#     def __init__(self, builder: mn.Animation | Any, *mobjects: mn.VMobject):
#         super().__init__(
#             *[Click(mobject) for mobject in mobjects],
#             mn.prepare_animation(builder),
#         )


# class Coincident(ConstraintBase):
#     """Constrains a point to a target using a coincident constraint."""

#     def __init__(
#         self, base: sketch.Base, target: sketch.Base, base_key: str | None = None
#     ) -> None:
#         if base_key is None:
#             throw_if(base, sketch.Line | sketch.Arc | sketch.Circle)

#         base_element = get_key(base, base_key)
#         target_point = self._get_target(target, base_element.get_center())

#         if isinstance(base, sketch.Line):
#             animation = move_line(base, base_key, target_point)
#         else:
#             animation = base.animate.move_to(target_point)

#         super().__init__(animation, base_element, target)

#     def _get_target(self, target: sketch.Base, point: vector.Point2d) -> vector.Point2d:
#         if isinstance(target, sketch.Circle | sketch.Arc):
#             return target.get_center() + (
#                 vector.direction(target.get_center(), point) * target.radius
#             )
#         elif isinstance(target, sketch.Line):
#             return target.get_projection(point)
#         elif isinstance(target, sketch.Point):
#             return target.get_center()


# # class Horizontal(mn.Succession):
# #     def __init__(
# #         self, base: sketch.Line
# #     ) -> None:


# # class VerticalLine(mn.Succession):
# #     def __init__(self, base: sketch.Line) -> None:
# #         angle = base.get_angle()
# #         pass


# class AlignType(enum.IntEnum):
#     HORIZONTAL = 0
#     VERTICAL = 1


# class AlignPointBase(ConstraintBase, ABC):
#     def __init__(
#         self, base: sketch.Base, target: sketch.Point, *, base_key: str, type: AlignType
#     ) -> None:
#         base_element = get_key(base, base_key)

#         if type == AlignType.VERTICAL:
#             values = (target, base_element)
#         else:
#             values = (base_element, target)

#         target_point = vector.point_2d(
#             values[0].get_center()[0], values[1].get_center()[1]
#         )
#         if isinstance(base, sketch.Line):
#             animation = move_line(base, base_key, target_point)
#         else:
#             animation = base.animate.move_to(target_point)

#         super().__init__(animation, base_element, target)


# class VerticalPoint(AlignPointBase):
#     def __init__(
#         self, base: sketch.Base, target: sketch.Point, *, base_key: str
#     ) -> None:
#         super().__init__(base, target, base_key=base_key, type=AlignType.VERTICAL)


# class HorizontalPoint(AlignPointBase):
#     def __init__(
#         self, base: sketch.Base, target: sketch.Point, *, base_key: str
#     ) -> None:
#         super().__init__(base, target, base_key=base_key, type=AlignType.HORIZONTAL)


# class Tangent(ConstraintBase):
#     """Constrains a point to a target using a tangent constraint.

#     The move performed is a straight line transform to the closest tangent position.
#     """

#     def __init__(
#         self,
#         base: sketch.Line | sketch.Arc | sketch.Circle,
#         target: sketch.Arc | sketch.Circle,
#     ) -> None:
#         """Constructs a tangent constraint animation."""
#         if isinstance(base, sketch.Line):
#             translation = self._get_line_translation(base, target)
#         else:
#             translation = self._get_circle_translation(base, target)
#         animation = base.animate.shift(translation)

#         super().__init__(animation, base, target)

#     def _get_line_translation(
#         self, base: sketch.Line, target: sketch.Circle | sketch.Arc
#     ) -> vector.Vector2d:
#         projection: vector.Point2d = base.get_projection(target.get_center())  # type: ignore
#         return vector.direction(projection, target.get_center()) * (
#             vector.norm(target.get_center() - projection) - target.radius
#         )

#     def _get_circle_translation(
#         self, base: sketch.Circle | sketch.Arc, target: sketch.Circle | sketch.Arc
#     ) -> vector.Vector2d:
#         vec = target.get_center() - base.get_center()
#         return vector.normalize(vec) * (vector.norm(vec) - base.radius - target.radius)


# # class Equal(ConstraintBase):
# #     def __init__(
# #         self,
# #         base: sketch.Line | sketch.ArcBase,
# #         target: sketch.Line | sketch.ArcBase,
# #     ) -> None:
# #         """Sets target to be equal to length.

# #         This constraint is moderately counterintuitive in that base is preserved while target is modified.
# #         However, this matches the behavior of equal for multiple targets.
# #         """
# #         # or doesn't work with type guards...
# #         if isinstance(base, sketch.Line) and isinstance(target, sketch.Line):
# #             super().__init__(base.equal(target), base, target)
# #         elif isinstance(base, sketch.ArcBase) and isinstance(target, sketch.ArcBase):
# #             super().__init__(base.equal(target), base, target)
# #         else:
# #             raise TypeError("base and target must be the same")


# class TangentRotate(ConstraintBase):
#     """Applies a tangent constraint to a line which is already coincident to a circle or arc."""

#     def __init__(
#         self, base: sketch.Line, target: sketch.Circle | sketch.Arc, reverse=False
#     ) -> None:
#         key = self._get_touching_key(base, target)
#         opposite_key = "end" if key == "start" else "start"
#         close_point = getattr(base, "get_" + key)()
#         far_point = getattr(base, "get_" + opposite_key)()

#         if reverse:
#             tangent_point = tangent.point_to_circle_tangent(
#                 far_point, target.get_center(), target.radius
#             )
#         else:
#             tangent_point = tangent.circle_to_point_tangent(
#                 target.get_center(), target.radius, far_point
#             )

#         angle = vector.angle_between_points(
#             close_point, tangent_point, target.get_center()
#         )

#         if reverse:
#             angle *= -1

#         animation = move_line(
#             base,
#             key,
#             tangent_point,
#             path_arc=angle,
#             path_arg_centers=[target.get_center()],
#         )
#         super().__init__(animation, base, target)

#     def _get_touching_key(
#         self, base: sketch.Line, target: sketch.Circle | sketch.Arc
#     ) -> str:
#         if np.isclose(
#             vector.norm(base.get_start() - target.get_center()), target.radius
#         ):
#             return "start"
#         elif np.isclose(
#             vector.norm(base.get_end() - target.get_center()), target.radius
#         ):
#             return "end"
#         raise ValueError("Expected line to touch target")
