from manim import *
from typing import NewType
from manim.utils.color import Colors
import enum

__all__ = ["Color", "FontSize", "Time", "center_and_scale"]

Color = NewType("Color", str)


class Palette(enum.StrEnum):
    RED = Colors.red_c.value
    GREEN = Colors.green_d.value
    BLUE = Colors.blue_d.value
    YELLOW = Colors.yellow_e.value
    WHITE = Colors.white.value


DEFAULT_COLOR = Palette.WHITE

# Default sizes were 24, 32, 48
class FontSize(enum.IntEnum):
    SMALL = 20
    MEDIUM = 24
    LARGE = 32


"""
The length of the delay at the end of each animation.
"""
END_DELAY = 3


def center_and_scale(object: Mobject) -> Mobject:
    """
    Centers and scales an object so it lies in the center of the screen.
    """
    pass
