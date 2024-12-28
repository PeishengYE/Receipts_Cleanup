import os
import time
from receipt_data_class import (
    Receipt, add_receipt, load_receipts_from_csv, start_receipt_monitor_thread, get_receipt_by_file_md5
)

if __name__ == "__main__":
    # Define the CSV file name
    csv_filename = "receipts.csv"

    # Initialize the receipt list
    if os.path.exists(csv_filename):
        print(f"Found existing CSV file: {csv_filename}. Loading receipts...")
        receipt_list = load_receipts_from_csv(csv_filename)
        print(f"Loaded {len(receipt_list)} receipts from the file.")
    else:
        print("No existing CSV file found. Starting with an empty receipt list.")
        receipt_list = []

    # Start monitoring the list and saving to CSV
    start_receipt_monitor_thread(receipts=receipt_list, filename=csv_filename, interval=5)

    # Add a new receipt to the list
    add_receipt(
        receipt_list,
        date=20241228,
        description="Laptop purchase",
        amount_after_tax=1500.00,
        gst=75.00,
        qst=120.00,
        paid_from_business=True,
        category="Electronics",
        file_md5="abc12345def67890",
        filename="receipt_laptop.pdf"
    )
    print("Added first receipt.")

    # Wait and simulate adding another receipt
    time.sleep(10)
    add_receipt(
        receipt_list,
        date=20241229,
        description="Office supplies",
        amount_after_tax=200.00,
        gst=10.00,
        qst=15.00,
        paid_from_business=False,
        category="Stationery",
        file_md5="xyz98765uvw43210",
        filename="receipt_supplies.pdf"
    )
    print("Added second receipt.")

    # Test retrieving a receipt by file MD5
    test_file = "receipt_laptop.pdf"  # Ensure this file exists with the matching MD5
    receipt = get_receipt_by_file_md5(receipt_list, test_file)
    if receipt:
        print(f"Receipt found for file {test_file}: {receipt}")
    else:
        print(f"No receipt found for file {test_file}")

    # Let the monitoring thread save the updates
    time.sleep(10)
    print("Exiting test.")

