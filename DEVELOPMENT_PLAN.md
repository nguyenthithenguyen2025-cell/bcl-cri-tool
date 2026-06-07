# KẾ HOẠCH PHÁT TRIỂN — BCL-CRI Tool v1.0

**Ngày lập:** 2026-06-07  
**Mục tiêu:** Web app Streamlit hoàn chỉnh, deploy được lên Streamlit Community Cloud

---

## TỔNG QUAN SPRINT

| Sprint | Nội dung | Ưu tiên | Trạng thái |
|--------|----------|---------|------------|
| Sprint 1 | Khung sườn + Logic tính CRI | P0 — Bắt buộc | ⬜ Chưa bắt đầu |
| Sprint 2 | Giao diện 6 trang đầy đủ | P0 — Bắt buộc | ⬜ Chưa bắt đầu |
| Sprint 3 | Biểu đồ + Dashboard so sánh | P0 — Bắt buộc | ⬜ Chưa bắt đầu |
| Sprint 4 | Xuất báo cáo Word/Excel/PDF | P1 — Quan trọng | ⬜ Chưa bắt đầu |
| Sprint 5 | Kiểm thử + Tinh chỉnh + Deploy | P0 — Bắt buộc | ⬜ Chưa bắt đầu |

---

## SPRINT 1 — Khung sườn & Logic tính CRI

**Mục tiêu:** Code thuần Python, test được không cần Streamlit  
**Files cần tạo:**

### 1.1. `requirements.txt`
```
streamlit>=1.35.0
plotly>=5.20.0
pandas>=2.0.0
openpyxl>=3.1.0
python-docx>=1.1.0
reportlab>=4.2.0
Pillow>=10.0.0
kaleido>=0.2.1
```

### 1.2. `config/parameters.py`
Nội dung: Dictionary chứa toàn bộ 14 thông số CRI:
- Mã (H1–H4, P1–P6, R1–R4)
- Tên tiếng Việt
- Trọng số trong nhóm
- Các mức điểm: {0.25: mô tả, 0.50: mô tả, 0.75: mô tả, 1.00: mô tả}
- Loại input: "dropdown" hoặc "numeric" (nếu numeric: ngưỡng quy đổi)
- Đơn vị (nếu có)

### 1.3. `config/solutions.py`
Nội dung: Dictionary 6 nhóm giải pháp:
- Mã giải pháp (1.1, 1.2, 2.1, 2.2, 2.3, 2.4)
- Tên giải pháp
- Điều kiện áp dụng (loại BCL + ngưỡng CRI)
- Hạng mục bắt buộc (list)
- Hạng mục tùy chọn (list)
- Điều kiện áp dụng chi tiết
- Ưu điểm, hạn chế
- Chi phí tương đối
- Lưu ý đặc biệt

### 1.4. `core/calculator.py`
Nội dung:
```python
def score_numeric(value, thresholds, scores):
    """Quy đổi giá trị số thực → điểm (0.25/0.50/0.75/1.00)"""

def calculate_H(scores: dict) -> float:
    """H = 0.35·H1 + 0.32·H2 + 0.15·H3 + 0.18·H4"""

def calculate_P(scores: dict) -> float:
    """P = 0.15·P1 + 0.12·P2 + 0.22·P3 + 0.17·P4 + 0.23·P5 + 0.12·P6"""

def calculate_R(scores: dict) -> float:
    """R = 0.39·R1 + 0.24·R2 + 0.20·R3 + 0.17·R4"""

def calculate_CRI(H: float, P: float, R: float) -> float:
    """CRI = H^0.28 × P^0.40 × R^0.32"""

def get_top_risk_factors(scores: dict, n=3) -> list:
    """Trả về top N thông số có điểm rủi ro cao nhất"""
```

### 1.5. `core/classifier.py`
Nội dung:
```python
def classify_risk_level(CRI: float) -> dict:
    """CRI → {cap, ten_cap, mau, hanh_dong}"""

def recommend_solution(bcl_type: str, CRI: float) -> dict:
    """Loại BCL + CRI → giải pháp khuyến nghị đầy đủ"""

def generate_analysis_text(H, P, R, CRI, scores) -> str:
    """Tạo văn bản nhận xét tự động bằng tiếng Việt"""
```

