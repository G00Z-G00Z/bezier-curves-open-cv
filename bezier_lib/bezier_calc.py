import numpy as np


def calculate_bezier_points(p0, p1, p2, num_points=100):
    """Calculate `num_points` points on the quadratic Bezier curve defined by points p0, p1, and p2."""
    bezier_points = []
    t_values = np.linspace(0, 1, num_points)

    for t in t_values:
        point = (
            (1 - t) ** 2 * np.array(p0)
            + 2 * (1 - t) * t * np.array(p1)
            + t**2 * np.array(p2)
        )
        bezier_points.append(point.astype(int))

    return bezier_points
