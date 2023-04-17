from typing import Any

import manim as mn

from rc_lib.design import sketch, sketch_animation


class ConstraintBase(mn.Succession):
    def __init__(self, animation: mn.Animation | Any, *mobjects: sketch.Base) -> None:
        super().__init__(
            *[sketch_animation.Click(mobject) for mobject in mobjects], animation
        )


class Equal(ConstraintBase):
    def __init__(
        self, base: sketch.ArcBase | sketch.Line, target: sketch.ArcBase | sketch.Line
    ) -> None:
        if isinstance(base, sketch.ArcBase) and isinstance(target, sketch.ArcBase):
            animation = base.equal_constraint(target)
        elif isinstance(base, sketch.Line) and isinstance(target, sketch.Line):
            animation = base.equal_constraint(target)
        else:
            raise TypeError("Expected arguments to be of the same type.")
        super().__init__(animation, base, target)


class Coincident(ConstraintBase):
    def __init__(self, base: sketch.Point, target: sketch.Base) -> None:
        animation = base.animate.move_to(target.coincident_target(base.get_center()))
        super().__init__(animation, base, target)


class Tangent(ConstraintBase):
    def __init__(
        self,
        base: mn.Mobject,
        target: mn.Mobject,
        rotate: bool = False,
        reverse: bool = False,
    ) -> None:
        raise NotImplementedError


class Align(ConstraintBase):
    def __init__(
        self,
        type: sketch.AlignType,
        line: sketch.Line | None = None,
        points: tuple[sketch.Point, sketch.Point] | None = None,
    ):
        if line is not None:
            super().__init__(line.align_constraint(type), line)
        elif points is not None:
            super().__init__(points[0].align_constraint(points[1], type), *points)
        else:
            raise ValueError("Expected either a line or two points.")


class Horizontal(Align):
    def __init__(
        self,
        line: sketch.Line | None = None,
        points: tuple[sketch.Point, sketch.Point] | None = None,
    ):
        return super().__init__(sketch.AlignType.HORIZONTAL, line=line, points=points)


class Vertical(Align):
    def __init__(
        self,
        line: sketch.Line | None = None,
        points: tuple[sketch.Point, sketch.Point] | None = None,
    ):
        return super().__init__(sketch.AlignType.VERTICAL, line=line, points=points)


class Midpoint(ConstraintBase):
    def __new__(cls, base: mn.Mobject, *args):
        if len(args) == 1:
            base_index = 0
        elif len(args) == 2:
            base_index = 1
        else:
            raise ValueError("Expected a line or two points.")
        return super().__new__(cls, base, *args, base_index=base_index)

    def __init__(self, base: mn.Mobject, *args: mn.Mobject) -> None:
        """Performs a midpoint constraint on the passed in points."""
        raise NotImplementedError


class Concentric(ConstraintBase):
    pass
