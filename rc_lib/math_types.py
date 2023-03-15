"""
    A collection of semantic aliases for type hinting used throughout the library.

    These should remain collected in a module namespace, rather than being
    put in to the global namespace, as some names may overlap with those
    used in the library.
"""
import numpy as np
from typing import NewType

# To avoid conflicts with manim, we do not have any public names
__all__ = []

Vector = NewType("Vector", np.ndarray)
# For compatability with manim, a 2d vector is defined as 3d vector with its third coordinate equal to zero.
Vector2d = NewType("Vector2d", np.ndarray)
Vector3d = NewType("Vector3d", np.ndarray)

Point = NewType("Point", np.ndarray)
# For compatability with manim, a 2d point is defined as a 3d point with its third coordinate equal to zero.
Point2d = NewType("Point2d", np.ndarray)
Point3d = NewType("Point3d", np.ndarray)

Direction2d = NewType("Direction2d", np.ndarray)
Direction3d = NewType("Direction3d", np.ndarray)
