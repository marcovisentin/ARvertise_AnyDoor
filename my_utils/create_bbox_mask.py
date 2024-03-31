import cv2
import numpy as np
import sys

sys.path.append('../')

# Global variables
image_path = "my_assets/test_image.png"
mask_file = "my_assets/binary_mask.png"  # Path to save the binary mask
drawing = False  # True if mouse is pressed
ix, iy = -1, -1  # Starting coordinates of the rectangle
coordinates = []  # List to store bounding box coordinates

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, coordinates

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_temp = img.copy()
            cv2.rectangle(img_temp, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow('image', img_temp)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        coordinates.append((min(ix, x), min(iy, y), abs(ix - x), abs(iy - y)))

# Load the image
img_name = image_path.split("/")[-1]
img = cv2.imread(image_path)
clone = img.copy()

# Create a window and bind the function to window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_rectangle)

while True:
    cv2.imshow('image', img)
    key = cv2.waitKey(1) & 0xFF

    # Press 'r' to reset the image
    if key == ord('r'):
        img = clone.copy()
        coordinates = []

    # Press 's' to save the coordinates to a text file and create a binary mask
    elif key == ord('s'):        
        # Create and save binary mask
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        for (x, y, w, h) in coordinates:
            mask[y:y+h, x:x+w] = 255
        cv2.imwrite(mask_file, mask)
        
        print("Bounding box coordinates and binary mask saved.")
        break

    # Press 'q' to quit
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
