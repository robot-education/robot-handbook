from manim import *
from typing import List, Optional

from rc_lib import style

__all__ = ["TitleSequence"]


class TitleSequence():
    """
    A class which provides a utility for displaying sequential titles in a step-by-step animation.
    """
    def __init__(self, add_numbers: Optional[bool] = False) -> None:
        self._add_numbers = add_numbers
        self._first = None
        self._number = 1
    
    def _make_text(self, title: str, color: style.Color) -> Text:
        prefix = str(self._number) + ": " if self._add_numbers else ""
        return Text(prefix + title, color=color).to_corner(UP + LEFT)

    def next(self, title: str, color: Optional[style.Color] = style.Color.WHITE) -> Animation:
        text = self._make_text(title, color)
        self._number += 1
        if (self._first == None):
            self._first = text
            return Write(self._first)
        else:
            return Transform(self._first, text)
