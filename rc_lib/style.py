from manim import *
from manim.utils.color import Colors
import enum

__all__ = ["Color", "FontSize", "Time", "center_and_scale"]

# Colors
# C_HIGHLIGHT = TEAL_C
# C_EMPHASIS = ORANGE


class Color(enum.StrEnum):
    RED = Colors.red_c.value
    GREEN = Colors.green_d.value
    BLUE = Colors.blue_d.value
    YELLOW = Colors.yellow_e.value

# Default sizes:
# SMALL_FONT = 24
# MED_FONT = 32
# LARGE_FONT = 48


class FontSize(enum.IntEnum):
    SMALL = 20
    MEDIUM = 24
    LARGE = 32


class Time():
    FAST = 0.5
    STANDARD = 1
    SLOW = 1.5
    # The delay to display at the end of an animation.
    END = 3


def center_and_scale(object: Mobject) -> Mobject:
    """
    Centers and scales an object so it lies in the center of the screen.
    """
    pass
