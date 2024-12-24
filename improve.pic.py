from PIL import Image, ImageFilter, ImageOps

# Load the image
#image_path = "input_receipts/202412171114_5.jpg"
image_path = "input_receipts/2024_0801_swimming.4.5.jpg"
img = Image.open(image_path)

# Convert to grayscale
img = img.convert("L")

# Enhance contrast
img = ImageOps.autocontrast(img)

# Apply slight blur to reduce noise
img = img.filter(ImageFilter.MedianFilter(size=3))

# Save or process the image further
processed_image_path = "input_receipts/processed_receipt.2.jpg"
img.save(processed_image_path)

