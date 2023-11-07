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


def draw_bezier_curve(img, points):
    # We need at least three points to draw a bezier curve
    if len(points) >= 3:
        # Clear the image and redraw everything
        img = original_img.copy()

        # Draw all the points
        for point in points:
            cv2.circle(img, point, 3, (0, 255, 0), -1)

        # Now draw the bezier curves
        for i in range(2, len(points), 3):
            # p0, p1, p2 are the start, control, and end points of the bezier curve, respectively
            p0, p1, p2 = points[i - 2], points[i - 1], points[i]
            bezier_curve_points = calculate_bezier_points(p0, p1, p2, num_points=100)

            # Draw the Bezier curve by connecting each pair of consecutive points
            for j in range(1, len(bezier_curve_points)):
                cv2.line(
                    img,
                    bezier_curve_points[j - 1],
                    bezier_curve_points[j],
                    (255, 0, 0),
                    2,
                )

            # Optionally, save the Bezier curve points if needed
            # bezier_points.extend(bezier_curve_points) # Uncomment if you want to save bezier curve points

    # Refresh the image
    cv2.imshow("image", img)
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
