"""
    Mobject groups with available layout methods.
"""
from typing import List

from manim import *
from rc_lib.common_mobjects.containers import OrderedVGroup

from rc_lib.math_utils.mobject_geometry import get_smooth_boundary_point

__all__ = [
    "LinearLayout"
]

normalize_vector = normalize  # alias


def edge_from_center(mobject, direction):
    """ Returns a vector for the edge, rather than an apsolute position. 
        Translational invariant version of get_smooth_boundary_point.
    """
    return get_smooth_boundary_point(mobject, direction) - mobject.get_center()


class LinearLayout(OrderedVGroup):
    """ A VGroup that arranges its elements in order along a given direction.

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

    def __init__(self, *mobjects, direction=DOWN):
        VGroup.__init__(self, *mobjects)
        self.set_direction(direction)

    def set_direction(self, direction):
        """ Sets the default direction for the layout. 

        This may be overridden by specific calls to arrange, and does not
        automatically update the layout- arrange must be called (manually or
        via an updater) to update the layout.
        """
        self.direction = direction
        return self

    def predict_arrangement(self, direction=None, root=None, normalize=True,
                            padding=0.0):
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
            direction = normalize_vector(direction)

        if root is None:
            root = self[0].get_center()

        positions = [root]

        pad_vector = padding * direction

        for i in range(1, len(self)):
            # Find and match points on the edges of the mobjects boundaries.
            # Use smooth boundaries for correct behavior along any given axis.
            prev_edge = edge_from_center(self[i - 1], direction)
            curr_edge_to_center = -edge_from_center(self[i], -direction)

            new_pos = positions[i - 1] + prev_edge + \
                curr_edge_to_center + pad_vector
            positions.append(new_pos)

        return positions

    def arrange(self, positions=None):
        """ Instantaneously updates the layout along the given direction, as
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

    def animate_arrange(self, anim_function=None,
                        positions=None) -> List[Animation]:
        """
        Returns an animation of the layout being updated to its predicted 
        arrangement.

        Args:
            anim_function(mobject, position): returns an animation that moves
                the mobject to the given position. By default, this moves 
                the mobject linearly (manim.animation.transform.Transform).
            positions: The positions to move the mobjects to. If None, the
                positions are predicted using predict_arrangement().
        """
        def _move_mob_to_pos(mob: VMobject, pos: np.ndarray) -> Animation:
            return mob.animate.move_to(pos)

        if positions is None:
            positions = self.predict_arrangement()

        if anim_function is None:
            anim_function = _move_mob_to_pos

        return [anim_function(self[i], positions[i]) for i in range(len(self))]
