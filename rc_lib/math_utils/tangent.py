from typing import List

from rc_lib import math_types as T
from rc_lib.math_utils import geometry

from math import acos, atan2, cos, sin

__all__ = ["circle_to_circle_tangent", "circle_to_point_tangent"]


def circle_to_circle_tangent(center1: T.Point2d, radius1: float, center2: T.Point2d, radius2: float) -> List[T.Point2d]:
    """
    Returns the outer tangent line between two circles.
    The tangent is such that it is on the (left) outside of 1 and 2 when they are arranged in clockwise fashion.
    To flip the tangent, flip the order of the circles.
    """
    dist = geometry.norm(center2 - center1)
    delta = (center2 - center1) / dist
    cross = geometry.point_2d(-delta[1], delta[0])
    alpha = (radius1 - radius2) / dist
    beta = (1 - alpha ** 2) ** 0.5
    return [
        T.Point2d(center1 + (alpha * delta + beta * cross) * radius1),
        T.Point2d(center2 + (alpha * delta + beta * cross) * radius2)
    ]


def circle_to_point_tangent(center: T.Point2d, radius: float, point: T.Point2d) -> T.Point2d:
    """
    Returns the outer tangent line between a circle and a point. 
    The tangent is such that it is on the outside when point is clockwise to center.
    To flip the tangent, pass point before center.
    """
    dist = geometry.norm(point - center)
    angle = acos(radius / dist)
    angle_offset = atan2(point[1] - center[1], point[0] - center[0])
    return geometry.point_2d(
        center[0] + radius * cos(angle_offset - angle),
        center[1] + radius * sin(angle_offset - angle)
    )


def circle_to_point_tangent(point: T.Point2d, center: T.Point2d, radius: float) -> T.Point2d:
    return circle_to_circle_tangent(center, -radius, point)
