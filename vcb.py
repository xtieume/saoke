import pdfplumber
import csv
import os

# Danh sách các tệp PDF cần xử lý
pdf_paths = [
    'mttq_vcb.0109.1009.pdf',
]

# Xác định các cột trong bảng bằng các biên (x1, x2)
column_boundaries = [
    20, 100, 190, 286, 386, 575
]

def find_column(x0, column_boundaries):
    for i in range(len(column_boundaries) - 1):
        if column_boundaries[i] <= x0 <= column_boundaries[i + 1]:
            return i
    return -1

def is_close_y(a, b, tolerance=5):
    return abs(a - b) <= tolerance

def are_words_in_same_line(word1, word2, x_tolerance=10):
    return word2['x0'] - word1['x1'] <= x_tolerance

def are_lines_in_same_cell(line1, line2, y_tolerance=10):
    return abs(line2[0]['top'] - line1[0]['bottom']) <= y_tolerance

def extract_table_and_merge_words(pdf_path, column_boundaries, y_tolerance=5, x_tolerance=10, line_y_tolerance=10):
    # Tạo tên file CSV từ tên file PDF
    csv_output_path = os.path.splitext(pdf_path)[0] + '.csv'

    with pdfplumber.open(pdf_path) as pdf, open(csv_output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for page_number, page in enumerate(pdf.pages):
            # Log để biết đang xử lý đến trang nào
            print(f"Đang xử lý trang {page_number + 1} của tệp {pdf_path}")

            tables = page.find_tables()
            if not tables:
                print(f"Không tìm thấy bảng trên trang {page_number+1}")
                continue

            table_bbox = tables[0].bbox
            x0, top, x1, bottom = table_bbox

            words = page.extract_words()
            filtered_words = [word for word in words if x0 <= word['x0'] <= x1 and top <= word['top'] <= bottom]

            columns = {i: [] for i in range(len(column_boundaries) - 1)}
            for word in filtered_words:
                col_idx = find_column(word['x0'], column_boundaries)
                if col_idx != -1:
                    columns[col_idx].append(word)

            page_data = [[] for _ in range(5)]  # List of 5 columns to store data from current page
            for col_idx, col_words in columns.items():
                col_words = sorted(col_words, key=lambda w: w['top'])

                current_line = []
                all_lines = []
                for word in col_words:
                    if not current_line:
                        current_line.append(word)
                    else:
                        if is_close_y(current_line[-1]['top'], word['top'], y_tolerance) and are_words_in_same_line(current_line[-1], word, x_tolerance):
                            current_line.append(word)
                        else:
                            if current_line:
                                current_line.sort(key=lambda w: w['x0'])
                                all_lines.append(current_line)
                            current_line = [word]
                
                if current_line:
                    current_line.sort(key=lambda w: w['x0'])
                    all_lines.append(current_line)

                current_cell = []
                for line in all_lines:
                    if not current_cell:
                        current_cell.append(line)
                    else:
                        if are_lines_in_same_cell(current_cell[-1], line, line_y_tolerance):
                            current_cell.append(line)
                        else:
                            if current_cell:
                                cell_text = ' '.join(' '.join(word['text'] for word in sorted(l, key=lambda w: w['x0'])) for l in current_cell)
                                page_data[col_idx].append(cell_text)
                            current_cell = [line]

                if current_cell:
                    cell_text = ' '.join(' '.join(word['text'] for word in sorted(l, key=lambda w: w['x0'])) for l in current_cell)
                    page_data[col_idx].append(cell_text)

            max_rows = max(len(column) for column in page_data)
            for row in range(max_rows):
                csv_row = []
                for col_idx, column in enumerate(page_data):
                    if col_idx == 0 and row < len(column):
                        first_col_split = column[row].split()
                        csv_row.append(first_col_split[0])  # Ngày tháng
                        csv_row.append(' '.join(first_col_split[1:]))  # Số CT
                    elif row < len(column):
                        csv_row.append(column[row])
                    else:
                        csv_row.append('')
                # Thêm cột số 7 với giá trị "VCB"
                csv_row.append('VCB')
                # Nguồn dữ liệu
                csv_row.append("MTTQ")
                # Lưu trực tiếp row vào file CSV
                if page_number == 0 or row > 0:
                    csv_writer.writerow(csv_row)

        print(f"Dữ liệu đã được xuất ra {csv_output_path}")

# Gọi hàm cho mỗi tệp PDF trong danh sách
x_tolerance = 200
y_tolerance = 5
line_y_tolerance = 5

for pdf_path in pdf_paths:
    extract_table_and_merge_words(pdf_path, column_boundaries, y_tolerance, x_tolerance, line_y_tolerance)
