import cv2
import numpy as np

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
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        # Draw a circle at the clicked point
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)

        # Append the new point
        points.append((x, y))

        # If we have at least two points, draw the connecting line
        if len(points) >= 2:
            cv2.line(img, points[-2], points[-1], (255, 0, 0), 2)

            # Get the sampled points and draw them
            sampled_points = sample_points(points[-2], points[-1])
            for sp in sampled_points:
                cv2.circle(img, tuple(sp), 2, (0, 0, 255), -1)

        # Refresh the image
        cv2.imshow("image", img)


# Load an image
img = cv2.imread(image_path)
if img is None:
    print("Error: could not load image")
    exit()

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
