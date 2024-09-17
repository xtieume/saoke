import pdfplumber
import csv
import os
import re

# Danh sách các tệp PDF cần xử lý
pdf_paths = [
    'mttq_agribank_caobang.1009.1309.pdf',
    'mttq_agribank_hanoi.0909.1209.pdf',
]

def format_currency(value):
    """Định dạng số tiền thành định dạng x.xxx"""
    # Loại bỏ tất cả các ký tự không phải số hoặc dấu phẩy
    value = re.sub(r'[^\d,]', '', value)
    
    # Kiểm tra nếu chuỗi có khoảng trống thì lấy từ cuối cùng
    if ' ' in value:
        value = value.split()[-1]

    # Thay thế dấu phẩy thành dấu chấm để làm chuẩn cho định dạng số
    parts = value.split(',')
    formatted_value = parts[0]
    
    # Định dạng thành tiền tệ
    if len(parts) > 1:
        for part in parts[1:]:
            formatted_value += f'.{part}'
    
    return formatted_value

def process_column_five(value):
    """Thay thế dấu phẩy thành dấu chấm cho cột số 5"""
    return value.replace(',', '.')

def extract_table_from_pdf(pdf_path):
    # Tạo tên file CSV từ tên file PDF
    csv_output_path = os.path.splitext(pdf_path)[0] + '.csv'

    with pdfplumber.open(pdf_path) as pdf, open(csv_output_path, 'w', newline='', encoding='utf-8') as csvfile:
        total_pages = len(pdf.pages)
        csv_writer = csv.writer(csvfile)
        print(f"Bắt đầu xử lý tệp {pdf_path}, Tổng số trang: {total_pages}")
        
        for page_number, page in enumerate(pdf.pages):
            print(f"Đang xử lý trang {page_number + 1}/{total_pages} của tệp {pdf_path}")

            # Trích xuất bảng từ trang hiện tại
            table = page.extract_table()

            if table:
                for row in table[1:]:
                    # Cột 3 và 4: Định dạng lại số tiền
                    row[2] = format_currency(row[2])  # Cột 3 (số tiền ghi có)
                    row[3] = format_currency(row[3])  # Cột 4 (số dư)

                    # Cột 5: Thay thế dấu phẩy thành dấu chấm
                    row[4] = process_column_five(row[4])

                    # Thêm cột cố định thứ 7 và 8
                    row.append('AGRIBANK')  # Cột cố định thứ 7
                    row.append('MTTQ')  # Cột cố định thứ 8

                    # Ghi hàng vào CSV
                    csv_writer.writerow(row)
            else:
                print(f"Không tìm thấy bảng trên trang {page_number + 1}/{total_pages}")

    print(f"Dữ liệu đã được xuất ra {csv_output_path}")

# Gọi hàm cho mỗi tệp PDF trong danh sách
for pdf_path in pdf_paths:
    extract_table_from_pdf(pdf_path)
