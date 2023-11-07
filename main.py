import cv2
import numpy as np

# Initialize a list to store the points
image = "./images/sample-classroom.jpeg"
points = []


# This function will be called whenever a mouse event happens
def draw_circle(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        # Draw a circle where the click happened
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)

        # Append the point
        points.append((x, y))

        # Draw line if there are at least two points
        if len(points) >= 2:
            cv2.line(img, points[-2], points[-1], (255, 0, 0), 2)

        cv2.imshow("image", img)


# Load an image
img = cv2.imread(image)

# Check if the image was loaded correctly
if img is None:
    print("Error: could not load image")
    exit()

# Create a window
cv2.namedWindow("image")

# Set the mouse callback function to `draw_circle`
cv2.setMouseCallback("image", draw_circle)

# Show the image and wait for a key press
cv2.imshow("image", img)
cv2.waitKey(0)

# Save the resulting image
cv2.imwrite("image_with_lines.jpg", img)

# Close all windows
cv2.destroyAllWindows()
