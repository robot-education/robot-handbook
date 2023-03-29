"""
    Style elements intrinsically linked with animation, such as timing.
"""
import manim as mn


END_DELAY = 2.5


class ShrinkToCenter(mn.Transform):
    """Remove an :class:`~.Mobject` by shrinking it to a point."""

    def __init__(
        self, mobject: mn.Mobject, point_color: str | None = None, **kwargs
    ) -> None:
        self.point = mobject.get_center()
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
        start.scale(0)
        start.move_to(self.point)
        if self.point_color:
            start.set_color(self.point_color)  # type: ignore
        return start
