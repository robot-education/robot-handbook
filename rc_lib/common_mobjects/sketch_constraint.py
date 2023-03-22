from typing import Callable

import manim as mn
from rc_lib.common_mobjects import sketch

ClickMethod = Callable[[], mn.Animation]
"""
A method which represents clicking on an entity.
Transforms selection to target.
Returns a tuple containing the click animation.
"""


def point_to_point_coincident(
    selection: sketch.Sketch, target: sketch.Sketch, click_method: ClickMethod
) -> mn.Animation:
    if isinstance(selection, sketch.SketchLine):
        pass

    return mn.Succession()


# def coincident(left, right) -> mn.Animation:
#     pass