### 1.6. `utils/session.py`
Nội dung: Quản lý danh sách BCL trong `st.session_state`
```python
def init_session()           # Khởi tạo session state
def add_bcl(bcl_data: dict)  # Thêm BCL mới
def update_bcl(id, data)     # Cập nhật BCL
def delete_bcl(id)           # Xóa BCL
def get_all_bcl() -> list    # Lấy tất cả BCL
def get_bcl_dataframe()      # Trả về DataFrame cho so sánh
```

### 1.7. `utils/validators.py`
Nội dung: Kiểm tra đầu vào
```python
def validate_bcl_info(data: dict) -> list  # List lỗi (rỗng = hợp lệ)
def validate_cri_scores(scores: dict) -> list
def check_missing_data(scores: dict) -> list  # Thông số chưa nhập
```

**Kiểm thử Sprint 1:** Chạy `python core/calculator.py` → so sánh với ví dụ PL2.4
- Expected: H ≈ 0,595 | P ≈ 0,673 | R ≈ 0,713 | CRI ≈ 0,662

---

## SPRINT 2 — Giao diện 6 trang Streamlit

**Mục tiêu:** Mỗi trang chạy được, form đầy đủ, session state hoạt động

### 2.1. `app.py` — Navigation chính
- Cấu hình `st.set_page_config()`: title, icon, layout wide
- Sidebar: logo, tên app, phiên bản
- Sidebar: danh sách BCL đã nhập (badge số lượng)
- Navigation: st.navigation() → 6 trang

### 2.2. `.streamlit/config.toml`
- Theme màu xanh dương chuyên nghiệp
- Font sans-serif

### 2.3. `pages/1_Giới_thiệu.py`
- Tiêu đề, mô tả mục đích
- Sơ đồ quy trình dạng mermaid hoặc ảnh tĩnh
- Hướng dẫn 6 bước sử dụng
- Accordion: Căn cứ pháp lý, Tài liệu tham khảo
- Nút "Bắt đầu đánh giá BCL mới" → chuyển Trang 2

### 2.4. `pages/2_Khai_báo_BCL.py`
- Form 2 cột:
  - Trái: Thông tin định danh (tên, tỉnh, huyện, tọa độ)
  - Phải: Đặc điểm vật lý (diện tích, thể tích, chiều cao)
- Dòng phụ: Lịch sử (năm bắt đầu, năm ngừng)
- Radio: Loại hình BCL
  - Nếu HVS → hiện checklist 5 tiêu chí → nút "Xác nhận loại hình"
  - Nếu KHVS → nút "Tiếp theo: Nhập thông số CRI"
- Thông tin người đánh giá, ngày đánh giá

### 2.5. `pages/3_Nhập_CRI.py`
- Header: Tên BCL đang đánh giá (từ session)
- Progress bar: % thông số đã nhập
- 3 expander theo nhóm (H / P / R):
  - Mỗi thông số: label + tooltip + input + hiển thị điểm ngay
  - Input dạng dropdown (thông số mô tả) hoặc number_input (thông số số)
  - Chỉ báo màu: xanh (thấp) → vàng → cam → đỏ (cao)
- Panel bên phải (cố định): Preview H, P, R theo thời gian thực
- Nút "Tính CRI & Xem kết quả"
- Cảnh báo nếu thiếu thông số (nguyên tắc thận trọng: gán 1,00)

### 2.6. `pages/4_Kết_quả.py`
- Selector: chọn BCL (nếu có nhiều trong session)
- Thẻ kết quả lớn: CRI, cấp, màu, giải pháp tóm tắt
- Tabs: [Biểu đồ] [Phân tích chi tiết] [Giải pháp đầy đủ]
- Nút: "Thêm BCL khác" | "Xem so sánh" | "Xuất báo cáo"

### 2.7. `pages/5_So_sánh_BCL.py`
- Cần ít nhất 2 BCL trong session → hiện cảnh báo nếu chưa đủ
- Bảng xếp hạng (DataFrame có màu)
- Bộ lọc: tỉnh, cấp rủi ro
- Tabs: [Bảng xếp hạng] [Biểu đồ so sánh] [Bản đồ]
- Nút xuất danh sách Excel

