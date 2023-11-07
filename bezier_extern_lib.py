import bezier
import numpy as np
import matplotlib.pyplot as plt

# Define the nodes of the Bezier curve
nodes = np.asfortranarray(
    [
        [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],  # x-coordinates
        [0.0, 0.5, 0.3, 0.6, 0.2, 0.5],  # y-coordinates
    ]
)

# Create a Bezier curve from the nodes
curve = bezier.Curve(nodes, degree=3)

# Evaluate points on the curve
s_vals = np.linspace(0, 1, 100)
points = curve.evaluate_multi(s_vals)

# Plot the curve
plt.plot(points[0, :], points[1, :], label="Bezier Curve")
plt.scatter(nodes[0, :], nodes[1, :], color="red", label="Control Points")
plt.legend()
plt.show()
