from ..bezier_calc import calculate_bezier_points
import matplotlib.pyplot as plt


def test_bezier_result():
    p0, p1, p2, num_points = (67, 288), (228, 95), (379, 302), 100

    cosa = calculate_bezier_points(p0, p1, p2, num_points)

    # Plot the points

    x = [i[0] for i in cosa]
    y = [i[1] for i in cosa]

    plt.plot(x, y, "ro")
    plt.show()

    print(cosa)
