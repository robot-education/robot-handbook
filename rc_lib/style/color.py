from manim import *
from typing import NewType
from manim.utils.color import Colors
import enum


Color = NewType("Color", str)

class Palette(enum.StrEnum):
    RED = Colors.red_c.value
    GREEN = Colors.green_d.value
    BLUE = Colors.blue_d.value
    YELLOW = Colors.yellow_e.value
    WHITE = Colors.white.value


FOREGROUND = Palette.WHITE

