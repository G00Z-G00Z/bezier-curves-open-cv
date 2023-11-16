import numpy as np
import sympy as sp

import bezier

Point_T = tuple[float, float]
BezierPoints_T = tuple[Point_T, Point_T, Point_T]


def points_to_bezier(points: BezierPoints_T) -> bezier.Curve:
    """
    Convert a tuple of three points to a bezier curve.
    """

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


def from_waypoints_ctr_to_bezier(
    waypoints: list[Point_T], ctr_points: list[Point_T], scale: float = 1.0
) -> list[BezierPoints_T]:
    # Check that the number of points and control points match
    if len(waypoints) != len(ctr_points):
        raise ValueError("Number of points and control points must match")

    # Create a list of bezier curves
    bezier_curves = []

    # Iterate over the points and control points
    for i in range(1, len(waypoints)):
        prev_point = waypoints[i - 1]
        prev_ctr_point = ctr_points[i - 1]
        point = waypoints[i]

        bezier_curve: BezierPoints_T = (prev_point, prev_ctr_point, point)
        bezier_curves.append(bezier_curve)

    return bezier_curves
