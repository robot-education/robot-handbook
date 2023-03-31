"""
Style elements intrinsically linked with animation, such as timing.
"""
import manim as mn
from rc_lib.style import color
from rc_lib.math_utils import vector

END_DELAY = 2.5


class ShrinkToPoint(mn.Transform):
    def __init__(
        self,
        mobject: mn.Mobject,
        point: vector.Point2d,
        point_color: color.Color | None = None,
        **kwargs
    ) -> None:
        self.point = point
        self.point_color = point_color
        super().__init__(
            mobject,
            remover=True,
            introducer=False,
            reverse_rate_function=True,
            **kwargs
        )

    def create_target(self) -> mn.Mobject:
        return self.mobject

    def create_starting_mobject(self) -> mn.Mobject:
        start = super().create_starting_mobject()
        start.scale(0).move_to(self.point)
        if self.point_color:
            start.set_color(self.point_color)  # type: ignore
        return start


class ShrinkToCenter(ShrinkToPoint):
    """Remove an :class:`~.Mobject` by shrinking it to a point."""

    def __init__(
        self, mobject: mn.Mobject, point_color: color.Color | None = None, **kwargs
    ) -> None:
        super().__init__(
            mobject, point=mobject.get_center(), point_color=point_color, **kwargs
        )
