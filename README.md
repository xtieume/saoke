# Hướng Dẫn Sử Dụng Extract Table Tool

## Giới thiệu
Project này chứa hai file Python `extract_table_with_image.py` và `extract_table.py` được sử dụng để trích xuất dữ liệu từ các tệp PDF có cấu trúc bảng. Kết quả trích xuất sẽ được lưu trữ dưới dạng file CSV, đồng thời có thể xuất các hình ảnh chứa bảng dữ liệu với các đường biên được vẽ.

## Yêu cầu
- Python 3.x
- Các thư viện cần thiết:
  - `pdfplumber`
  - `PIL` (Python Imaging Library hoặc thư viện `Pillow`)
  - `csv`

## Cấu trúc project
- **extract_table_with_image.py**: Tập lệnh này không chỉ trích xuất dữ liệu bảng mà còn vẽ các đường biên lên hình ảnh của bảng trong PDF và lưu các hình ảnh này ra file.
- **extract_table.py**: Tập lệnh này chỉ trích xuất dữ liệu bảng từ file PDF và xuất ra file CSV mà không xuất hình ảnh.
- **vcb.pdf** và **vcb_p1.pdf**: Các file PDF chứa dữ liệu bảng cần trích xuất.
- **extracted_table_with_image.csv**: File CSV kết quả chứa dữ liệu được trích xuất từ file PDF.

## Hướng dẫn sử dụng

### 1. Cài đặt môi trường
Trước khi chạy các tập lệnh, bạn cần cài đặt các thư viện cần thiết:

```bash
pip install pdfplumber pillow
```

### 2. Cách sử dụng các tập lệnh

#### a. Chạy tập lệnh trích xuất bảng và xuất hình ảnh:
Sử dụng `extract_table_with_image.py` để trích xuất bảng từ file PDF, lưu trữ kết quả vào file CSV và xuất ra hình ảnh có chứa bảng.

```bash
python extract_table_with_image.py
```

Kết quả:
- File CSV sẽ được lưu với tên `extracted_table_with_image.csv`.
- Các hình ảnh của từng trang PDF chứa bảng dữ liệu sẽ được lưu với tên như `page_1_with_combined_bbox.png`, `page_2_with_combined_bbox.png`,...

#### b. Chạy tập lệnh chỉ trích xuất bảng:
Nếu bạn chỉ muốn trích xuất bảng và không cần lưu hình ảnh, hãy sử dụng tập lệnh `extract_table.py`:

```bash
python extract_table.py
```

Kết quả:
- File CSV chứa dữ liệu bảng sẽ được lưu tương tự như trên.

## Chú ý
- Tập lệnh `extract_table_with_image.py` xuất cả hình ảnh và dữ liệu bảng, do đó bạn cần chắc chắn thư mục làm việc có đủ không gian lưu trữ hình ảnh và file CSV.
- Đảm bảo rằng file PDF đầu vào có định dạng bảng rõ ràng để tập lệnh có thể nhận diện và trích xuất dữ liệu chính xác.