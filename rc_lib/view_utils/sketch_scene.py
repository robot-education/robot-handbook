from abc import ABC, abstractmethod
from typing import List
import manim as mn

from rc_lib.common_mobjects import sketch
from rc_lib.style import animation


class SketchScene(mn.Scene, ABC):
    CONSTRAINT_DELAY = 0.5
    # def add_mobjects(self, mobject_dict: Dict[str, sketch.Sketch]):
    #     self._set_mobjects(mobject_dict.values())
    #     [setattr(self, k, v) for k, v in mobject_dict]

    def set_static_mobjects(self, *mobjects: sketch.Sketch):
        self._static_mobjects = mobjects

    def _begin(self):
        self.play(
            mn.AnimationGroup(*[mobject.create() for mobject in self._static_mobjects])
        )
        self.wait(self.CONSTRAINT_DELAY)

    def _end(self):
        self.wait(animation.END_DELAY - self.CONSTRAINT_DELAY)
        self.play(
            mn.AnimationGroup(
                *[mobject.uncreate() for mobject in self._static_mobjects]
            )
        )
        self.wait(self.CONSTRAINT_DELAY * 2)

    @abstractmethod
    def make_animations(self) -> List[List[mn.Animation]]:
        raise NotImplementedError

    def construct(self):
        self._begin()
        for group in self.make_animations():
            self.play(mn.Succession(*group))
            self.wait(self.CONSTRAINT_DELAY)
        self._end()
