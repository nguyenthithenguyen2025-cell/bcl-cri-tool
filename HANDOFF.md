# HANDOFF NOTE — BCL-CRI Decision Support Tool

**Ngày cập nhật:** 2026-06-07 (Phiên 4)
**Dự án:** Công cụ Hỗ trợ Quyết định Đóng bãi Chôn lấp CTRSH
**Thư mục dự án:** `D:\1. AI_landfill\landfill-cri-tool\`
**Git:** Branch `master` — Commit hiện tại: `8e5439d`
**GitHub:** https://github.com/nguyenthithenguyen2025-cell/bcl-cri-tool

---

## 1. Trạng thái dự án hiện tại

| Sprint | Nội dung | Trạng thái |
|--------|----------|-----------|
| Sprint 1 | Core logic (calculator, classifier, config) | ✅ HOÀN THÀNH |
| Sprint 2 | Giao diện 6 trang Streamlit | ✅ HOÀN THÀNH |
| Sprint 3 | Biểu đồ (6 loại) + Export Excel/Word | ✅ HOÀN THÀNH |
| Sprint 4 | Test + Sửa lỗi + Git commit | ✅ HOÀN THÀNH |
| Sprint 5 | HTML demo để kiểm tra trước | ✅ HOÀN THÀNH (Phiên 3) |
| Sprint 6 | Deploy GitHub + Streamlit Cloud | ✅ HOÀN THÀNH (Phiên 4) |

**Tóm tắt:** App Streamlit hoàn chỉnh, đã deploy thành công. Test thủ công 5 bước không có lỗi.

**URL công khai:** https://bcl-cri-tool-f7bzdcw6lzg6yz92ouerqz.streamlit.app  
**GitHub:** https://github.com/nguyenthithenguyen2025-cell/bcl-cri-tool  
**Git working tree hiện tại:** Sạch — tất cả file đã commit và push.

---

## 2. Những gì vừa hoàn thành (Phiên 3 — 2026-06-07)

### 2.1 Tạo file HTML demo — `bcl_cri_demo.html`

**File:** `D:\1. AI_landfill\landfill-cri-tool\bcl_cri_demo.html`
**Mục đích:** Kiểm tra logic CRI và giao diện mà không cần cài Python/Streamlit.
**Cách mở:** Double-click → mở bằng Chrome/Edge/Firefox. Cần internet để biểu đồ Chart.js hiển thị.

**Tính năng trong demo HTML:**

| Tính năng | Có |
|-----------|-----|
| Form khai báo BCL (KHVS/HVS) với 10 trường | ✅ |
| Nút nạp dữ liệu mẫu PL2.4 (cả BCL info + 14 điểm) | ✅ |
| Form nhập 14 thông số CRI (3 nhóm H/P/R) | ✅ |
| Màu điểm thay đổi theo mức (xanh/vàng/cam/đỏ) | ✅ |
| Tính CRI đúng công thức `H^0.28 × P^0.40 × R^0.32` | ✅ |
| Phân loại 4 cấp rủi ro + màu tương ứng | ✅ |
| Top 3 thông số rủi ro cao nhất | ✅ |
| Biểu đồ radar 14 thông số (Chart.js 4.4.0) | ✅ |
| Biểu đồ cột H/P/R | ✅ |
| 4 nhóm giải pháp khuyến nghị đầy đủ (GP1/2.1/2.2/3) | ✅ |
| BCL-HVS: bỏ qua CRI, đi thẳng đến giải pháp | ✅ |
| Giao diện tiếng Việt, responsive (mobile/desktop) | ✅ |

**Kết quả kỳ vọng khi nạp mẫu:** H=0,6250 | P=0,6658 | R=0,7000 | CRI=0,6647 → Cấp 3 → GP 2.2 ✅

**Demo HTML KHÔNG có (chỉ có trong Streamlit app):**
- Trang 1 (Giới thiệu phương pháp)
- Quản lý nhiều BCL cùng lúc
- Trang 5 — So sánh nhiều BCL
- Trang 6 — Xuất báo cáo Excel/Word
- Biểu đồ gauge và heatmap
- Session state (dữ liệu tồn tại khi chuyển trang)

### 2.2 Cập nhật `.gitignore`

Thêm `bcl_cri_demo.html` vào `.gitignore` để không đưa file demo vào git repository (file này chỉ dùng để kiểm tra cục bộ).

```gitignore
__pycache__/
*.pyc
*.pyo
.env
streamlit_log.txt
assets/logo.png
bcl_cri_demo.html
```

---

## 3. Tất cả file dự án (31 files trong git)

```
landfill-cri-tool/
├── app.py                          ✅ Entry point Streamlit
├── requirements.txt                ✅ streamlit, plotly, pandas, openpyxl, python-docx
├── .streamlit/config.toml          ✅ Theme xanh lá, layout wide
├── .gitattributes                  ✅ UTF-8/LF cho file tiếng Việt
├── .gitignore                      ✅ Loại trừ __pycache__, .env, bcl_cri_demo.html...
│
├── config/
│   ├── __init__.py
│   ├── parameters.py               ✅ 14 thông số CRI đầy đủ với trọng số
│   └── solutions.py                ✅ 4 nhóm giải pháp (GP1, GP2.1, GP2.2, GP3)
│
├── core/
│   ├── __init__.py
│   ├── calculator.py               ✅ calculate_cri() → {H, P, R, CRI}
│   └── classifier.py               ✅ classify_and_recommend() → {risk, solution}
│
├── pages/
│   ├── __init__.py
│   ├── 1_Giới_thiệu.py             ✅ Trang giới thiệu + hướng dẫn
│   ├── 2_Khai_báo_BCL.py           ✅ Form nhập thông tin BCL (HVS/KHVS)
│   ├── 3_Nhập_CRI.py               ✅ Form 14 thông số CRI — đã sửa lỗi trùng BCL
│   ├── 4_Kết_quả.py                ✅ Dashboard + 4 biểu đồ + giải pháp
│   ├── 5_So_sánh_BCL.py            ✅ Bảng xếp hạng + biểu đồ so sánh nhiều BCL
│   └── 6_Xuất_báo_cáo.py           ✅ Xuất Excel (3 sheet) + Word
│
├── utils/
│   ├── __init__.py
│   ├── charts.py                   ✅ radar, gauge, bar_group, heatmap, comparison, scatter
│   ├── session.py                  ✅ add_bcl, update_bcl, get_active_bcl, get_all_bcl
│   ├── sidebar.py                  ✅ render_sidebar() — dùng chung 6 trang
│   └── validators.py               ✅ validate_bcl_info, validate_scores
│
├── export/
│   ├── __init__.py
│   ├── excel_export.py             ✅ export_to_excel() → BytesIO (8,532 bytes)
│   └── word_export.py              ✅ export_to_word() → BytesIO (39,197 bytes)
│
├── data/
│   └── sample_data.json            ✅ Dữ liệu mẫu PL2.4
│
├── assets/                         ⏳ Thư mục rỗng (logo.png chưa có — không ảnh hưởng)
│
├── PROJECT_BRIEF.md                ✅
├── DEVELOPMENT_PLAN.md             ✅
├── README.md                       ✅
└── HANDOFF.md                      ✅ File này

