import numpy as np
import sympy as sp

import bezier

Point_T = tuple[float, float]
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
    prev_bezier: BezierPoints_T, end_point: Point_T, scale: float = 1.0
) -> Point_T:
    """
    Calculate the control point for the next curve.
    Ctrl_point should be on the line from p1 through end_point, we scale the vector if needed
    """
    p2 = prev_bezier[1]
    v = np.array(end_point) - np.array(p2)
    ctr_point = np.array(end_point) + v * scale

    return ctr_point.tolist()


def curvature_of_bezier(curve: bezier.Curve, s_values: np.ndarray):
    curvatures = []
    for s in np.nditer(s_values):
        first_derivative = curve.evaluate_hodograph(s)
        second_derivative = curve.evaluate_hodograph(s, derivative=2)

        x_prime, y_prime = first_derivative[0, 0], first_derivative[1, 0]
        x_double_prime, y_double_prime = (
            second_derivative[0, 0],
            second_derivative[1, 0],
        )

        numerator = abs(x_prime * y_double_prime - y_prime * x_double_prime)
        denominator = (x_prime**2 + y_prime**2) ** 1.5

        curvature = numerator / denominator if denominator != 0 else 0
        curvatures.append(curvature)

    return np.array(curvatures)


def calculate_curvature(curve: bezier.Curve, s_values: np.ndarray):
    # Convert the curve to a symbolic representation
    symbolic_curve = curve.to_symbolic()

    # Derive the first and second derivatives
    x, y = symbolic_curve
    s = sp.symbols("s")
    x_prime = sp.diff(x, s)
    y_prime = sp.diff(y, s)
    x_double_prime = sp.diff(x_prime, s)
    y_double_prime = sp.diff(y_prime, s)

    # Define curvature calculation function
    curvature_function = sp.lambdify(
        s,
        (x_prime * y_double_prime - y_prime * x_double_prime)
        / ((x_prime**2 + y_prime**2) ** 1.5),
        "numpy",
    )

    # Compute curvature for each s value
    curvatures = curvature_function(s_values)

    return np.array(curvatures)
