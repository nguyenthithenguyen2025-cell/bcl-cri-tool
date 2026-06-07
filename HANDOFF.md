# HANDOFF NOTE — BCL-CRI Decision Support Tool

**Ngày cập nhật:** 2026-06-07  
**Dự án:** Công cụ Hỗ trợ Quyết định Đóng bãi Chôn lấp CTRSH  
**Thư mục dự án:** `D:\1. AI_landfill\landfill-cri-tool\`

---

## 1. Trạng thái dự án hiện tại

**Sprint 1 (Core logic): HOÀN THÀNH ✅**  
**Sprint 2 (Giao diện 6 trang): HOÀN THÀNH ✅**  
**Sprint 3 (Biểu đồ + Export): HOÀN THÀNH ✅**  
**Sprint 4 (Test + Sửa lỗi + Deploy): ĐANG THỰC HIỆN 🔄** — Đã sửa lỗi logic, chưa deploy

---

## 2. Các file đã tạo (hoàn chỉnh)

```
landfill-cri-tool/
├── app.py                          ✅ Entry point Streamlit
├── requirements.txt                ✅ Dependencies (đã dọn gói thừa: reportlab, Pillow, kaleido)
├── .streamlit/config.toml          ✅ Theme và cài đặt
│
├── config/
│   ├── __init__.py                 ✅
│   ├── parameters.py               ✅ 14 thông số CRI đầy đủ với trọng số
│   └── solutions.py                ✅ 4 nhóm giải pháp (GP1, GP2.1, GP2.2, GP3)
│
├── core/
│   ├── __init__.py                 ✅
│   ├── calculator.py               ✅ Tính H, P, R, CRI (có normalize P weights)
│   └── classifier.py               ✅ Phân loại rủi ro + khuyến nghị giải pháp
│
├── pages/
│   ├── __init__.py                 ✅
│   ├── 1_Giới_thiệu.py             ✅ Trang giới thiệu + hướng dẫn
│   ├── 2_Khai_báo_BCL.py           ✅ Form nhập thông tin BCL (HVS/KHVS)
│   ├── 3_Nhập_CRI.py               ✅ Form 14 thông số CRI — ĐÃ SỬA LỖI TRÙNG BCL
│   ├── 4_Kết_quả.py                ✅ Dashboard kết quả + biểu đồ + giải pháp
│   ├── 5_So_sánh_BCL.py            ✅ Bảng xếp hạng nhiều BCL
│   └── 6_Xuất_báo_cáo.py           ✅ Xuất Excel, Word
│
├── utils/
│   ├── __init__.py                 ✅
│   ├── charts.py                   ✅ Radar, gauge, bar, heatmap, comparison, scatter
│   ├── session.py                  ✅ Quản lý nhiều BCL trong session state
│   ├── sidebar.py                  ✅ Sidebar dùng chung cho tất cả 6 trang
│   └── validators.py               ✅ Kiểm tra đầu vào BCL info + CRI scores
│
├── export/
│   ├── __init__.py                 ✅
│   ├── excel_export.py             ✅ 3-sheet Excel export (openpyxl)
│   └── word_export.py              ✅ Báo cáo Word (python-docx)
│
├── data/
│   └── sample_data.json            ✅ Dữ liệu mẫu PL2.4
│
├── assets/                         ⏳ Thư mục rỗng — chờ logo.png
│
├── PROJECT_BRIEF.md                ✅ Đặc tả kỹ thuật đầy đủ
├── DEVELOPMENT_PLAN.md             ✅ Kế hoạch 5 sprint
├── README.md                       ✅ Tóm tắt dự án
└── HANDOFF.md                      ✅ File này
```

**Các file CHƯA TẠO:**
- `export/pdf_export.py` — Chưa cần thiết (PDF xuất từ Word)
- `assets/logo.png` — Tùy người dùng cung cấp

---

## 3. Công việc VỪA HOÀN THÀNH (phiên 2026-06-07)

### Sửa lỗi logic quan trọng trong `pages/3_Nhập_CRI.py`

**Lỗi gốc:** `_bcl_active_editing_id` không bao giờ được gán sau `add_bcl` → mỗi lần nhấn "Tính CRI" tạo thêm một BCL trùng lặp. Đồng thời `_bcl_saved_info` bị xóa sau lần tính đầu → người dùng không thể điều chỉnh và tính lại.

**Fix đã áp dụng (dòng 248–265):**
```python
else:
    bcl_id = add_bcl(info=saved_info, scores=all_scores, ...)
    # Lưu id để các lần tính lại sau dùng update_bcl thay vì add_bcl
    st.session_state["_bcl_active_editing_id"] = bcl_id
    # Giữ lại _bcl_saved_info để người dùng có thể điều chỉnh và tính lại
