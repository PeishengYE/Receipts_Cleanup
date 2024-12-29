import csv
import hashlib
import threading
import time
from typing import List
from dataclasses import dataclass

@dataclass
class Receipt:
    file_md5: str
    date: int
    amount_after_tax: float
    gst: float
    qst: float
    payment_method: str
    category: str
    filename: str
    notice: str

def add_receipt(receipts: List[Receipt], **kwargs) -> None:
    new_receipt = Receipt(**kwargs)
    receipts.append(new_receipt)

def save_receipts_to_csv(receipts: List[Receipt], filename: str) -> None:
    headers = [
        "file_md5", "date",  "amount_after_tax", "gst", "qst",
        "payment_method", "category", "filename", "notice"
    ]
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for receipt in receipts:
            writer.writerow([
                receipt.file_md5, receipt.date, receipt.amount_after_tax,
                receipt.gst, receipt.qst, receipt.payment_method,
                receipt.category,  receipt.filename, receipt.notice
            ])

def load_receipts_from_csv(filename: str) -> List[Receipt]:
    receipts = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            receipt = Receipt(
                file_md5=row['file_md5'],
                date=int(row['date']),
                amount_after_tax=float(row['amount_after_tax']),
                gst=float(row['gst']),
                qst=float(row['qst']),
                payment_method=row['payment_method'],
                category=row['category'],
                filename=row['filename'], 
                notice=row['notice'], 
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

def get_md5sum(file_path: str) -> str:
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error: {e}"

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

def get_receipt_by_file_md5(receipts: List[Receipt], file_path: str) -> Receipt:
    file_md5 = get_md5sum(file_path)
    if file_md5 == "File not found" or "Error" in file_md5:
        print(file_md5)
        return None
    for receipt in receipts:
        if receipt.file_md5 == file_md5:
            return receipt
    return None