── NGOÀI git (không track) ──
└── bcl_cri_demo.html               ✅ Demo HTML kiểm tra cục bộ (trong .gitignore)
```

---

## 4. Bước tiếp theo — Deploy (ưu tiên cao nhất)

### Bước 0: Commit 2 file thay đổi chưa vào git

```bash
cd D:\1. AI_landfill\landfill-cri-tool
git add .gitignore HANDOFF.md
git commit -m "Update .gitignore and HANDOFF after Sprint 5 (HTML demo)"
```

### Bước 1: Push lên GitHub

**Cách A — Qua GitHub CLI (nhanh nhất, nếu đã cài `gh`):**
```bash
gh repo create bcl-cri-tool --public --source=. --remote=origin --push
```

**Cách B — Thủ công:**
1. Truy cập https://github.com/new
2. Tạo repo tên `bcl-cri-tool` (Public, **không** tick "Add a README file")
3. Copy URL repo (dạng `https://github.com/TEN_USER/bcl-cri-tool.git`)
4. Chạy lệnh:
```bash
git remote add origin https://github.com/TEN_USER/bcl-cri-tool.git
git push -u origin master
```

> **Lưu ý tên branch:** Local đang dùng `master`. Nếu muốn đổi sang `main` (convention GitHub mới):
> ```bash
> git branch -m master main
> git push -u origin main
> ```

