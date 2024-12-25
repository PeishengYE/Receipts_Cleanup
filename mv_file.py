import os

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

# Example usage
# Replace 'your_file_path' and 'your_destination_folder' with actual values
file_path = '/home/yep/Python/yep/tax_receips/logs/input_receipts/2024_1216_swimming.jpg'
destination_folder_name = 'Processed'
move_file_to_folder(file_path, destination_folder_name)
