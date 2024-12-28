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

def update_receipt_by_file_md5(receipts: List[Receipt], updated_receipt: Receipt) -> bool:
    for index, receipt in enumerate(receipts):
        if receipt.file_md5 == updated_receipt.file_md5:
            receipts[index] = updated_receipt
            return True
    return False

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

def get_receipt_by_file_md5(receipts: List[Receipt], file_path: str) -> Receipt:
    file_md5 = get_md5sum(file_path)
    if file_md5 == "File not found" or "Error" in file_md5:
        print(file_md5)
        return None
    for receipt in receipts:
        if receipt.file_md5 == file_md5:
            return receipt
    return None