**Kiểm tra thành công:** Truy cập `https://github.com/TEN_USER/bcl-cri-tool` — phải thấy 31 files.

### Bước 2: Deploy trên Streamlit Community Cloud

1. Truy cập https://share.streamlit.io
2. Đăng nhập bằng tài khoản GitHub (cùng tài khoản vừa push)
3. Nhấn **New app**
4. Điền:
   - Repository: `TEN_USER/bcl-cri-tool`
   - Branch: `master` (hoặc `main` nếu đã đổi)
   - Main file path: `app.py`
5. Nhấn **Deploy** → chờ ~3-5 phút
6. URL sẽ có dạng: `https://bcl-cri-tool.streamlit.app`

**Không cần cấu hình thêm:** `requirements.txt` được đọc tự động. Tên file tiếng Việt hoạt động bình thường trên Linux nhờ `.gitattributes`.

### Bước 3: Kiểm tra sau deploy

Luồng test đầu đủ sau khi app lên cloud:

1. **Trang 2 — Khai báo BCL:** Nạp dữ liệu mẫu → Lưu BCL → xác nhận chuyển sang Trang 3
2. **Trang 3 — Nhập CRI:** Nạp điểm mẫu → Tính CRI → kiểm tra: CRI ≈ 0,665, Cấp 3, GP 2.2
3. **Trang 3 — Kiểm tra lỗi trùng BCL:** Thay đổi 1 thông số → Tính lại → BCL trong danh sách vẫn chỉ có 1 (không nhân đôi)
4. **Trang 4 — Kết quả:** Xác nhận 4 biểu đồ (radar, gauge, bar, heatmap) hiển thị
5. **Trang 6 — Xuất báo cáo:** Tải Excel → kiểm tra 3 sheet. Tải Word → kiểm tra nội dung

---

## 5. Tùy chọn sau deploy (ưu tiên thấp)

### Thêm logo ứng dụng

Đặt file ảnh tại `assets/logo.png` (nền trắng hoặc trong suốt, ~200×200px).
`utils/sidebar.py` đã có code hiển thị, sẽ tự nhận ngay sau khi có file.
Sau đó commit và push (Streamlit Cloud tự cập nhật khi repo thay đổi).

### Điều chỉnh điểm mẫu PL2.4

Hiện tại: điểm mẫu cho CRI = 0,6647; PL2.4 gốc: CRI = 0,662.
Chênh lệch nhỏ, vẫn đúng Cấp 3 → GP 2.2. Khi có bảng điểm gốc, cập nhật `data/sample_data.json`.

---

## 6. Chi tiết kỹ thuật quan trọng

### Công thức tính CRI

```
H = Σ(wi·Hi)   trọng số H: [0.35, 0.32, 0.15, 0.18]  → tổng = 1.00
P = Σ(wi·Pi)   trọng số P raw: [0.15, 0.12, 0.22, 0.17, 0.23, 0.12] → tổng = 1.01
               → normalize: chia mỗi wi cho 1.01 trước khi tính
R = Σ(wi·Ri)   trọng số R: [0.39, 0.24, 0.20, 0.17]  → tổng = 1.00

CRI = H^0.28 × P^0.40 × R^0.32
```

### Ngưỡng phân loại CRI → Giải pháp

| CRI | Cấp | Màu | Giải pháp (BCL-KHVS) |
|-----|-----|-----|-----------------------|
| < 0,36 | Cấp 1 — Thấp | `#2ecc71` (xanh) | GP 1 — Phủ xanh đơn giản |
| 0,36 – 0,53 | Cấp 2 — Trung bình | `#f39c12` (vàng) | GP 2.1 — Đóng bãi cơ bản |
| 0,53 – 0,69 | Cấp 3 — Cao | `#e67e22` (cam) | GP 2.2 — Đóng bãi tăng cường |
| ≥ 0,69 | Cấp 4 — Rất cao | `#e74c3c` (đỏ) | GP 3 — Can thiệp nâng cao |

BCL-HVS: đạt chuẩn QCVN 96:2025 → GP 2.1; cần bổ sung → GP 2.2 (không tính CRI).

