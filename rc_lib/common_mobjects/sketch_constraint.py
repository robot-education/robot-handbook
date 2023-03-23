from typing import Callable

import manim as mn
from rc_lib.common_mobjects import sketch

ClickMethod = Callable[[], mn.Animation]

# To implement generic constraints we need to be able to interface with Sketch objects in a generic way
# The challenge is that every sketch object has different entities and can move in different ways
# We can pass methods and use inheritance though
# 

# def coincident_line_to_circle() -> mn.Animation:


# def point_to_point_coincident(
#     selection: sketch.Sketch, target: sketch.Sketch, click_method: ClickMethod
# ) -> mn.Animation:
#     if isinstance(selection, sketch.SketchLine):
#         pass

#     return mn.Succession()


# def coincident(left, right) -> mn.Animation:
#     pass
