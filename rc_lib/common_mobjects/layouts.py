"""
    Mobject groups with available layout methods.
"""
from typing import Callable, List, Any, Self, Tuple, cast

import manim as mn
from rc_lib.math_utils import vector, mobject_geometry
from rc_lib.common_mobjects import containers


def edge_from_center(
    mobject: mn.VMobject, direction: vector.Vector2d
) -> vector.Vector2d:
    """Returns a vector for the edge, rather than an absolute position.
    Translational invariant version of get_smooth_boundary_point.
    """
    return (
        mobject_geometry.get_smooth_boundary_point(mobject, direction)
        - mobject.get_center()
    )


class Placeholder(mn.VMobject):
    """
    An invisible placeholder constructed to have an equivalent bounding box
    to a given mobject, referred to as the reservee. Useful for reserving
    space in a layout without yet joining it.

    Placeholders may be constructed from dimensions using
    `make_placeholder(width, height)`. In this case, the placeholder
    does not have a reservee, which may be specified later using set_reservee()

    Note that transformations to the placeholder do not effect the reservee
    and vice versa. To update a placeholder to meet the new dimensions of the
    reservee, call `self.fit()`

    Placeholders are considered equal if they are for the same reservee, even
    if their positions or dimensions are different. Placeholders with no
    reservee are not considered equal (unless they are the same object).
    """

    def __init__(self, reservee: mn.VMobject | None):
        """
        Creates a placeholder for reservee with equivalent bounding rectangle.

        If reservee is None, dimensions are defaulted to (1, 1).
        """
        super().__init__()
        # Initialize the invisible rectangle we will be using
        self._bounding_box = mn.Rectangle(
            height=1, width=1, stroke_opacity=0.0, fill_opacity=0.0
        )
        # If we register it as a sub-mobject, we will take on its boundaries
        self.add(self._bounding_box)

        self.set_reservee(reservee)

    def set_reservee(self, reservee: mn.VMobject | None) -> Self:
        """
        Sets a new reservee and updates the bounding box. Does not move the
        placeholder.

        If `reservee == None`, the reservee is cleared and no changes to the
        box are made.

        Returns self for chaining.
        """

        self.reservee = reservee

        if reservee != None:
            diagonal = reservee.get_corner(mn.UP + mn.RIGHT) - reservee.get_corner(
                mn.DOWN + mn.LEFT
            )
            width = diagonal[0]
            height = diagonal[1]
            self.set_dimensions(width, height)
        return self

    def set_dimensions(self, width: float, height: float) -> Self:
        """
        Sets the edge-to-edge dimensions of the placeholder. Does not move
        the center.

        Returns self for chaining.
        """
        self._bounding_box.stretch_to_fit_height(height)
        self._bounding_box.stretch_to_fit_width(width)
        return self

    def reserved_for(self, mob: mn.VMobject) -> bool:
        """
        Returns true if this placeholder is reserved for `mob`.

        A placeholder with no reservee is never considered to be reserved
        for anything even if `mob` is `None`.
        """
        return not (self.reservee == None) and (mob is self.reservee)

    def __eq__(self, other: Any):
        if self is other:
            return True

        if isinstance(other, Placeholder):
            if (not self.reservee == None) and self.reservee == other.reservee:
                return True

        return False

    def __hash__(self) -> int:
        return self._bounding_box.__hash__()


def make_placeholder(width: float, height: float) -> Placeholder:
    """
    Returns a placeholder of the given dimensions with no reservee.
    """
    return Placeholder(None).set_dimensions(width, height)


