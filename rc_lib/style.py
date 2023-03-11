from manim import *
from typing import NewType
from manim.utils.color import Colors
import enum

__all__ = ["Color", "FontSize", "Time", "center_and_scale"]

# This isn't a collision!
Color = NewType('Color', str)

class Color(enum.StrEnum):
    RED = Color(Colors.red_c.value)
    GREEN = Color(Colors.green_d.value)
    BLUE = Color(Colors.blue_d.value)
    YELLOW = Color(Colors.yellow_e.value)
    WHITE = Color(Colors.white.value)

DEFAULT_COLOR = Color.WHITE

# Default sizes were 24, 32, 48
class FontSize(enum.IntEnum):
    SMALL = 20
    MEDIUM = 24
    LARGE = 32


class Time():
    FAST = 0.5
    MEDIUM = 0.75
    STANDARD = 1
    SLOW = 1.5
    # The delay to display at the end of an animation.
    END = 3

"""
The length of the delay at the end of each animation.
"""
END_DELAY = 3


def center_and_scale(object: Mobject) -> Mobject:
    """
    Centers and scales an object so it lies in the center of the screen.
    """
    pass
