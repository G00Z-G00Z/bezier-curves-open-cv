import matplotlib.pyplot as plt
import numpy as np
import bezier


def calculate_control_point(P1, P2, scale=1):
    # Vector from P1 to P2
    v = np.array(P2) - np.array(P1)
    # P3 should be on the line from P1 through P2, we scale the vector if needed
    P3 = np.array(P2) + scale * v
    return P3.tolist()


# Define the nodes for the first quadratic Bezier curve
nodes1 = np.asfortranarray(
    [
        [0.0, 0.5, 1.0],  # x-coordinates
        [0.0, 1.0, 0.0],  # y-coordinates
    ]
)

# Create the first Bezier curve
curve1 = bezier.Curve(nodes1, degree=2)

# The end point of the first curve and start of the second curve
P2 = nodes1[:, -1]

# Define the end control point of the second curve
P4 = [4.0, 10.0]

# Calculate the control point P3 for the second Bezier curve
P3 = calculate_control_point(nodes1[:, 1], P2)

# Define the nodes for the second quadratic Bezier curve
nodes2 = np.asfortranarray(
    [[P2[0], P3[0], P4[0]], [P2[1], P3[1], P4[1]]]  # x-coordinates  # y-coordinates
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