### Cấu trúc session state

```python
st.session_state["bcl_list"] = [
    {
        "id": "ABCD1234",        # 8 ký tự hex tự sinh
        "info": {...},           # Trang 2 — thông tin định danh
        "scores": {...},         # Trang 3 — 14 điểm thông số
        "missing_notes": {...},  # Trang 3 — lý do thiếu dữ liệu
        "result": {
            "H": float, "P": float, "R": float, "CRI": float,
            "risk": {"level": 1-4, "label": str, "color": hex_str},
            "solution": dict,    # keys: id, name, short_name, mandatory_items, ...
        },
        "created_at": "ISO datetime",
    }
]

# Dữ liệu tạm giữa các trang:
"_bcl_saved_info"         = dict   # Thông tin BCL từ Trang 2 → Trang 3
"_bcl_active_editing_id"  = str    # ID BCL đang nhập CRI (update thay vì add lại)
"_cri_scores_draft"       = dict   # Draft điểm Trang 3
"_cri_notes_draft"        = dict   # Draft lý do thiếu
```

**Lưu ý quan trọng về lỗi trùng BCL (đã sửa Sprint 4):**
Sau `add_bcl()` trong `pages/3_Nhập_CRI.py` (dòng ~257–267), bắt buộc phải gán:
```python
st.session_state["_bcl_active_editing_id"] = bcl_id
```
để các lần "Tính CRI" tiếp theo gọi `update_bcl()` thay vì `add_bcl()`.

### API các module chính

```python
# core/calculator.py
calculate_cri(scores: dict) -> {"H": float, "P": float, "R": float, "CRI": float}

# core/classifier.py
classify_and_recommend(cri: float | None, bcl_type: str, hvs_status: str = None)
    -> {"risk": {"level", "label", "color", "cri"}, "solution": dict, "classification_key": str}
get_top_risk_params(scores: dict, n: int = 3) -> list[dict]

# utils/session.py
add_bcl(info, scores, missing_notes, result) -> str   # trả về bcl_id
update_bcl(bcl_id, **kwargs) -> None
get_active_bcl() -> dict | None
get_all_bcl() -> list[dict]

# export/excel_export.py
export_to_excel(entries: list[dict]) -> BytesIO   # 3 sheets

# export/word_export.py
export_to_word(entry: dict, include_solution=True, include_legal=True) -> BytesIO
```

---

## 7. Vấn đề chưa giải quyết

| Vấn đề | Mức độ | Ghi chú |
|--------|--------|---------|
| Commit 2 file chưa vào git | **Cao** | `.gitignore`, `HANDOFF.md` — làm trước khi push |
| Deploy GitHub + Streamlit Cloud | **Cao** | Xem chi tiết Bước 1-2 ở trên |
| Test thủ công trình duyệt sau deploy | Trung bình | Xem Bước 3 ở trên |
| Điểm mẫu PL2.4 chênh lệch nhỏ | Thấp | CRI = 0,6647 vs 0,662 — đúng cấp rủi ro |
| Logo ứng dụng | Thấp | Đặt `assets/logo.png` là xong |
| PDF export | Thấp | Chưa implement — người dùng xuất từ Word |

---

## 8. Lưu ý vận hành

- **Windows `WinError 10054`** trong `streamlit_log.txt`: Noise bình thường trên Windows (ProactorEventLoop), không xuất hiện trên Linux/Streamlit Cloud, không ảnh hưởng chức năng.
- **Session state mất khi refresh:** Hành vi mặc định của Streamlit. Người dùng cần xuất Excel/Word trước khi đóng trình duyệt.
- **Tên file tiếng Việt trên GitHub/Linux:** `.gitattributes` đã xử lý (LF line endings), hoạt động bình thường.
- **Streamlit Cloud tự cập nhật:** Mỗi khi push commit mới lên GitHub, Streamlit Cloud sẽ tự rebuild và deploy.
- **bcl_cri_demo.html:** File demo cục bộ, không ảnh hưởng đến Streamlit app, không có trong git.

---

*HANDOFF.md — BCL-CRI Tool v1.0*
*Cập nhật: 2026-06-07 — Sau Sprint 5 (HTML demo) | Phiên kế tiếp: Deploy GitHub + Streamlit Cloud*
