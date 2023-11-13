import numpy as np
import bezier

Point_T = tuple[int, int]
BezierPoints_T = tuple[Point_T, Point_T, Point_T]


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


def calculate_bezier_points_and_angles(p0, p1, p2, num_points=100):
    """Calculate points and angles on the quadratic Bezier curve defined by points p0, p1, and p2."""
    bezier_points = []
    angles = []
    t_values = np.linspace(0, 1, num_points)

    # Helper function to calculate the tangent
    def tangent(t, p0, p1, p2):
        return 2 * (1 - t) * (np.array(p1) - np.array(p0)) + 2 * t * (
            np.array(p2) - np.array(p1)
        )

    for i, t in enumerate(t_values):
        point = (
            (1 - t) ** 2 * np.array(p0)
            + 2 * (1 - t) * t * np.array(p1)
            + t**2 * np.array(p2)
        )
        bezier_points.append(point.astype(int))

        # Calculate angle of curvature
        if 0 < i < len(t_values) - 1:
            t_prev = t_values[i - 1]
            t_next = t_values[i + 1]

            # Calculate tangent vectors
            tangent_prev = tangent(t_prev, p0, p1, p2)
            tangent_next = tangent(t_next, p0, p1, p2)

            # Calculate the angle between tangents
            angle = np.arccos(
                np.dot(tangent_prev, tangent_next)
                / (np.linalg.norm(tangent_prev) * np.linalg.norm(tangent_next))
            )
            angle = np.degrees(angle)  # Convert to degrees if preferred
            angles.append(angle)

    # Edge cases for the first and last points where we do not have a previous or next point
    angles.insert(0, angles[0])  # Repeat the first calculable angle
    angles.append(angles[-1])  # Repeat the last calculable angle

    return bezier_points, angles


def points_to_bezier(points: BezierPoints_T) -> bezier.Curve:
    """
    Convert a tuple of three points to a bezier curve.
    """
    p1, p2, p3 = points

    # Get the x and y coordinates of the points
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    nodes = np.asfortranarray([x, y])

    curve = bezier.Curve(nodes, degree=2)

    return curve


def calculate_ctr_point(
    start_point: Point_T, end_point: Point_T, scale: float = 1.0
) -> Point_T:
    """
    Calculate the control point for the next curve.
    Ctrl_point should be on the line from p1 through end_point, we scale the vector if needed
    """
    v = np.array(end_point) - np.array(start_point)
    ctr_point = np.array(end_point) + v * scale

    return ctr_point.tolist()
