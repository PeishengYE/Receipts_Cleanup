import pytesseract

# Path to processed image
processed_image_path = "input_receipts/processed_receipt.jpg"

# Configure Tesseract
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz./:'

# Perform OCR
text = pytesseract.image_to_string(processed_image_path, config=custom_config)
print(text)

