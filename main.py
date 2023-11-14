import cv2
import numpy as np
from bezier_lib.bezier_calc import (
    BezierPoints_T,
    Point_T,
    calculate_ctr_point,
    points_to_bezier,
)

points: list[Point_T] = []  # List to store points
ctrl_points: list[Point_T] = []
curves: list[BezierPoints_T] = []

image_path = "./images/3.jpeg"
IMAGE_TITLE = "Paths"


def draw_bezier_curve(img, points: list[Point_T]):
    # Clear the image and redraw everything
    img = original_img.copy()

    # Draw all points as circles
    for point in points:
        cv2.circle(img, point, 3, (0, 255, 0), -1)

    if len(points) < 2:
        # Refresh the image
        cv2.imshow(IMAGE_TITLE, img)
        return img

    if len(points) == 2:
        first_ctr_point = (np.array(points[1]) + np.array(points[0])) / 2
        ctrl_points.append(first_ctr_point.tolist())

    prev_point = points[-2]
    last_point = points[-1]
    prev_ctr_point = ctrl_points[-1]

    bezier_points: BezierPoints_T = (prev_point, prev_ctr_point, last_point)
    curves.append(bezier_points)

    # Calculate next ctr point
    new_ctr_point = calculate_ctr_point(bezier_points, last_point, scale=0.5)
    ctrl_points.append(new_ctr_point)

    # Draw the beziers curves

    # Plot both curves
    s_vals = np.linspace(0, 1, 100)

    # Plot all the curves
    for bezier_points in curves:
        curve = points_to_bezier(bezier_points)
        coordinates = curve.evaluate_multi(s_vals)
        x = coordinates[0, :]
        y = coordinates[1, :]
        coordinates = np.array([x, y]).T.reshape(-1, 1, 2).astype(np.int32)
        cv2.polylines(img, [coordinates], False, (0, 0, 255), 2)

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
