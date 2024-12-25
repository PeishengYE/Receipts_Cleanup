import os
import re

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

# Example usage
original_file_path = "/home/yep/Python/yep/tax_receips/logs/input_receipts/2024_1220_swimming.jpg"
new_file_path = get_incremented_file_path(original_file_path)
print(f"New file path: {new_file_path}")

