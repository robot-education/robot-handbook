from manim import *
from typing import List

from rc_lib import style

__all__ = ["SequentialTitle"]


class SequentialTitle(Text):
    """
    A class which provides a utility for displaying sequential titles in a step-by-step animation.
    """

    def __init__(self, titles: List[str]) -> None:
        # titles = [(str(i + 1) + ": " + title) for i,
        #           title in enumerate(titles)]
        self._titles = [Text(title, font_size=42) for title in titles]
        # (title.to_corner(UP + LEFT) for title in self._titles)
        self._index = -1
        super().__init__(self._titles[0])

    def next(self) -> Animation:
        self._index += 1
        if (self._index == 0):
            return Create(self)
        else:
            return Transform(self, self._titles[self._index])
