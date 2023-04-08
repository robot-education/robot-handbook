import manim as mn
from rc_lib.style import color
from rc_lib.design import sketch


class Click(mn.Succession):
    """Defines an animation which represents an object getting clicked."""

    Z_INDEX = 500

    def __init__(self, mobject: mn.Mobject):
        target = mobject.copy().set_stroke(width=4 * 3.5).set_color(color.Palette.YELLOW)  # type: ignore

        # set z_index to make highlight go over the top (a bit suss)
        mobject.set_z_index(self.Z_INDEX)
        self.Z_INDEX += 1

        super().__init__(
            mn.Transform(mobject, target, rate_func=mn.there_and_back, run_time=0.75)
        )
