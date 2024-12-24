import easyocr

reader = easyocr.Reader(['en', 'fr'])
#results = reader.readtext("input_receipts/processed_receipt.jpg")
#results = reader.readtext("input_receipts/processed_receipt.2.jpg")
#results = reader.readtext("/mnt/largeDisk1/myOwnCompany/20240801_receipts/202412171114_1.jpg")
results = reader.readtext("/mnt/largeDisk1/myOwnCompany/20240801_receipts/202411291740_2.jpg")
#results = reader.readtext("/mnt/largeDisk1/myOwnCompany/20240801_receipts/2024_0801_swimming.4.5.jpg")

for (bbox, text, prob) in results:
    print(f"Text: {text}, Probability: {prob}")

