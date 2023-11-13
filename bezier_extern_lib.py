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
waypoints: list[Point_T] = [(0, 0), (4, 10), (5, 8), (7, 12), (10, 5), (7, 3), (0, 0)]


# First ctr point will be the first waypoint
first_ctr_point = (np.array(waypoints[1]) + np.array(waypoints[0])) / 2
ctr_points: list[Point_T] = [first_ctr_point]
curves: list[bezier.Curve] = []


for i in range(1, len(waypoints)):
    ctr_point = ctr_points[i - 1]
    p1 = waypoints[i - 1]
    p2 = waypoints[i]
    bezier_points: BezierPoints_T = (p1, ctr_point, p2)
    curve = points_to_bezier(bezier_points)
    curves.append(curve)

    # Calculate next ctr point
    new_ctr_point = calculate_ctr_point(bezier_points, p2, scale=1)
    ctr_points.append(new_ctr_point)


# Plot both curves
s_vals = np.linspace(0, 1, 100)

# # Plot all the curves
for curve in curves:
    points = curve.evaluate_multi(s_vals)
    plt.plot(points[0, :], points[1, :])


# # points1 = curve1.evaluate_multi(s_vals)
# # points2 = curve2.evaluate_multi(s_vals)

# # plt.plot(points1[0, :], points1[1, :], label="First Bezier Curve")
# # plt.plot(points2[0, :], points2[1, :], label="Second Bezier Curve")
# # plt.scatter(
# #     nodes1[0, :], nodes1[1, :], color="red", label="Control Points of First Curve"
# # )
# # plt.scatter(
# #     nodes2[0, :], nodes2[1, :], color="green", label="Control Points of Second Curve"
# # )
plt.grid()
plt.show()
