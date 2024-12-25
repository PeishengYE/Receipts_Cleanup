import os
import re
import csv
import easyocr
import cv2
import numpy as np
import shutil

# Define the input folder containing scanned receipts and the output CSV file
input_folder = "/mnt/largeDisk1/myOwnCompany/20240801_receipts/"  # Replace with your folder path
#input_folder = "/home/yep/Python/yep/tax_receips/logs/input_receipts/"  # Replace with your folder path
#output_csv = "receipts_content.csv"  # Output CSV file name
tmp_path = "/home/yep/Python/yep/tax_receips/logs/tmp.jpg"
failure_folder = "Swimming_failure"

def get_incremented_file_path(file_path):
    """
    Check the input file path and return an incremented file path if the file already exists.

    :param file_path: Original file path to check.
    :return: A new file path with an incremented number if the file exists.
    """
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)

    # Regex to find an existing number at the end of the filename
    pattern = r"^(.*?)(_\d{2})?$"
    match = re.match(pattern, name)

    if match:
        base_name = match.group(1)  # The main part of the filename
        number = match.group(2)    # The existing number (if any)

        # Start incrementing from 1 if no number exists
        if number is None:
            increment = 1
        else:
            increment = int(number[1:]) + 1

        # Generate a new filename with the incremented number
        while True:
            new_name = f"{base_name}_{increment:02}{ext}"
            new_file_path = os.path.join(directory, new_name)
            if not os.path.exists(new_file_path):
                return new_file_path
            increment += 1

    # If no match, return the original file path
    return file_path


def move_deskew_file_to_folder(file_path, destination_folder_name):
    """
    Moves a file to a destination folder, creating the folder if it doesn't exist.

    :param file_path: Path to the input file.
    :param destination_folder_name: Name of the folder to move the file into.
    """
    # Extract the directory of the input file
    base_dir = os.path.dirname(file_path)

    # Create the full path for the destination folder
    destination_folder_path = os.path.join(base_dir, destination_folder_name)

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)

    name, ext = os.path.splitext(file_path)

    new_filename = f"{name}_deskew{ext}"
    new_file_path = os.path.join(destination_folder_path, new_filename)

    # Move the file to the destination folder
    #os.rename(tmp_path, new_file_path)
    shutil.move(tmp_path, new_file_path)

    print(f"Moved deskewed file to {new_file_path}")





def move_file_to_folder(file_path, destination_folder_name):
    """
    Moves a file to a destination folder, creating the folder if it doesn't exist.

    :param file_path: Path to the input file.
    :param destination_folder_name: Name of the folder to move the file into.
    """
    # Extract the directory of the input file
    base_dir = os.path.dirname(file_path)

    # Create the full path for the destination folder
    destination_folder_path = os.path.join(base_dir, destination_folder_name)

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)

    # Move the file to the destination folder
    destination_file_path = os.path.join(destination_folder_path, os.path.basename(file_path))
    os.rename(file_path, destination_file_path)

    print(f"Moved file to {destination_file_path}")




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


def check_file_pattern(file_path):
    """
    Check if the filename in a given file path matches the pattern `YYYYMMDDHHMM_number.ext`.

    :param file_path: The file path to check.
    :return: True if the filename matches the pattern, False otherwise.
    """
    # Extract the filename from the path
    file_name = file_path.split('/')[-1]  # Handles Unix-style paths
    
    # Regex for the pattern `YYYYMMDDHHMM_number.ext`
#    pattern = r"^\d{12}_\d{1,2}\.[a-zA-Z]{3,4}$"
    pattern = r"^\d{12}_\d{1,2}_swimming_swimming\.[a-zA-Z]{3,4}$"

    # Match the pattern
    return bool(re.match(pattern, file_name))

def convert_date_to_numeric(date_str):
    """
    Replace month abbreviations with numeric equivalents in a string,
    leaving all other content unchanged.
    """
    # Mapping of month abbreviations to numeric equivalents
    month_map = {
        "JAN": "01", "FEB": "02", "MAR": "03", "APR": "04",
        "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
        "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"
    }
    # Replace month abbreviations with their numeric equivalents
    return re.sub(r"\b(\w{3}) (\d{1,2})\b", 
                  lambda m: f"{month_map.get(m.group(1).upper(), m.group(1))}{m.group(2)}", 
                  date_str)

def process_file(file_path):

    reader = easyocr.Reader(['en', 'fr'])

    # Keywords to look for
    keywords_required = ["Purchase", "BEACONSFIELD"]
    keywords_optional = ["4,50", "4.50"]

    # Date pattern to search for
    date_pattern = r"\b(\w{3} \d{1,2},\d{4})\b"

    try:
            #result = reader.readtext(tmp_path)
            result = reader.readtext(file_path)
            # Combine detected text into a single string
            content = "\n".join([text for (_, text, _) in result])

            print(f"{file_path}: ")
            print(f"=====================")
            print(f"{content}")
            print(f"=====================")

            filename = file_path.split('/')[-1]  # Handles Unix-style paths
            # Check for required and optional keywords in the extracted content
            if all(keyword in content for keyword in keywords_required) and any(keyword in content for keyword in keywords_optional):

                
                    # Find the date in the content
                    date_match = re.search(date_pattern, content)
                    if date_match:
                        date_str = date_match.group(1)
                        print(f"date_str: {date_str}")
                        new_date_str = convert_date_to_numeric(date_str)
                        # Convert date to desired format (YYYY_MMDD)
                        formatted_date = re.sub(r"(\d{4}),(\d{4})", lambda m: f"{m.group(2)}_{m.group(1)}", new_date_str)
                        name, ext = os.path.splitext(filename)
                        new_name = f"{formatted_date}_swimming{ext}"
                        new_path = os.path.join(input_folder, new_name)
                        os.rename(file_path, new_path)
                        print(f"File renamed to {new_name}")
                    else : 
                        deskew_image(file_path, tmp_path)

                        result = reader.readtext(file_path)
                        content = "\n".join([text for (_, text, _) in result])

                        print(f"After adjust image:  ")
                        print(f"{file_path}: ")
                        print(f"=====================")
                        print(f"{content}")
                        print(f"=====================")

                        date_match = re.search(date_pattern, content)
                        if date_match:

                            date_str = date_match.group(1)
                            print(f"date_str: {date_str}")
                            new_date_str = convert_date_to_numeric(date_str)
                            # Convert date to desired format (YYYY_MMDD)
                            formatted_date = re.sub(r"(\d{4}),(\d{4})", lambda m: f"{m.group(2)}_{m.group(1)}", new_date_str)
                            name, ext = os.path.splitext(filename)
                            new_name = f"{formatted_date}_swimming{ext}"
                            new_path = os.path.join(input_folder, new_name)

                            # increase the version number if a file exist already
                            filename_with_version = get_incremented_file_path(new_path):

                            os.rename(file_path, filename_with_version)
                            print(f"File renamed to {new_name}")

                        else:
                            # Rename the file by appending '_swimming' before the file extension
                            print(f"Failed! No action on {filename}")
                            move_file_to_folder(file_path, failure_folder)
                            move_deskew_file_to_folder(file_path, failure_folder)


    except Exception as e:
       print(f"Error processing {file_path}: {e}")




def process_receipts(input_folder):
    """
    Process all receipt images in the folder, extract text using EasyOCR,
    and rename files if specific criteria are met.
    """
        # Iterate through all files in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Supported image formats
            file_path = os.path.join(input_folder, filename)

            if  check_file_pattern(file_path):
                print(f"Processing {file_path}...")
                process_file(file_path)

process_receipts(input_folder)


