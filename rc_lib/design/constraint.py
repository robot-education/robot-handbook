from typing import Any
import enum

import manim as mn

from rc_lib.style import color


class Add(mn.Animation):
    def __init__(self, *mobjects: mn.VMobject):
        super().__init__(mn.VGroup(*mobjects), introducer=True, run_time=0)


class Remove(mn.Animation):
    def __init__(self, *mobjects: mn.VMobject):
        super().__init__(
            mn.VGroup(*mobjects), introducer=True, remover=True, run_time=0
        )


# doesn't work as a class member...
Z_INDEX = 500


class Click(mn.Transform):
    """Defines an animation which represents an object getting clicked."""

    def __init__(self, mobject: mn.Mobject):
        target = mobject.copy().set_stroke(width=4 * 3.5).set_color(color.Palette.YELLOW)  # type: ignore

        # set z_index to make highlight go over the top (a bit suss)
        global Z_INDEX
        mobject.set_z_index(Z_INDEX)
        Z_INDEX += 1

        super().__init__(
            mobject, target_mobject=target, rate_func=mn.there_and_back, run_time=0.75
        )


def make(animation: mn.Animation | Any, *mobjects: mn.Mobject) -> mn.Succession:
    return mn.Succession(*[Click(mobject) for mobject in mobjects], animation)


class ConstraintBase(mn.Animation):
    def __new__(cls, base: mn.Mobject, *mobjects: mn.Mobject, **kwargs):
        override_function = base.animation_override_for(cls)
        if not callable(override_function):
            raise NotImplementedError
        animation = override_function(base, *mobjects, **kwargs)

        values = list(mobjects)
        values.insert(0, base)
        return mn.Succession(*[Click(mobject) for mobject in values], animation)

    def __init__(self, base: mn.Mobject, *args, **kwargs) -> None:
        raise NotImplementedError


class TwoSelectionBase(ConstraintBase):
    def __init__(self, base: mn.Mobject, target: mn.Mobject) -> None:
        raise NotImplementedError


class OneSelectionBase(ConstraintBase):
    def __init__(self, base: mn.Mobject) -> None:
        raise NotImplementedError


class Equal(TwoSelectionBase):
    pass


class Coincident(TwoSelectionBase):
    pass


class Tangent(ConstraintBase):
    def __init__(
        self,
        base: mn.Mobject,
        target: mn.Mobject,
        rotate: bool = False,
        reverse: bool = False,
    ) -> None:
        raise NotImplementedError


class AlignType(enum.IntEnum):
    HORIZONTAL = 0
    VERTICAL = 1


class Horizontal(ConstraintBase):
    pass


class Vertical(ConstraintBase):
    pass


# class TangentRotate(ConstraintBase):
#     """Applies a tangent constraint to a line which is already coincident to a circle or arc."""

#     def __init__(
#         self, base: sketch.Line, target: sketch.Circle | sketch.Arc, reverse=False
#     ) -> None:
