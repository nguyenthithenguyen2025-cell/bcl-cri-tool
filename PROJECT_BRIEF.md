# PROJECT BRIEF — BCL-CRI Decision Support Tool

**Tên dự án:** CÔNG CỤ HỖ TRỢ QUYẾT ĐỊNH ĐÓNG BÃI CHÔN LẤP CTRSH  
**Phiên bản:** 1.0  
**Ngày khởi tạo:** 2026-06-07  
**Chủ nhiệm:** Trường Đại học Thủy Lợi — Đề tài TNMT.2024.05.05  
**Công nghệ:** Python 3.11+ · Streamlit · Plotly · openpyxl · python-docx  
**Triển khai:** Streamlit Community Cloud (URL công khai, miễn phí)

---

## 1. Mục tiêu

Xây dựng web app chuyên nghiệp hỗ trợ:

1. **Khai báo thông tin** bãi chôn lấp (BCL) không hợp vệ sinh (BCL-KHVS)
2. **Tính toán chỉ số rủi ro CRI** theo 14 thông số (nhóm H, P, R)
3. **Phân loại mức độ rủi ro** (4 cấp) và **khuyến nghị giải pháp đóng bãi** (6 nhóm)
4. **So sánh nhiều BCL** trên cùng một dashboard (bảng xếp hạng CRI)
5. **Xuất báo cáo** kỹ thuật dạng Word, PDF, Excel

---

## 2. Cơ sở kỹ thuật

### 2.1. Căn cứ pháp lý và kỹ thuật

| Văn bản | Nội dung áp dụng |
|---------|-----------------|
| Điều 32, TT 02/2022/TT-BTNMT | Yêu cầu đóng bãi CTRSH |
| QCVN 96:2025/BNNMT | Quy chuẩn BCL chất thải rắn |
| TCVN 13766:2023 | Yêu cầu thiết kế BCL hợp vệ sinh |
| Đề tài TNMT.2024.05.05 (ĐH Thủy Lợi, 2026) | Phương pháp CRI và phân loại giải pháp |

### 2.2. Phương pháp tính CRI

**14 thông số chia thành 3 nhóm:**

#### Nhóm H — Nguồn nguy hại (trọng số nhóm: 0,28)

| Mã | Thông số | Trọng số trong H |
|----|----------|-----------------|
| H1 | Thời gian ngừng tiếp nhận chất thải (năm) | 0,35 |
| H2 | Diện tích BCL (ha) | 0,32 |
| H3 | Thành phần chất thải nguy hại (%) | 0,15 |
| H4 | Lượng nước rỉ rác quan sát được | 0,18 |

#### Nhóm P — Đường lan truyền (trọng số nhóm: 0,40)

| Mã | Thông số | Trọng số trong P |
|----|----------|-----------------|
| P1 | Tình trạng lớp phủ bề mặt | 0,15 |
| P2 | Lượng mưa trung bình năm (mm/năm) | 0,12 |
| P3 | Đặc điểm địa chất khu vực BCL | 0,22 |
| P4 | Khoảng cách đến nguồn nước mặt (m) | 0,17 |
| P5 | Khoảng cách đến mực nước ngầm (m) | 0,23 |
| P6 | Độ dốc địa hình khu vực BCL (%) | 0,12 |

#### Nhóm R — Đối tượng tiếp nhận (trọng số nhóm: 0,32)

| Mã | Thông số | Trọng số trong R |
|----|----------|-----------------|
| R1 | Mục đích sử dụng nguồn nước mặt và nước ngầm | 0,39 |
| R2 | Số người sống trong phạm vi 1.000 m quanh BCL | 0,24 |
| R3 | Tỷ lệ khiếu nại/phản ánh của cộng đồng (%) | 0,20 |
| R4 | Khoảng cách đến hệ sinh thái cần bảo vệ (m) | 0,17 |

### 2.3. Công thức tính

```
Bước 1 — Chỉ số từng nhóm (trung bình cộng có trọng số):
  H = 0,35·H1 + 0,32·H2 + 0,15·H3 + 0,18·H4
  P = 0,15·P1 + 0,12·P2 + 0,22·P3 + 0,17·P4 + 0,23·P5 + 0,12·P6
  R = 0,39·R1 + 0,24·R2 + 0,20·R3 + 0,17·R4 (lưu ý: tổng trọng số R = 1,00)

Bước 2 — Chỉ số rủi ro tổng hợp (trung bình nhân có trọng số):
  CRI = H^0,28 × P^0,40 × R^0,32

Phạm vi: CRI ∈ [0,25; 1,00]
```

### 2.4. Thang phân loại rủi ro

| CRI | Cấp | Mức độ rủi ro |
|-----|-----|---------------|
| < 0,36 | Cấp 1 | Rủi ro thấp |
| 0,36 – < 0,53 | Cấp 2 | Rủi ro trung bình |
| 0,53 – < 0,69 | Cấp 3 | Rủi ro cao |
| 0,69 – 1,00 | Cấp 4 | Rủi ro rất cao |

### 2.5. Giải pháp khuyến nghị theo phân loại BCL

