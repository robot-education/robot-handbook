import manim
import numpy as np

import rc_lib.style as T


def norm(point: T.Point2d | T.Point3d) -> float:
    return np.linalg.norm(point)


def normalize(vector: T.Vector2d) -> T.Direction2d:
    return manim.normalize(vector)


def normalize(vector: T.Vector3d) -> T.Direction3d:
    return manim.normalize(vector)


def dot(vector1: T.Vector2d, vector2: T.Vector2d) -> T.Vector2d:
    return np.dot(vector1, vector2)


def dot(vector1: T.Vector3d, vector2: T.Vector3d) -> T.Vector3d:
    return np.dot(vector1, vector2)


def point_2d(x: float, y: float) -> T.Point2d:
    """
    A constructor for a point2d.
    """
    return np.array([x, y, 0])


def point_3d(x: float, y: float, z: float) -> T.Point3d:
    """
    A constructor for a point3d.
    """
    return np.array([x, y, z])
