import csv
import hashlib
import threading
import time
from typing import List
from dataclasses import dataclass

@dataclass
class Receipt:
    date: int
    description: str
    amount_after_tax: float
    gst: float
    qst: float
    paid_from_business: bool
    category: str
    file_md5: str
    filename: str

def add_receipt(receipts: List[Receipt], **kwargs) -> None:
    new_receipt = Receipt(**kwargs)
    receipts.append(new_receipt)

def save_receipts_to_csv(receipts: List[Receipt], filename: str) -> None:
    headers = [
        "date", "description", "amount_after_tax", "gst", "qst",
        "paid_from_business", "category", "file_md5", "filename"
    ]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for receipt in receipts:
            writer.writerow([
                receipt.date, receipt.description, receipt.amount_after_tax,
                receipt.gst, receipt.qst, receipt.paid_from_business,
                receipt.category, receipt.file_md5, receipt.filename
            ])

def load_receipts_from_csv(filename: str) -> List[Receipt]:
    receipts = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            receipt = Receipt(
                date=int(row['date']),
                description=row['description'],
                amount_after_tax=float(row['amount_after_tax']),
                gst=float(row['gst']),
                qst=float(row['qst']),
                paid_from_business=row['paid_from_business'].lower() == 'true',
                category=row['category'],
                file_md5=row['file_md5'],
                filename=row['filename']
            )
            receipts.append(receipt)
    return receipts

def update_receipt(receipts: List[Receipt], **kwargs ) -> None:
    input_receipt = Receipt(**kwargs)
    found = False
    for index, receipt in enumerate(receipts):
        if receipt.file_md5 == input_receipt.file_md5:
            receipts[index] = input_receipt
            print(f"update_receipt()>> update the current receipt item")
            found = True

    if not found:
        add_receipt(receipts, **kwargs)
        print(f"update_receipt()>> This is a new receipt, added this new receipt item")



def calculate_list_hash(receipts: List[Receipt]) -> str:
    hash_obj = hashlib.sha256()
    for receipt in receipts:
        hash_obj.update(str(receipt).encode('utf-8'))
    return hash_obj.hexdigest()

def monitor_and_save_receipts(receipts: List[Receipt], filename: str, interval: int = 5):
    last_hash = calculate_list_hash(receipts)
    while True:
        time.sleep(interval)
        current_hash = calculate_list_hash(receipts)
        if current_hash != last_hash:
            save_receipts_to_csv(receipts, filename)
            print(f"Receipts updated and saved to {filename}.")
            last_hash = current_hash

def start_receipt_monitor_thread(receipts: List[Receipt], filename: str, interval: int = 5):
    monitor_thread = threading.Thread(
        target=monitor_and_save_receipts, 
        args=(receipts, filename, interval),
        daemon=True
    )
    monitor_thread.start()

