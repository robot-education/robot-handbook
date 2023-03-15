"""
    A collection of semantic aliases for type hinting used throughout the library.
"""
import manim as mn
import numpy as np
from typing import NewType

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

def norm(point: Point | Vector) -> float:
    return np.linalg.norm(point)


def normalize(vector: Vector) -> Direction:
    return mn.normalize(vector)

def dot(vector1: Vector, vector2: Vector) -> Vector:
    return np.dot(vector1, vector2)

def point_2d(x: float, y: float) -> Point2d:
    """
    A constructor for a point2d.
    """
    return np.array([x, y, 0])


def point_3d(x: float, y: float, z: float) -> Point3d:
    """
    A constructor for a point3d.
    """
    return np.array([x, y, z])