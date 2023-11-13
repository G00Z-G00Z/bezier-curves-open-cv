import matplotlib.pyplot as plt
import numpy as np
import bezier
from bezier_lib.bezier_calc import (
    calculate_bezier_points,
    calculate_bezier_points_and_angles,
    Point_T,
    BezierPoints_T,
    calculate_ctr_point,
    points_to_bezier,
)


# Random waypoints for generating curves
waypoints: list[Point_T] = [
    (0, 0),
    (1, 1),
    (2, 0),
    (3, 1),
    (4, 0),
    (5, 1),
    (6, 0),
    (7, 1),
]


curves: list[bezier.Curve] = []

for i in range(1, len(waypoints)):
    p1 = waypoints[i - 1]
    p3 = waypoints[i]
    ctr = calculate_ctr_point(p1, p3)
    curve = points_to_bezier(p1, ctr, p3)
    curves.append(curve)


# Plot both curves
s_vals = np.linspace(0, 1, 100)

# Plot all the curves
for curve in curves:
    points = curve.evaluate_multi(s_vals)
    plt.plot(points[0, :], points[1, :])


# points1 = curve1.evaluate_multi(s_vals)
# points2 = curve2.evaluate_multi(s_vals)

# plt.plot(points1[0, :], points1[1, :], label="First Bezier Curve")
# plt.plot(points2[0, :], points2[1, :], label="Second Bezier Curve")
# plt.scatter(
#     nodes1[0, :], nodes1[1, :], color="red", label="Control Points of First Curve"
# )
# plt.scatter(
#     nodes2[0, :], nodes2[1, :], color="green", label="Control Points of Second Curve"
# )
plt.legend()
plt.show()
