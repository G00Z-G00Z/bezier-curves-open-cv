import cv2
import numpy as np
from bezier_lib.bezier_calc import calculate_bezier_points

points = []  # List to store points
image_path = "./images/sample-classroom.jpeg"


def sample_points(start, end, interval=10):
    """Sample points at fixed intervals along the line from start to end."""
    sampled_points = []

    # Calculate the distance between the start and end points
    distance = np.linalg.norm(np.array(end) - np.array(start))

    # Calculate the number of intervals to sample
    num_samples = int(distance / interval)

    # Calculate the vector going from start to end
    vector = np.array(end) - np.array(start)

    # Normalize the vector
    unit_vector = vector / distance

    # Sample points at interval distances
    for i in range(1, num_samples):
        point = np.array(start) + unit_vector * i * interval
        sampled_points.append(point.astype(int))

    return sampled_points


def draw_circle(event, x, y, flags, param):
    global points, img
    if event == cv2.EVENT_LBUTTONDOWN:
        # Append the new point
        points.append((x, y))

        # We need at least two points to form a line
        if len(points) > 1:
            # Clear the image and redraw everything
            img = original_img.copy()

            # Draw all the points
            for point in points:
                cv2.circle(img, point, 3, (0, 255, 0), -1)

            # Redraw each bezier curve segment
            for i in range(1, len(points)):
                # To draw a Bezier curve, we need at least 3 points
                if i < 2:
                    # Draw a straight line for the first segment
                    cv2.line(img, points[i - 1], points[i], (255, 0, 0), 2)
                else:
                    # Use the midpoint of the previous segment as the control point
                    control_point = (
                        np.array(points[i - 2]) + np.array(points[i - 1])
                    ) // 2
                    bezier_points = calculate_bezier_points(
                        points[i - 2], control_point, points[i - 1]
                    )
                    for j in range(1, len(bezier_points)):
                        cv2.line(
                            img,
                            tuple(bezier_points[j - 1]),
                            tuple(bezier_points[j]),
                            (255, 0, 0),
                            2,
                        )

        # Refresh the image
        cv2.imshow("image", img)


# Load an image
original_img = cv2.imread(image_path)
if original_img is None:
    print("Error: could not load image")
    exit()

# Make a copy of the original image to draw on
img = original_img.copy()


cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_circle)

# Display the image and wait for a key press
cv2.imshow("image", img)
cv2.waitKey(0)

# Save the image with lines and sampled points
cv2.imwrite("./exports/image_with_lines_and_samples.jpg", img)

cv2.destroyAllWindows()

# If you want to print out the sampled points for each line
for i in range(1, len(points)):
    sampled_points = sample_points(points[i - 1], points[i])
    print(f"Sampled points between {points[i-1]} and {points[i]}: {sampled_points}")