### 2.8. `pages/6_Xuất_báo_cáo.py`
- Multiselect: chọn BCL cần xuất
- Radio: định dạng (Excel / Word / PDF)
- Preview nội dung báo cáo (collapsible)
- Nút tải xuống (st.download_button)

---

## SPRINT 3 — Biểu đồ & Dashboard so sánh

**Files:** `utils/charts.py`

### Biểu đồ đơn BCL (Trang 4):
```
1. Radar chart (14 thông số)
   - Trục: tên thông số (viết tắt: H1, H2,... P1,... R1,...)
   - Giá trị: điểm 0.25–1.00
   - Fill màu theo cấp rủi ro
   - Tooltip: tên đầy đủ + giá trị thực tế

2. Gauge chart (CRI)
   - Thang: 0.25 → 1.00
   - 4 vùng màu (xanh/vàng/cam/đỏ)
   - Kim chỉ giá trị CRI
   - Hiển thị H, P, R dưới gauge

3. Bar chart ngang (H, P, R so sánh)
   - 3 thanh + 1 thanh CRI
   - Đường kẻ ngưỡng phân loại

4. Heatmap điểm thông số
   - Grid 3×6 (hoặc 4 hàng)
   - Màu cell theo điểm
```

### Biểu đồ so sánh nhiều BCL (Trang 5):
```
5. Bảng xếp hạng màu
   - Pandas DataFrame + st.dataframe(styled)
   - Màu nền dòng: xanh/vàng/cam/đỏ

6. Scatter plot: CRI vs Diện tích
   - Kích thước bong bóng = dân số (R2)
   - Màu = cấp rủi ro
   - Hover: tên BCL, tỉnh, CRI

7. Bar chart nhóm: H/P/R của nhiều BCL
   - Grouped bar, mỗi nhóm 3 cột H/P/R
   - Sắp xếp theo CRI giảm dần

8. Bản đồ (nếu có tọa độ GPS)
   - Plotly scatter_mapbox
   - Màu marker = cấp rủi ro
   - Popup: tên BCL, CRI, giải pháp
```

---

## SPRINT 4 — Xuất báo cáo

### 4.1. `export/excel_export.py`
Sheet 1 — "Thông tin BCL": Tên, tỉnh, diện tích, loại hình, ngày đánh giá  
Sheet 2 — "Bảng CRI": 14 thông số | Giá trị thực | Điểm | Trọng số | Đóng góp  
Sheet 3 — "Kết quả": H, P, R, CRI, cấp rủi ro, giải pháp  
Sheet 4 — "So sánh BCL": Nếu xuất tất cả BCL — bảng xếp hạng đầy đủ

Định dạng: header bold, freeze row 1, autofit column width, color fill theo cấp rủi ro

### 4.2. `export/word_export.py`
Cấu trúc Word:
```
1. Trang bìa: Tên BCL, Tỉnh/TP, Ngày đánh giá, Đơn vị thực hiện
2. Mục 1: Thông tin chung về BCL
3. Mục 2: Phương pháp đánh giá (tóm tắt CRI)
4. Mục 3: Kết quả đánh giá
   3.1 Bảng 14 thông số (có giá trị, điểm)
   3.2 Chỉ số H, P, R, CRI (bảng tóm tắt)
   3.3 Biểu đồ radar + gauge (ảnh nhúng từ Plotly/kaleido)
5. Mục 4: Phân tích rủi ro (văn bản tự động)
6. Mục 5: Giải pháp khuyến nghị
   5.1 Tên giải pháp, căn cứ
   5.2 Hạng mục bắt buộc, tùy chọn
   5.3 Điều kiện áp dụng, lưu ý
7. Tài liệu tham khảo
```

### 4.3. `export/pdf_export.py`
- Dùng `reportlab` với font hỗ trợ Unicode (DejaVu)
- Hoặc: chuyển đổi từ Word → PDF qua `docx2pdf` (cần MS Word cài sẵn)
- Backup: in từ trình duyệt (Ctrl+P → Save as PDF)

