import cv2
import numpy as np

def deskew_image(input_path, output_path):
    """
    Reads a scanned receipt, deskews it to make it horizontal, and saves the corrected image.

    :param input_path: Path to the input image file (scanned receipt).
    :param output_path: Path to save the deskewed image.
    """
    # Read the image
    image = cv2.imread(input_path, cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detection
    edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

    # Find lines in the image using Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    if lines is not None:
        # Calculate the average angle of the detected lines
        angles = []
        for line in lines:
            rho, theta = line[0]
            angles.append(theta)

        # Convert angles to degrees and find the average angle
        angles = [np.rad2deg(theta) for theta in angles]
        median_angle = np.median(angles)

        # Adjust the angle to rotate the image to horizontal
        rotation_angle = median_angle - 90 if median_angle > 45 else median_angle

        # Get the image dimensions
        (h, w) = gray.shape[:2]
        center = (w // 2, h // 2)

        # Calculate the rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)

        # Perform the rotation
        deskewed = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

        # Save the deskewed image
        cv2.imwrite(output_path, deskewed)
        print(f"Deskewed image saved to {output_path}")
    else:
        print("No lines detected; unable to deskew the image.")

# Example usage
input_path = '/home/yep/Python/yep/tax_receips/logs/input_receipts/./2024_1025_swimming_rotated.jpg'  # Replace with the path to your scanned receipt
output_path = '/home/yep/Python/yep/tax_receips/logs/input_receipts/./2024_1025_swimming_new.jpg'  # Replace with the path to your scanned receipt
deskew_image(input_path, output_path)

