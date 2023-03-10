from manim import *
from typing import List

from rc_lib import style

__all__ = ["TitleSequence"]


class TitleSequence():
    """
    A class which provides a utility for displaying sequential titles in a step-by-step animation.
    """
    def __init__(self, titles: List[str]) -> None:
        self._titles = [Text(str(i + 1) + ": " + title).to_corner(UP + LEFT)
            for i, title in enumerate(titles)]
        self._index = -1
        # super().__init__(self._titles[0])

    def next(self) -> Animation:
        self._index += 1
        if (self._index == 0):
            return Write(self._titles[0])
        else:
            return Transform(self._titles[0], self._titles[self._index])