| Mã | Phân loại | Tiêu chí | Giải pháp |
|----|-----------|----------|-----------|
| 1.1 | BCL-HVS đạt chuẩn | Đạt QCVN 96:2025 | Đóng bãi cơ bản (GP 2.1) |
| 1.2 | BCL-HVS cần bổ sung | Chưa đạt đầy đủ QCVN 96:2025 | Đóng bãi tăng cường (GP 2.2) |
| 2.1 | BCL-KHVS rủi ro thấp | CRI < 0,36 | Nhóm GP 1 (đơn giản/xanh) |
| 2.2 | BCL-KHVS rủi ro trung bình | 0,36 ≤ CRI < 0,53 | GP 2.1 (cơ bản) |
| 2.3 | BCL-KHVS rủi ro cao | 0,53 ≤ CRI < 0,69 | GP 2.2 (tăng cường) |
| 2.4 | BCL-KHVS rủi ro rất cao | CRI ≥ 0,69 | Nhóm GP 3 (nâng cao) |

---

## 3. Kiến trúc ứng dụng

```
landfill-cri-tool/
│
├── app.py                          ← Entry point, navigation chính
├── requirements.txt                ← Python dependencies
├── .streamlit/
│   └── config.toml                 ← Theme, cài đặt Streamlit
│
├── config/
│   ├── parameters.py               ← 14 thông số, trọng số, ngưỡng điểm, label
│   └── solutions.py                ← 6 giải pháp, hạng mục, điều kiện áp dụng
│
├── core/
│   ├── calculator.py               ← Tính H, P, R, CRI
│   └── classifier.py               ← Phân loại → cấp rủi ro → giải pháp
│
├── pages/
│   ├── 1_Giới_thiệu.py             ← Hướng dẫn sử dụng, sơ đồ quy trình
│   ├── 2_Khai_báo_BCL.py           ← Form nhập thông tin BCL
│   ├── 3_Nhập_CRI.py               ← Form 14 thông số CRI
│   ├── 4_Kết_quả.py                ← Dashboard kết quả đơn BCL
│   ├── 5_So_sánh_BCL.py            ← Dashboard so sánh nhiều BCL
│   └── 6_Xuất_báo_cáo.py           ← Xuất Word/PDF/Excel
│
├── export/
│   ├── excel_export.py             ← Xuất Excel (openpyxl)
│   ├── word_export.py              ← Xuất Word (python-docx)
│   ├── pdf_export.py               ← Xuất PDF (reportlab)
│   └── templates/
│       └── bao_cao_template.docx   ← Template Word có sẵn định dạng
│
├── utils/
│   ├── charts.py                   ← Plotly: radar, gauge, bar, scatter
│   ├── session.py                  ← Quản lý session state (lưu nhiều BCL)
│   └── validators.py               ← Kiểm tra dữ liệu đầu vào
│
├── data/
│   └── sample_data.json            ← Dữ liệu mẫu (ví dụ từ PL2.4)
│
└── assets/
    └── logo.png                    ← Logo tổ chức (nếu có)
```

---

## 4. Chức năng chi tiết từng trang

### Trang 1 — Giới thiệu
- Mô tả mục đích công cụ, phạm vi áp dụng
- Sơ đồ quy trình: Khai báo → Nhập CRI → Kết quả → Xuất báo cáo
- Hướng dẫn sử dụng ngắn gọn từng bước
- Link tài liệu tham khảo (JICA, TT02/2022, QCVN 96:2025)

### Trang 2 — Khai báo thông tin BCL
- Thông tin định danh: tên BCL, tỉnh/thành, huyện, tọa độ GPS
- Đặc điểm vật lý: diện tích (ha), thể tích ước tính (m³), chiều cao ước tính (m)
- Lịch sử hoạt động: năm bắt đầu, năm ngừng tiếp nhận
- **Rẽ nhánh loại hình:**
  - BCL-HVS → Checklist 5 tiêu chí đạt chuẩn → Kết quả ngay
  - BCL-KHVS → Chuyển sang Trang 3 nhập CRI
- Lưu BCL vào session (cho phép thêm nhiều BCL)

### Trang 3 — Nhập 14 thông số CRI
- Bố cục 3 cột (H / P / R), mỗi thông số gồm:
  - Label tiếng Việt + tooltip giải thích
  - Input: dropdown mô tả HOẶC ô nhập số (tự động quy đổi điểm)
  - Hiển thị điểm quy đổi ngay khi chọn (0,25 / 0,50 / 0,75 / 1,00)
  - Thanh màu trực quan (xanh → đỏ)
- Nút "Tính CRI" → chuyển sang Trang 4

### Trang 4 — Kết quả & Phân tích (1 BCL)
- **Thẻ kết quả chính:** CRI, cấp rủi ro, màu nền (xanh/vàng/cam/đỏ)
- **Biểu đồ:**
  - Radar chart: 14 thông số (Plotly)
  - Gauge chart: CRI trên thang 0,25–1,00
  - Bar chart: H, P, R so sánh
  - Heatmap: điểm từng thông số theo màu
