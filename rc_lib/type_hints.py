"""
    A collection of semantic aliases for type hinting used throughout the library.

    These should remain collected in a module namespace, rather than being
    put in to the global namespace, as some names may overlap with those
    used in the library.
"""
from manim import *
import numpy as np

__all__ = []  # no public names, access via module namespace

Vector = np.ndarray
# Means it has the semantic meaning of a 2d vector.
# Even in 2d spaces manim prefers to use 3d vectors.
Vector2D = np.ndarray
Vector3D = np.ndarray

Point = np.ndarray
# Means it has the semantic meaning of a 2d point, not that it has dimension 2.
Point2D = np.ndarray
Point3D = np.ndarray
