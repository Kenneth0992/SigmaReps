"""
utils.py — shared geometry helpers used by every exercise module
"""

import numpy as np


def get_coords(landmarks, landmark_enum, name: str):
    """Return (x, y) for a named landmark."""
    lm = landmarks[landmark_enum[name].value]
    return np.array([lm.x, lm.y])


def angle_between(a, b, c) -> float:
    """
    Calculate the angle (degrees) at point B formed by A-B-C.
    a, b, c are np.arrays of (x, y).
    """
    ba = a - b
    bc = c - b
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    return float(np.degrees(np.arccos(cos_angle)))


def midpoint(a, b):
    """Return the midpoint between two (x,y) arrays."""
    return (a + b) / 2
