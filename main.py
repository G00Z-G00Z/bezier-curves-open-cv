import cv2
import numpy as np
from bezier_lib.bezier_calc import (
    BezierPoints_T,
    Point_T,
    calculate_bezier_points,
    calculate_bezier_points_and_angles,
)

points: list[Point_T] = []  # List to store points
ctrl_points: list[Point_T] = []
curves: list[BezierPoints_T] = []

image_path = "./images/3.jpeg"
IMAGE_TITLE = "Paths"


def draw_bezier_curve(img, points):
    if len(points) < 3:
        # Refresh the image
        cv2.imshow(IMAGE_TITLE, img)
        return img

    # Clear the image and redraw everything
    img = original_img.copy()

    # Draw all points as circles
    for point in points:
        cv2.circle(img, point, 3, (0, 255, 0), -1)

    # Draw the initial bezier curve with the first three points
    p0, p1, p2 = points[0], points[1], points[2]
    bezier_curve_points, angles = calculate_bezier_points_and_angles(p0, p1, p2)
    print(angles)

    # Draw the bezier curve
    for j in range(1, len(bezier_curve_points)):
        cv2.line(
            img, bezier_curve_points[j - 1], bezier_curve_points[j], (255, 0, 0), 2
        )

    # Draw the rest of the bezier curves
    for i in range(3, len(points), 2):
        p0 = points[i - 1]  # Last point of the previous curve
        p1 = points[i]  # Control point
        if i + 1 < len(points):
            p2 = points[i + 1]  # End point of the current curve
            bezier_curve_points, angles = calculate_bezier_points_and_angles(p0, p1, p2)
            print(angles)

            # Draw the bezier curve
            for j in range(1, len(bezier_curve_points)):
                cv2.line(
                    img,
                    bezier_curve_points[j - 1],
                    bezier_curve_points[j],
                    (255, 0, 0),
                    2,
                )

    # Refresh the image
    cv2.imshow(IMAGE_TITLE, img)
    return img


# Inside your mouse callback
def draw_circle(event, x, y, flags, param):
    global points, img
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

        # Update the image with the new point and possibly a new bezier curve
        img = draw_bezier_curve(img, points)


# Load an image
original_img = cv2.imread(image_path)
if original_img is None:
    print("Error: could not load image")
    exit()

# Make a copy of the original image to draw on
img = original_img.copy()


cv2.namedWindow(IMAGE_TITLE)
cv2.setMouseCallback(IMAGE_TITLE, draw_circle)

# Display the image and wait for a key press
cv2.imshow(IMAGE_TITLE, img)
cv2.waitKey(0)

# Save the image with lines and sampled points
cv2.imwrite("./exports/image_with_lines_and_samples.jpg", img)

cv2.destroyAllWindows()