- **Phân tích tự động:** nhận diện top 3 thông số rủi ro cao nhất, diễn giải
- **Giải pháp khuyến nghị:** hạng mục bắt buộc, tùy chọn, ưu/nhược, chi phí

### Trang 5 — So sánh nhiều BCL *(tính năng đặc trưng)*
- **Bảng xếp hạng:** tất cả BCL đã nhập, sắp xếp theo CRI giảm dần
  - Cột: Tên BCL | Tỉnh | Diện tích | H | P | R | CRI | Cấp | Giải pháp
  - Màu nền dòng theo cấp rủi ro
- **Biểu đồ so sánh:**
  - Scatter plot: CRI vs Diện tích BCL (kích thước bong bóng = dân số)
  - Bar chart so sánh H/P/R của các BCL
  - Bản đồ phân bố (nếu có tọa độ GPS) dùng Plotly mapbox
- **Bộ lọc:** theo tỉnh, cấp rủi ro, giải pháp khuyến nghị
- **Xuất danh sách** sang Excel

### Trang 6 — Xuất báo cáo
- Chọn BCL cần xuất (một hoặc tất cả)
- **Excel:** 3 sheet (Thông tin BCL | Bảng CRI | Kết quả & Giải pháp)
- **Word:** Báo cáo kỹ thuật đầy đủ theo mẫu (thông tin BCL, bảng CRI, biểu đồ nhúng, giải pháp, căn cứ pháp lý)
- **PDF:** Phiên bản in ấn của báo cáo Word

---

## 5. Yêu cầu kỹ thuật

### Dependencies

```
streamlit>=1.35.0
plotly>=5.20.0
pandas>=2.0.0
openpyxl>=3.1.0
python-docx>=1.1.0
reportlab>=4.2.0
Pillow>=10.0.0
kaleido>=0.2.1          # Xuất biểu đồ Plotly sang ảnh (nhúng vào Word/PDF)
```

### Phiên bản Python tối thiểu: 3.11

### Streamlit config (.streamlit/config.toml)
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 10
```

---

## 6. Triển khai

### Chạy cục bộ
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Deploy lên Streamlit Community Cloud (chia sẻ công khai)
1. Tạo repository GitHub (public hoặc private)
2. Push toàn bộ code lên repo
3. Đăng nhập https://share.streamlit.io → "New app"
4. Chọn repo, branch `main`, file `app.py`
5. Deploy → nhận URL dạng `https://[tên-app].streamlit.app`
6. Chia sẻ URL cho đồng nghiệp/cơ quan — không cần cài đặt gì

---

## 7. Hạn chế cần lưu ý

| Hạn chế | Nguyên nhân | Hướng xử lý |
|---------|-------------|-------------|
| Dữ liệu mất khi tắt tab | Streamlit dùng session state, không có database | Xuất Excel để lưu; phiên bản sau có thể thêm SQLite |
| Bản đồ cần tọa độ GPS | Plotly mapbox yêu cầu lat/lon | Trường tọa độ không bắt buộc |
| Xuất PDF tiếng Việt | Font tiếng Việt trong reportlab cần cấu hình | Dùng font DejaVu hoặc export qua Word trước |
| Không phân quyền người dùng | Streamlit Community Cloud không có auth | Thêm st-authenticator nếu cần |

---

## 8. Lộ trình phát triển

| Phiên bản | Nội dung | Thời gian |
|-----------|----------|-----------|
| **v1.0** | 6 trang đầy đủ, tính CRI, xuất Excel + Word | Sprint 1–2 (2 tuần) |
| **v1.1** | Bản đồ phân bố BCL (Plotly mapbox), lọc nâng cao | Sprint 3 |
| **v1.2** | Lưu dữ liệu SQLite, lịch sử đánh giá | Sprint 4 |
| **v2.0** | Phân quyền người dùng | Tương lai |

---

## 9. Ghi chú cho AI hỗ trợ phát triển (Codex/Claude)

- **Ngôn ngữ giao diện:** Tiếng Việt duy nhất, đầy đủ dấu — không hỗ trợ đa ngôn ngữ
- **Tên biến:** tiếng Anh (snake_case), comment tiếng Việt
- **Dữ liệu thông số CRI:** lấy chính xác từ PROJECT_BRIEF.md, không tự ý thay đổi trọng số
- **Công thức CRI:** dùng `math.pow()` hoặc toán tử `**`, kiểm tra domain [0.25, 1.00]
- **Session state key:** prefix `bcl_` để tránh xung đột
- **Xuất biểu đồ:** dùng `plotly.io.to_image()` kết hợp `kaleido` để nhúng vào Word/PDF
- **Màu cấp rủi ro:** Cấp 1 `#2ecc71`, Cấp 2 `#f39c12`, Cấp 3 `#e67e22`, Cấp 4 `#e74c3c`
- **Validate đầu vào:** tổng trọng số H = 1,00, P = 1,01 (làm tròn), R = 1,00 — không cần normalize lại

---

*PROJECT_BRIEF.md — v1.0 — 2026-06-07*
*Tham chiếu: Đề tài TNMT.2024.05.05, Trường ĐH Thủy Lợi*
