from manim import *
from typing import NewType
from manim.utils.color import Colors
import enum

Color = str


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