```

### Sửa lỗi logic trong `pages/2_Khai_báo_BCL.py`

**Fix đã áp dụng (sau dòng lưu `_bcl_saved_info`):**
```python
st.session_state.pop("_bcl_active_editing_id", None)
st.session_state.pop("_cri_scores_draft", None)
st.session_state.pop("_cri_notes_draft", None)
```
Đảm bảo khi người dùng lưu một BCL mới, context cũ được xóa sạch.

### Dọn dẹp `requirements.txt`

Xóa 3 gói không dùng trong code hiện tại:
- `reportlab` (PDF export chưa implement)
- `Pillow` (không dùng trực tiếp)
- `kaleido` (chart image export chưa implement; có thể gây lỗi hệ thống trên Linux)

`requirements.txt` hiện tại còn 5 gói:
```
streamlit>=1.35.0
plotly>=5.20.0
pandas>=2.0.0
openpyxl>=3.1.0
python-docx>=1.1.0
```

---

## 4. Kết quả kiểm tra tự động

| Kiểm tra | Kết quả |
|---------|---------|
| Tất cả import (config, core, utils, export) | ✅ Không lỗi |
| Tính CRI với sample PL2.4 | ✅ H=0.6250, P=0.6658, R=0.7000, CRI=0.6647 → Cấp 3 |
| Phân loại cấp rủi ro | ✅ Cấp 3 → GP 2.2 |
| App chạy local (HTTP 200) | ✅ |
| Sidebar hiển thị trên tất cả 6 trang | ✅ (`utils/sidebar.py` dùng chung) |

---

## 5. Chi tiết kỹ thuật quan trọng

### Công thức tính CRI (đã implement)
```
H = Σ(wi·Hi)   trọng số H: [0.35, 0.32, 0.15, 0.18], tổng = 1.00
P = Σ(wi·Pi)   trọng số P raw: [0.15, 0.12, 0.22, 0.17, 0.23, 0.12], tổng = 1.01
               → normalize: chia mỗi w cho 1.01
R = Σ(wi·Ri)   trọng số R: [0.39, 0.24, 0.20, 0.17], tổng = 1.00
CRI = H^0.28 × P^0.40 × R^0.32
```

### Cấu trúc dữ liệu session

```python
st.session_state["bcl_list"] = [
    {
        "id": "ABCD1234",        # 8 ký tự hex tự sinh
        "info": {...},           # Trang 2
        "scores": {...},         # Trang 3 — 14 thông số
        "missing_notes": {...},  # Lý do thiếu dữ liệu
        "result": {
            "H", "P", "R", "CRI": float,
            "risk": {"level": 1-4, "label": str, "color": hex},
            "solution": dict,
        },
        "created_at": "ISO datetime",
    }
]
st.session_state["bcl_active_id"] = "ABCD1234"     # BCL đang xem

