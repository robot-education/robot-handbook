from abc import ABC, abstractmethod
import manim as mn

from rc_lib.common_mobjects import sketch
from rc_lib.style import animation


class SketchScene(mn.Scene, ABC):
    CONSTRAINT_DELAY = 0.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # rebind construct so that the manim compiler is happy
        self._child_construct = self.construct
        self.construct = self._sketch_construct

        self._groups = []
        self._static_mobjects = []

    def set_static_mobjects(self, *mobjects: sketch.Sketch):
        self._static_mobjects = mobjects

    def run_group(self, *animation: mn.Animation):
        self.play(mn.Succession(*animation))
        self.wait(self.CONSTRAINT_DELAY)

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def construct(self) -> None:
        raise NotImplementedError

    def _sketch_construct(self):
        self._begin()
        self._child_construct()
        self._end()

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