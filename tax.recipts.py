import os
import csv
import shutil
from datetime import datetime
from PIL import Image
import pytesseract

# 设置路径和配置
input_folder = "input_receipts"  # 原始收据文件夹路径
output_folder = "sorted_receipts"  # 分类后收据的存储路径
csv_file = "receipts_summary.csv"  # 输出的CSV文件

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

def extract_info_from_receipt(image_path):
    """
    从收据图片中提取日期和内容。
    """
    try:
        # 使用OCR读取图片文字
        text = pytesseract.image_to_string(Image.open(image_path))

        print(f"{image_path}: {text}")
        
        # 假设日期格式为 YYYY-MM-DD 或 DD/MM/YYYY，提取日期
        date_formats = ["%Y-%m-%d", "%d/%m/%Y"]
        date = None
        for word in text.split():
            for fmt in date_formats:
                try:
                    date = datetime.strptime(word, fmt).date()
                    break
                except ValueError:
                    continue
            if date:
                break
        
        # 简单获取收据的主要内容（假设在前几行）
        lines = text.strip().split("\n")
        main_content = " ".join(lines[:3])  # 提取前3行作为主要内容
        
        return date, main_content
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None, None

def process_receipts():
    """
    分类和处理收据文件。
    """
    records = []

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(input_folder, filename)
            
            print(f"Processing {filepath}...")
            # 提取信息
            date, content = extract_info_from_receipt(filepath)
            
            if date and content:
                # 生成新的文件名
                new_filename = f"{date}_{content[:10].replace(' ', '_')}.jpg"
                new_filepath = os.path.join(output_folder, new_filename)
                
                # 移动并重命名文件
                shutil.move(filepath, new_filepath)
                
                # 记录数据
                records.append([date, content, new_filename])

    # 将记录保存到CSV文件
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Content", "Filename"])
        writer.writerows(records)

    print(f"Processing complete. Summary saved to {csv_file}")

if __name__ == "__main__":
    process_receipts()

