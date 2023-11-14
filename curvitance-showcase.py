import matplotlib.pyplot as plt
import numpy as np
import bezier
import sympy as sp
from bezier_lib.bezier_calc import calculate_curvature


# Define a Bezier curve with varying curvature
nodes = np.asfortranarray(
    [[0.0, 0.3, 0.6, 1.0], [0.0, 0.7, -0.7, 0.0]]  # x-coordinates  # y-coordinates
)
curve = bezier.Curve(nodes, degree=3)

# Calculate curvature
s_values = np.linspace(0, 1, 100)
curve_points = curve.evaluate_multi(s_values)
curvature_values = calculate_curvature(curve, s_values)

# Plot the curve and its curvature
fig, ax1 = plt.subplots()

# Plot curve
ax1.plot(curve_points[0, :], curve_points[1, :], "b-", label="Bezier Curve")
ax1.scatter(nodes[0, :], nodes[1, :], color="red", label="Control Points")
ax1.set_xlabel("x")
ax1.set_ylabel("y", color="b")
ax1.tick_params("y", colors="b")

# Plot curvature
ax2 = ax1.twinx()
ax2.plot(s_values, curvature_values, "r-", label="Curvature")
ax2.set_ylabel("Curvature", color="r")
ax2.tick_params("y", colors="r")

fig.tight_layout()
plt.legend()
plt.show()
