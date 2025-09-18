<p align="center">
  <img src="assets/logo.png" alt="EasyWeather" width="150"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.13-blue" alt="Python">
  <img src="https://img.shields.io/badge/Framework-Streamlit-orange" alt="Streamlit">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

<p align="center">
  <a href="https://ady201m-group3.streamlit.app/">
    <img src="https://img.shields.io/badge/Open%20App-EasyWeather-brightgreen?style=for-the-badge&logo=streamlit" 
         alt="Open App"
         style="transform: scale(1.5); margin-top: 15px;">
  </a>
</p>

<p align="center">
  <a href="#introduction">Introduction</a> •
  <a href="#feature">Features</a> •
  <a href="#how-to-run">How&nbsp;to&nbsp;Run</a> •
  <a href="#-project-structure">Project&nbsp;Structure</a> •
  <a href="#demo">Demo</a> •
  <a href="#techstack">Tech&nbsp;Stack</a> •
  <a href="#flow-app">Flow&nbsp;App</a> •
  <a href="#limitations">Limitations</a> •
  <a href="#authors">Authors</a>
</p>

EW: EasyWeather là một web app dự báo thời tiết 7 ngày sử dụng Open-Meteo API, thực hiện bởi nhóm 3 môn ADY201m do thầy Hùng-BK phụ trách.

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

 ## Project structure 
 ``` 
├── README.md # mô tả dự án 
├── app.py # entry point chính 
├── requirements.txt # dependencies 
└── assets/ # ảnh demo 
```

## Demo
[Truy cập app online](https://ady201m-group3.streamlit.app/) để xem live demo app.
Biểu đồ dự báo của Hà Nội 7 ngày tới:
<p align="center">
  <img src="assets/chart.png" alt="Weather Chart Demo" width="750"/>
</p>

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

## Limitations
- Do giới hạn thời gian, ứng dụng mới chỉ có thể sử dụng vị trí thành phố mặc định, chưa hỗ trợ tra cứu thông tin trong quá khứ và so sánh giữa các địa điểm.

## Authors:
- Lê Quang Hưng: MSSV: HE201273
- Đinh Quang Minh: MSSV: HE201506
- Đỗ Mạnh Chung: MSSV: HE201350
