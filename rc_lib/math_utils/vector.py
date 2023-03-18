"""
    A collection of semantic aliases for type hinting used throughout the library.
"""
<<<<<<< HEAD
import manim as mn
import numpy as np
from typing import Any
=======
from typing import cast

import manim as mn
import numpy as np
>>>>>>> 69e9e27 (Fixed typing errors and updated to refactored style)

Vector = np.ndarray
# For compatability with manim, a 2d vector is defined as 3d vector with its third coordinate equal to zero.
Vector2d = np.ndarray
Vector3d = np.ndarray

Point = np.ndarray
# For compatability with manim, a 2d point is defined as a 3d point with its third coordinate equal to zero.
Point2d = np.ndarray
Point3d = np.ndarray

Direction = np.ndarray
Direction2d = np.ndarray
Direction3d = np.ndarray


<<<<<<< HEAD
def norm(point: Point | Vector) -> np.floating[Any]:
    return np.linalg.norm(point)
=======
def norm(point: Point | Vector) -> float:
    return cast(float, np.linalg.norm(point))
>>>>>>> 69e9e27 (Fixed typing errors and updated to refactored style)


def normalize(vector: Vector) -> Direction:
    return mn.normalize(vector)


def dot(vector1: Vector, vector2: Vector) -> Vector:
    return np.dot(vector1, vector2)


<<<<<<< HEAD
def vector_2d(x: float, y: float) -> Vector2d:
    """A constructor for a vector2d."""
    return np.array([x, y, 0])


def vector_3d(x: float, y: float, z: float) -> Vector3d:
    """A constructor for a vector3d."""
    return np.array([x, y, z])


def point_2d(x: float, y: float) -> Point2d:
    """A constructor for a point2d."""
=======
def point_2d(x: float, y: float) -> Point2d:
    """
    A constructor for a point2d.
    """
>>>>>>> 69e9e27 (Fixed typing errors and updated to refactored style)
    return np.array([x, y, 0])


def point_3d(x: float, y: float, z: float) -> Point3d:
<<<<<<< HEAD
    """A constructor for a point3d."""
    return np.array([x, y, z])

def angle_between(x1: Vector, x2: Vector) -> float:
    # mn.angle_between_vectors is incorrectly typed as np.ndarray, not float
    return mn.angle_between_vectors(x1, x2)  # type: ignore

def angle_between_points(start: Point, end: Point, center: Point) -> float:
    return angle_between(start - center, end - center)
=======
    """
    A constructor for a point3d.
    """
    return np.array([x, y, z])
>>>>>>> 69e9e27 (Fixed typing errors and updated to refactored style)
