import numpy as np


# Useful constants
# Pauli matrices
pauli_x = np.array([[0, 1], [1, 0]])
paily_y = np.array([[0, -1j], [1j, 0]])
pauli_z = np.array([[1, 0], [0, -1]])

# Levi-Civita symbol (for cross products and similar operations)


def levi_civita(i, j, k):
    """Return the Levi-Civita symbol for the given indices."""
    if max(i, j, k) > 2 or min(i, j, k) < 0:
        raise ValueError('Indices must be between 0 and 2 inclusive.')
    if i == j or j == k or i == k:
        return 0

    order = np.array([i, j, k])
    start = np.argmin(order)
    order = np.roll(order, -start)

    return 1 if np.array_equal(order, [0, 1, 2]) else -1


# Conversion between right-handed coordinate systems
# (x, y, z), (z, x, y), (y, z, x).
# All coordinate systems are transformed in the same way, with a
# rotate_right and rotate_left operation.
rotate_coords_right = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
rotate_coords_left = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])


# Rotation matrices
def rotation_matrix_2d(angle):
    """Return the rotation matrix for a 2D rotation by angle."""
    return np.cos(angle) * np.eye(2) + np.sin(angle) * np.array([[0, -1], [1, 0]])


def rotation_z(angle):
    """Return the rotation matrix for a rotation around the z axis."""
    r2d = rotation_matrix_2d(angle)
    r3d = np.pad(r2d, ((0, 1), (0, 1)), 'constant', constant_values=0)
    r3d[2, 2] = 1

    return r3d


def rotation_x(angle):
    """Return the rotation matrix for a rotation around the x axis."""

    return rotate_coords_right @ rotation_z(angle) @ rotate_coords_left


def rotation_y(angle):
    """Return the rotation matrix for a rotation around the y axis."""

    return rotate_coords_left @ rotation_z(angle) @ rotate_coords_right


def rotation_3d(axis, angle=None):
    """Return the rotation matrix for a rotation around the axis by angle.
    If angle is None, the magnitude of the axis vector is used.
    """

    # A good explanation of the process can be found here:
    # https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle
    # The gist is to move to a coordinate system where the rotation axis is
    # the z axis (or a different axis if you prefer), then rotate around the
    # z axis, then move back to the original coordinate system.
    # We will simply use the formula provided in the Wikipedia article.

    if np.linalg.norm(axis) == 0:
        if angle is not None and angle != 0:
            raise ValueError(
                'Cannot rotate around zero vector by non-zero angle.')
        return np.eye(3)

    if angle is None:
        angle = np.linalg.norm(axis)

    axis = axis / np.linalg.norm(axis)

    outer_matrix = np.outer(axis, axis)
    cross_matrix = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            cross_matrix[i, j] = sum(
                levi_civita(k, i, j) * axis[k] for k in range(3))

    c, s = np.cos(angle), np.sin(angle)
    R = c * np.eye(3)
    R += s * cross_matrix
    R += (1 - c) * outer_matrix

    return R
