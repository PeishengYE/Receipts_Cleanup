import os
import csv
import easyocr

# Define the input folder containing scanned receipts and the output CSV file
input_folder = "/mnt/largeDisk1/myOwnCompany/20240801_receipts/"  # Replace with your folder path
output_csv = "receipts_content.csv"  # Output CSV file name

def process_receipts():
    """
    Process all receipt images in the folder, extract text using EasyOCR,
    and save the results into a CSV file.
    """
    # Initialize EasyOCR reader with GPU support (set gpu=False if no GPU is available)
    reader = easyocr.Reader(['en', 'fr'])

    # Prepare a list to store the results
    records = []

    # Iterate through all files in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Supported image formats
            file_path = os.path.join(input_folder, filename)
            print(f"Processing {file_path}...")

            # Use EasyOCR to extract text
            try:
                result = reader.readtext(file_path)
                # Combine detected text into a single string
                content = "\n".join([text for (_, text, _) in result])
                
                # Append the filename and content to records
                records.append([filename, content])
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                records.append([filename, "Error: Unable to process file"])

    # Write the records to a CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Filename", "Content"])  # Header row
        writer.writerows(records)

    print(f"Processing complete. Results saved to {output_csv}")

if __name__ == "__main__":
    process_receipts()

