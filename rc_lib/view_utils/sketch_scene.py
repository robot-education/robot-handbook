from abc import ABC, abstractmethod
from typing import List
import manim as mn

from rc_lib.common_mobjects import sketch
from rc_lib.style import animation


class SketchScene(mn.Scene, ABC):
    CONSTRAINT_DELAY = 0.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # rebind construct so that the manim compiler is happy
        self._child_construct = self.construct
        self.construct = self._construct_sketch

        self._static_mobjects: List[sketch.Sketch] = []

    def set_static_mobjects(self, *mobjects: sketch.Sketch):
        self._static_mobjects.extend(mobjects)

    def run_group(self, *animation: mn.Animation):
        self.play(mn.Succession(*animation))
        self.wait(self.CONSTRAINT_DELAY)

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def construct(self) -> None:
        raise NotImplementedError

    def tear_down(self):
        self.wait(animation.END_DELAY - self.CONSTRAINT_DELAY)

        # Prevents bug where circles would sometimes not shrink
        # a_lot = 999999
        # [mobject.set_z_index(a_lot := a_lot + 1) for mobject in self._static_mobjects]

        self.play(
            mn.AnimationGroup(
                *[mobject.uncreate() for mobject in self._static_mobjects]
            )
        )
        self.wait(self.CONSTRAINT_DELAY * 1.5)

    def _construct_sketch(self):
        self._setup_sketch()
        self._child_construct()

    def _setup_sketch(self):
        self.play(
            mn.AnimationGroup(*[mobject.create() for mobject in self._static_mobjects])
        )
        self.wait(self.CONSTRAINT_DELAY)
