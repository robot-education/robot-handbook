from abc import ABC
from typing import Any, Iterable
import manim as mn

from rc_lib.common_mobjects import sketch
from rc_lib.style import animation


class SketchScene(mn.Scene, ABC):
    CONSTRAINT_DELAY = 0.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # rebind construct so that the manim compiler is happy
        # self._child_construct = self.construct
        # self.construct = self._construct_sketch

        self._static_mobjects: Iterable[sketch.Sketch] = []

    def introduce(self, *mobjects: sketch.Sketch):
        self._static_mobjects = mobjects

        self.play(
            mn.AnimationGroup(
                *[mn.Create(mobject) for mobject in self._static_mobjects]
            )
        )
        self.wait(self.CONSTRAINT_DELAY)

    def run_group(self, *animation: mn.Animation | Any):
        self.play(mn.Succession(*animation))
        self.wait(self.CONSTRAINT_DELAY)

    def tear_down(self):
        self.wait(animation.END_DELAY - self.CONSTRAINT_DELAY)

        self.play(
            mn.AnimationGroup(
                *[mn.Uncreate(mobject) for mobject in self._static_mobjects]
            )
        )
        self.wait(self.CONSTRAINT_DELAY * 1.5)
