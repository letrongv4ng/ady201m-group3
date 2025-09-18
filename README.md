## Feature
- Tra cứu thời tiết sử dụng API thực của "Open-Meteo".
- Dự báo theo biểu đồ 7 ngày tới.
## How to run
1. Clone repository:
- Run this code in your terminal: 
``` bash 
git clone https://github.com/letrongv4ng/ady201m-group3
```
- Install dependencies:
``` bash
pip install -r requirements.txt
```
- Run app:
``` python
streamlit run app.py
```
2. Quick access:
https://ady201m-group3.streamlit.app/

## Project structure:
.
├── README.md   # mô tả dự án
├── app.py  # entry point chính
├── requirements.txt    # dependencies

## Techstack:
- Python version: 3.13
- Framework: streamlit
- Lib chính: requests, pandas, matplotlib.

## Flow app:

1. Người dùng nhập vào tên thành phố muốn tra cứu:
- Tự động regex theo tên thành phố chuẩn.
- Ghép tên thành phố vào "city-name" trong đường link dẫn đến API.
2. Dẫn API -> json raw
- Trích xuất dữ liệu từ json raw.
- Sử dụng matplotlib để tạo biểu đồ.
3. Kết quả:
- Ứng dụng hiển thị biểu đồ đường (line chart) thể hiện:
    - Nhiệt độ cao nhất
    - Nhiệt độ thấp nhất
    - Độ ẩm
    - Tốc độ gió

## Limitation

# Do giới hạn thời gian, ứng dụng mới chỉ có thể sử dụng vị trí thành phố mặc định, chưa hỗ trợ tra cứu thông tin trong quá khứ và so sánh giữa các địa điểm.

## Authors:

# LAB 02 - ADY201m
- Lê Quang Hưng: MSSV: HE201273
- Đinh Quang Minh: MSSV: HE201506
- Đỗ Mạnh Chung: MSSV: HE201350
