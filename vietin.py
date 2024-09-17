import pdfplumber
import csv
import os

# Danh sách các tệp PDF cần xử lý
pdf_paths = [
    'bvdcttu_vietin.1009.1209.pdf',
]

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
                # Thêm hai cột cố định vào mỗi dòng và ghi ra file CSV
                for row in table:
                    row.append('VIETIN')  # Cột cố định thứ 7
                    row.append('BVDCTTU')  # Cột cố định thứ 8
                    csv_writer.writerow(row)
            else:
                print(f"Không tìm thấy bảng trên trang {page_number + 1}/{total_pages}")

    print(f"Dữ liệu đã được xuất ra {csv_output_path}")

# Gọi hàm cho mỗi tệp PDF trong danh sách
for pdf_path in pdf_paths:
    extract_table_from_pdf(pdf_path)
