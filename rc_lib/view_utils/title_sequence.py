from manim import *
from typing import List

from rc_lib import style

__all__ = ["TitleSequence"]


class TitleSequence:
    """
    A class which provides a utility for displaying sequential titles in a step-by-step animation.
    """

    def __init__(
        self, add_numbers: bool = True, default_color: style.Color = style.DEFAULT_COLOR
    ) -> None:
        self._add_numbers = add_numbers
        self._default_color = default_color
        self._number = 1

    def reset(self) -> None:
        """
        Resets the class. Allows the same title_sequence to be used across multiple animations.
        """
        self._number = 1

    def next(self, title: str, color: style.Color | None = None) -> Animation:
        text = self._make_text(title, self._default_color if color is None else color)
        self._number += 1
        if self._number == 2:
            self._first = text
            return Write(self._first, run_time=0.75)
        else:
            return Transform(self._first, text, run_time=0.75)

    def _make_text(self, title: str, color: style.Color) -> Text:
        prefix = str(self._number) + ": " if self._add_numbers else ""
        return Text(prefix + title, color=color).to_corner(UP + LEFT)