class LinearLayout(containers.OrderedVGroup):
    """
    A VGroup that arranges its elements in order along a given direction.

    Does not automatically update the layout. To use the layout, three primary
    methods are provided:
        predict_arrangement() - returns an ordered list of the positions that
            the mobjects would be placed at to satisfy the linear layout.
        arrange() - instantaneously updates the layout along the given direction,
            as according to predict_arrangement().
        animate_arrange() - returns an animation of the layout being updated to
            its predicted arrangement. By default, mobjects move linearly
            (manim.animation.transform.Transform) to their predicted positions:
            this can be changed by passing in a different animation class.
    """

    def __init__(self, *mobjects: mn.VMobject, direction=mn.DOWN):
        super().__init__(*mobjects)
        self.set_direction(direction)

    def set_direction(self, direction: vector.Vector2d) -> Self:
        """Sets the default direction for the layout.

        This may be overridden by specific calls to arrange, and does not
        automatically update the layout- arrange must be called (manually or
        via an updater) to update the layout.
        """
        self.direction = direction
        return self

    def predict_arrangement(
        self,
        direction: vector.Vector2d | None = None,
        root: vector.Point2d | None = None,
        normalize: bool = True,
        padding: float = 0.0,
    ) -> List[vector.Point2d]:
        """
        Returns a list of the predicted positions that the mobjects would be
        arranged at, in the order they have been placed in the layout.

        Args:
            direction: The direction to arrange the mobjects in. If None, the
                default direction is used.
            root: The position to place the center of the first mobject at.
                If None, the first mobject will not be moved.
            normalize: Whether to normalize the direction vector to a unit
                vector. If False, the magnitude of the direction vector will
                result in an equivalent linear scaling of the center placements
                along the axis.
            padding: The amount of space (proportional to the direction vector)
                to place between each mobject.
        """

        if direction is None:
            direction = self.direction

        if normalize:
            direction = vector.normalize(direction)

        if root is None:
            root = cast(vector.Point2d, self[0].get_center())

        positions: List[vector.Point2d] = [root]

        pad_vector = padding * direction

        for i in range(1, len(self)):
            # Find and match points on the edges of the mobjects boundaries.
            # Use smooth boundaries for correct behavior along any given axis.
            prev_edge = edge_from_center(self[i - 1], direction)
            curr_edge_to_center = -edge_from_center(self[i], -direction)

            new_pos = positions[i - 1] + prev_edge + curr_edge_to_center + pad_vector
            positions.append(new_pos)

        return positions

    def arrange(self, positions: List[vector.Point2d] | None = None) -> Self:
        """Instantaneously updates the layout along the given direction, as
        according to predict_arrangement().

        Args:
            positions: The positions to move the mobjects to. If None, the
                positions are predicted using predict_arrangement().

        Returns:
            self (for chaining)
        """
        if positions is None:
            positions = self.predict_arrangement()

        for i in range(len(self)):
            self[i].move_to(positions[i])

        return self

    def animate_arrange(
        self,
        anim_function: Callable[[mn.VMobject, vector.Point2d], mn.Animation]
        | None = None,
        positions: List[vector.Point2d] | None = None,
    ) -> List[mn.Animation]:
        """
        Returns an animation of the layout being updated to its predicted
        arrangement.

        Args:
            anim_function(mobject, position): returns an animation that moves
                the mobject to the given position. By default, this moves
                the mobject linearly (mobject.animate.move_to).
            positions: The positions to move the mobjects to. If None, the
                positions are predicted using predict_arrangement().
        """

        def _move_mob_to_pos(
            mobject: mn.VMobject, pos: vector.Vector2d
        ) -> mn.Animation:
            return mn.Transform(mobject, mobject.move_to(pos))

        if positions is None:
            positions = self.predict_arrangement()

        if anim_function is None:
            anim_function = _move_mob_to_pos

        return [anim_function(self[i], positions[i]) for i in range(len(self))]

    def replace_placeholder(self, reservee: mn.VMobject) -> Self:
        """
        Searches for a placeholder reserving reservee and replaces it with
        the reservee.

        Throws a value error if no placeholder found.
        """

        for i, sub_mob in enumerate(self):
            if isinstance(sub_mob, Placeholder):
                if sub_mob.reserved_for(reservee):
                    self[i] = reservee
                    return self

        raise ValueError("No placeholder found for reservee")