---

## SPRINT 5 — Kiểm thử & Deploy

### 5.1. Test cases
- [ ] Nhập đúng ví dụ PL2.4 → CRI = 0,662 ± 0,001
- [ ] Tất cả thông số = 0,25 → CRI = 0,25
- [ ] Tất cả thông số = 1,00 → CRI = 1,00
- [ ] BCL-HVS đạt chuẩn → không hiện form CRI → giải pháp 2.1
- [ ] Thiếu 1 thông số → cảnh báo thận trọng, gán 1,00
- [ ] 5 BCL khác nhau → bảng xếp hạng đúng thứ tự

### 5.2. Deploy lên Streamlit Community Cloud
1. `git init && git add . && git commit -m "init"`
2. Tạo repo GitHub → push
3. Đăng nhập https://share.streamlit.io
4. New app → chọn repo → app.py → Deploy
5. Kiểm tra URL công khai

### 5.3. Kiểm tra sau deploy
- [ ] Tất cả 6 trang load được
- [ ] Form nhập và tính CRI hoạt động
- [ ] Biểu đồ hiển thị đúng
- [ ] Download Excel/Word hoạt động
- [ ] Không lỗi encoding tiếng Việt

---

## ĐIỂM CẦN THẢO LUẬN VỚI CHỦ DỰ ÁN

### Câu hỏi kỹ thuật cần xác nhận

**[Q1] Xử lý thiếu dữ liệu**
- Tài liệu nói: "nếu không thể thu thập được, áp dụng nguyên tắc thận trọng — chấm điểm cao nhất (1,00)"
- App hiện tại: cảnh báo màu vàng + tự động gán 1,00 + ghi chú trong báo cáo
- **Xác nhận:** Có nên để người dùng ghi rõ lý do thiếu dữ liệu không?

**[Q2] Lưu dữ liệu**
- v1.0: Session state (mất khi đóng tab) → bù lại bằng xuất Excel ngay sau nhập
- Phiên bản sau: SQLite local hoặc Google Sheets API
- **Xác nhận:** v1.0 chỉ cần session + Excel là đủ không?

**[Q3] Thông số P (tổng trọng số)**
- H: 0,35+0,32+0,15+0,18 = **1,00** ✅
- P: 0,15+0,12+0,22+0,17+0,23+0,12 = **1,01** (có vẻ làm tròn từ tài liệu gốc)
- R: 0,39+0,24+0,20+0,17 = **1,00** ✅
- **Xác nhận:** Dùng đúng trọng số trong tài liệu (không normalize lại P)?

**[Q4] BCL-HVS trong dashboard so sánh**
- BCL-HVS không có chỉ số CRI → xếp hạng thế nào?
- **Đề xuất:** Hiển thị BCL-HVS riêng (không xếp hạng CRI), hoặc gán CRI = N/A và đặt cuối bảng

**[Q5] Bản đồ**
- Plotly mapbox cần Mapbox token (hoặc dùng OpenStreetMap miễn phí)
- Tọa độ GPS có thể nhập tay hoặc bỏ qua
- **Xác nhận:** Có cần tính năng bản đồ trong v1.0 không?

**[Q6] Logo và thương hiệu**
- **Xác nhận:** Dùng logo ĐH Thủy Lợi hay logo dự án riêng?

**[Q7] Ngôn ngữ báo cáo Word**
- Hiện tại: tiếng Việt hoàn toàn
- **Xác nhận:** Có cần song ngữ Việt-Anh không?

---

## PHÂN CÔNG (đề xuất)

| Nhiệm vụ | Thực hiện bởi |
|----------|---------------|
| Code toàn bộ app | Claude / Codex (AI) |
| Kiểm tra logic kỹ thuật CRI | Chủ dự án |
| Cung cấp logo, template báo cáo | Chủ dự án |
| Xác nhận nội dung giải pháp | Chủ dự án |
| Test, phản hồi lỗi | Chủ dự án |
| Deploy GitHub + Streamlit Cloud | Chủ dự án (hỗ trợ bởi AI) |

---

*DEVELOPMENT_PLAN.md — v1.0 — 2026-06-07*