# Dữ liệu tạm giữa các trang:
"_bcl_saved_info"         = dict    # Thông tin BCL từ Trang 2
"_bcl_active_editing_id"  = str     # ID BCL đang nhập CRI (để update thay vì add)
"_cri_scores_draft"       = dict    # Draft điểm Trang 3
"_cri_notes_draft"        = dict    # Draft lý do thiếu
```

### Quy tắc routing BCL → Giải pháp
| Loại BCL | Điều kiện | Giải pháp |
|----------|-----------|-----------|
| BCL-KHVS | CRI < 0.36 | GP 1 (đơn giản/phủ xanh) |
| BCL-KHVS | 0.36 ≤ CRI < 0.53 | GP 2.1 (cơ bản) |
| BCL-KHVS | 0.53 ≤ CRI < 0.69 | GP 2.2 (tăng cường) |
| BCL-KHVS | CRI ≥ 0.69 | GP 3 (nâng cao) |
| BCL-HVS đạt chuẩn | — | GP 2.1 |
| BCL-HVS cần bổ sung | — | GP 2.2 |

---

## 6. Bước tiếp theo (theo thứ tự ưu tiên)

### Bước 3 — Test thủ công trong trình duyệt ⚠️ CHƯA THỰC HIỆN

Chạy app:
```bash
cd D:\1. AI_landfill\landfill-cri-tool
streamlit run app.py
```

Kiểm tra theo luồng sau:
1. **Trang 2 — Khai báo BCL:**
   - Nhấn "📂 Nạp dữ liệu mẫu từ Ví dụ PL2.4"
   - Kiểm tra các trường đã điền
   - Nhấn "💾 Lưu thông tin BCL"
   - Xác nhận thông báo thành công

2. **Trang 3 — Nhập CRI:**
   - Nhấn "📂 Nạp điểm mẫu từ Ví dụ PL2.4"
   - Nhấn "🔢 Tính CRI"
   - Kiểm tra: CRI ≈ 0,665 → Cấp 3 → GP 2.2
   - **Thay đổi 1-2 thông số và tính lại** → xác nhận KHÔNG tạo BCL trùng (đây là lỗi đã sửa)

3. **Trang 4 — Kết quả:**
   - Kiểm tra biểu đồ radar, đồng hồ gauge, bar chart, heatmap hiển thị đúng
   - Kiểm tra phần "Giải pháp khuyến nghị" hiển thị GP 2.2

4. **Trang 5 — So sánh BCL:**
   - Thêm một BCL thứ hai (Trang 2 → Trang 3)
   - Kiểm tra bảng xếp hạng và biểu đồ comparison

5. **Trang 6 — Xuất báo cáo:**
   - Nhấn "📥 Tạo file Excel" → tải xuống → mở kiểm tra 3 sheet
   - Nhấn "📥 Tạo file Word" → tải xuống → mở kiểm tra nội dung

### Bước 4 — Deploy lên Streamlit Community Cloud

**Yêu cầu:** Tài khoản GitHub + tài khoản Streamlit Community Cloud.

```bash
# 1. Khởi tạo git repo
cd D:\1. AI_landfill\landfill-cri-tool
git init
git add .
git commit -m "BCL-CRI Tool v1.0 — initial release"

# 2. Tạo repo trên GitHub (qua web hoặc gh CLI)
gh repo create bcl-cri-tool --public --source=. --remote=origin --push
# Hoặc thủ công: tạo repo trên github.com → git remote add origin <URL> → git push -u origin main

# 3. Deploy trên Streamlit Community Cloud
# - Truy cập https://share.streamlit.io
# - Đăng nhập bằng GitHub
# - New app → chọn repo → branch: main → Main file: app.py
# - Deploy → lấy URL dạng https://your-app.streamlit.app
```

**Lưu ý deploy:**
- Tên file pages có dấu tiếng Việt (vd: `3_Nhập_CRI.py`) — hoạt động bình thường trên Linux
- `requirements.txt` tự động đọc, không cần cấu hình thêm
- Session state chỉ tồn tại trong phiên — dữ liệu mất khi refresh

### Bước 5 — Cập nhật sample_data.json (tùy chọn)

Hiện tại CRI tính được = 0.6647 (tài liệu gốc PL2.4: 0.662). Chênh lệch nhỏ do điểm mẫu chưa khớp hoàn toàn. Khi có bảng điểm gốc từ PL2.4, cập nhật:

`D:\1. AI_landfill\landfill-cri-tool\data\sample_data.json`

Để đạt đúng H=0.595, P=0.673, R=0.713, CRI=0.662.

---

## 7. Vấn đề chưa giải quyết

| Vấn đề | Mức độ | Ghi chú |
|--------|--------|---------|
| Test thủ công trình duyệt | Cao | Cần thực hiện trước deploy — xem Bước 3 |
| Deploy GitHub + Streamlit Cloud | Cao | Cần tài khoản GitHub |
| Điểm mẫu PL2.4 chưa khớp chính xác | Trung bình | CRI = 0.6647 vs. 0.662 — vẫn đúng cấp rủi ro |
| Logo ứng dụng | Thấp | `assets/logo.png` chưa có, sidebar vẫn hoạt động |
| PDF export | Thấp | `pdf_export.py` chưa tạo — người dùng xuất từ Word |
| Tên file pages tiếng Việt trên GitHub | Thấp | Git xử lý UTF-8 tốt trên Linux; Windows có thể cần `.gitattributes` |

---

## 8. File `.gitattributes` đề xuất cho deploy

Tạo file này để đảm bảo tên file UTF-8 hoạt động đúng trên GitHub/Linux:

```
# .gitattributes
* text=auto eol=lf
*.py text eol=lf
*.md text eol=lf
*.toml text eol=lf
*.txt text eol=lf
*.json text eol=lf
```

---

*HANDOFF.md — BCL-CRI Tool v1.0 — Cập nhật 2026-06-07*  
*Phiên làm việc: Sửa lỗi duplicate BCL + recalculation + dọn requirements.txt*
