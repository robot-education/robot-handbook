import enum

import manim as mn
from rc_lib.style import color
from rc_lib.design import sketch


class SketchType(enum.IntEnum):
    POINT = 0
    LINE = 1
    CIRCLE = 2
    ARC = 3


def classify(base: sketch.Base) -> SketchType:
    if isinstance(base, sketch.Line):
        return SketchType.POINT
    elif isinstance(base, sketch.Line):
        return SketchType.POINT
    elif isinstance(base, sketch.Circle):
        return SketchType.CIRCLE
    elif isinstance(base, sketch.Arc):
        return SketchType.ARC
    raise NotImplementedError


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


class LineEnd(enum.IntEnum):
    """An enum defining the start and end of a line (or other edge)."""

    START = 0
    END = 1
