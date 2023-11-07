import matplotlib.pyplot as plt
import numpy as np
import bezier

# Define the nodes for the first quadratic Bezier curve
nodes1 = np.asfortranarray(
    [
        [0.0, 0.5, 1.0],  # x-coordinates
        [0.0, 1.0, 0.0],  # y-coordinates
    ]
)

# Create the first Bezier curve
curve1 = bezier.Curve(nodes1, degree=2)

# Define the nodes for the second quadratic Bezier curve
# The first point (1.0, 0.0) is the same as the last point of the first curve
# The second point (1.5, -1.0) is chosen to ensure the gradient is continuous
# The third point (2.0, 0.0) is the end point of the second curve
nodes2 = np.asfortranarray(
    [
        [1.0, 1.5, 2.0],  # x-coordinates
        [0.0, -1.0, 0.0],  # y-coordinates
    ]
)

# Create the second Bezier curve
curve2 = bezier.Curve(nodes2, degree=2)

# Plot both curves
s_vals = np.linspace(0, 1, 100)
points1 = curve1.evaluate_multi(s_vals)
points2 = curve2.evaluate_multi(s_vals)

plt.plot(points1[0, :], points1[1, :], label="First Bezier Curve")
plt.plot(points2[0, :], points2[1, :], label="Second Bezier Curve")
plt.scatter(
    nodes1[0, :], nodes1[1, :], color="red", label="Control Points of First Curve"
)
plt.scatter(
    nodes2[0, :], nodes2[1, :], color="green", label="Control Points of Second Curve"
)
plt.legend()
plt.show()
