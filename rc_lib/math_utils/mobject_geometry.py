import manim as mn
import numpy as np
from rc_lib.math_utils import vector


def get_smooth_boundary_point(
    mobject: mn.VMobject, direction: vector.Direction2d
) -> vector.Point2d:
    """Returns a point on the boundary of the mobject in the given direction.

    Manim has a number of methods for finding the boundary of a mobject, but
    they rely on finding corners/bounding boxes- the resulting point isn't
    continuous for changes in direction.

    This method instead fits a bounding ellipse to the mobject, and smoothly
    finds points on the boundary of that ellipse: continuity is guaranteed.

    Only implemented and tested for 2D Mobjects.

    Args:
        mobject: The mobject to find the boundary point of.
        direction: The direction to find the boundary point in. Must be a
            unit vector to find true boundary points: scaling the vector
            will scale the resulting point radially from the center of the
            mobject.
    """
    # Start at center
    border_point = vector.Point2d(mobject.get_center())

    # project direction onto the axes for two of the corners of the bounding box,
    # get their vectors, and add them to get the border point vector in the
    # given direction.
    # Note: relies on symmetry that corner(dir) = -corner(-dir) when viewed from the
    # center of the mobject. If the corners no longer show rectangular symmetry
    # a new method will need to be found.
    basis = [(mn.UP + mn.RIGHT) / np.sqrt(2), (mn.UP + mn.LEFT) / np.sqrt(2)]
    for project_direction in basis:
        component = vector.dot(direction, project_direction)
        corner = mobject.get_corner(project_direction) - mobject.get_center()
        border_point += component * corner

    return border_point
