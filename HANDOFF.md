# HANDOFF NOTE — BCL-CRI Decision Support Tool

**Ngày cập nhật:** 2026-06-07 (Phiên 6 — ĐÃ COMMIT)
**Dự án:** Công cụ Hỗ trợ Quyết định Đóng bãi Chôn lấp CTRSH
**Thư mục dự án:** `D:\1. AI_landfill\landfill-cri-tool\`
**Git:** Branch `master` — Commit hiện tại: `2cf640d`
**GitHub:** https://github.com/nguyenthithenguyen2025-cell/bcl-cri-tool
**App URL:** https://bcl-cri-tool-f7bzdcw6lzg6yz92ouerqz.streamlit.app

---

## 1. Trạng thái dự án hiện tại

| Sprint / Phiên | Nội dung | Trạng thái |
|----------------|----------|-----------|
| Sprint 1 | Core logic (calculator, classifier, config) | ✅ HOÀN THÀNH |
| Sprint 2 | Giao diện 6 trang Streamlit | ✅ HOÀN THÀNH |
| Sprint 3 | Biểu đồ (6 loại) + Export Excel/Word | ✅ HOÀN THÀNH |
| Sprint 4 | Test + Sửa lỗi + Git commit | ✅ HOÀN THÀNH |
| Sprint 5 | HTML demo để kiểm tra trước | ✅ HOÀN THÀNH |
| Sprint 6 | Deploy GitHub + Streamlit Cloud | ✅ HOÀN THÀNH |
| Phiên 5 | Tinh chỉnh UI/UX theo phản hồi | ✅ HOÀN THÀNH |
| **Phiên 6** | **Cải thiện Trang 1, thêm HTML export, sửa lỗi Word** | ✅ HOÀN THÀNH — commit `2cf640d` |

**Git working tree hiện tại:** Sạch — tất cả thay đổi đã được commit và push.

---

## 2. Lịch sử thay đổi theo phiên

### Phiên 6 — 2026-06-07 (MỚI NHẤT — CHƯA COMMIT)

#### 2.1 Sửa lỗi — `export/word_export.py`

**Vấn đề:** Trường "Huyện/Quận" đã bị xóa khỏi form Trang 2 (Phiên 5) nhưng vẫn còn trong bảng xuất Word, gây ra dòng "—" thừa.

**Thay đổi:** Xóa dòng `("Huyện/Quận", info.get("huyen"))` khỏi danh sách `fields` trong hàm `export_to_word()`.

#### 2.2 Cải thiện Trang 1 — `pages/1_Giới_thiệu.py`

Viết lại toàn bộ trang, gồm:

| Phần | Thay đổi |
|------|---------|
| Callout nhanh | Thêm `st.info()` hướng dẫn bắt đầu ngay |
| Layout 2 cột | Mô tả mục đích (trái) + bảng phạm vi áp dụng (phải) |
| Cards 5 bước | Styled HTML cards với viền xanh, nền nhạt, icon lớn — thay thế 5 cột markdown thô |
| Expander CRI | Thêm tabs 3 nhóm (H / P / R) với bảng 14 thông số đầy đủ ngưỡng điểm |
| Lưu ý | Chia 2 cột: Về dữ liệu đầu vào / Về lưu trữ và xuất kết quả |

#### 2.3 Thêm HTML export — `export/html_export.py` (file mới)

**Chức năng:** Tạo báo cáo kỹ thuật dạng HTML hoàn chỉnh, hỗ trợ đầy đủ tiếng Việt, in thành PDF qua trình duyệt.

**Không cần dependency mới** — dùng thư viện chuẩn Python, không thêm vào `requirements.txt`.

**Nội dung báo cáo HTML:**
1. Thông tin bãi chôn lấp (bảng)
2. Kết quả CRI: badge màu theo cấp, bảng H/P/R, bảng 14 thông số
3. Giải pháp khuyến nghị (nếu bật)
4. Căn cứ pháp lý (nếu bật)
5. Nút "🖨️ In / Lưu PDF" cố định góc phải (ẩn khi in)
6. CSS print-ready: layout A4, font Times New Roman

**Cách dùng:** Người dùng tải file `.html` → mở bằng Chrome/Edge → Ctrl+P → Destination: "Save as PDF" → Print.

#### 2.4 Cập nhật Trang 6 — `pages/6_Xuất_báo_cáo.py`

Thêm Section 5 "Xuất HTML → In thành PDF" với nút tải xuống + hướng dẫn in PDF.
Cập nhật phần "Lưu ý" để mô tả cách in PDF từ HTML.

---

### Phiên 5 — 2026-06-07

**Commit:** `54b7f05` — UX: show content on all pages even when no BCL data exists

#### Sửa giao diện `pages/2_Khai_báo_BCL.py`

| Thay đổi | Chi tiết |
|----------|---------|
| Đổi tiêu đề mục 1 | "Thông tin định danh" → **"Thông tin chung về bãi chôn lấp"** |
| Xóa trường Huyện/Quận/Thị xã | Bỏ `huyen` khỏi form và khỏi dict lưu kết quả |
| Sửa nhãn trường Xã | "Xã / Phường / Thị trấn" → **"Xã / Phường"** |

#### Cải thiện UX khi chưa có dữ liệu — 4 trang

| Trang | Thay đổi |
|-------|---------|
| **Trang 3 — Nhập CRI** | Bỏ `st.stop()` — hiện form đầy đủ ngay cả khi chưa khai báo BCL |
| **Trang 4 — Kết quả** | Thêm mô tả nội dung sẽ xuất hiện |
| **Trang 5 — So sánh** | Thêm mô tả nội dung sẽ xuất hiện |
| **Trang 6 — Xuất báo cáo** | Thêm mô tả 3 định dạng xuất |

---

### Phiên 4 — 2026-06-07

- Tạo GitHub repo public: `nguyenthithenguyen2025-cell/bcl-cri-tool`
- Push toàn bộ code lên GitHub
- Deploy lên Streamlit Community Cloud
- URL app: https://bcl-cri-tool-f7bzdcw6lzg6yz92ouerqz.streamlit.app

---

## 3. Commit Phiên 6 — ĐÃ PUSH

```
Commit: 2cf640d
Branch: master → origin/master (đã push)
Files: 5 files changed, 574 insertions(+), 153 deletions(-)

  modified:   HANDOFF.md
  new file:   export/html_export.py
  modified:   export/word_export.py
  modified:   pages/1_Giới_thiệu.py
  modified:   pages/6_Xuất_báo_cáo.py
```

---

## 4. Tất cả file dự án (32 files — sau phiên 6)

```
landfill-cri-tool/
├── app.py                          ✅ Entry point Streamlit
├── requirements.txt                ✅ streamlit, plotly, pandas, openpyxl, python-docx
├── .streamlit/config.toml          ✅ Theme xanh dương, layout wide
├── .gitattributes                  ✅ UTF-8/LF cho file tiếng Việt
├── .gitignore                      ✅
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
│   ├── 1_Giới_thiệu.py             ✅ Trang giới thiệu — viết lại Phiên 6
│   ├── 2_Khai_báo_BCL.py           ✅ Form nhập thông tin BCL
│   ├── 3_Nhập_CRI.py               ✅ Form 14 thông số CRI
│   ├── 4_Kết_quả.py                ✅ Dashboard + 4 biểu đồ + giải pháp
│   ├── 5_So_sánh_BCL.py            ✅ Bảng xếp hạng + biểu đồ so sánh nhiều BCL
│   └── 6_Xuất_báo_cáo.py           ✅ Xuất Excel + Word + HTML/PDF — cập nhật Phiên 6
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
│   ├── excel_export.py             ✅ export_to_excel() → BytesIO
│   ├── word_export.py              ✅ export_to_word() → BytesIO — sửa lỗi Phiên 6
│   └── html_export.py              ✅ export_to_html() → bytes — MỚI Phiên 6
│
├── data/
│   └── sample_data.json            ✅ Dữ liệu mẫu PL2.4
│
├── assets/                         ⏳ Thư mục rỗng (logo.png chưa có)
│
├── PROJECT_BRIEF.md                ✅
├── DEVELOPMENT_PLAN.md             ✅
├── README.md                       ✅
└── HANDOFF.md                      ✅ File này (cập nhật Phiên 6)
```

---

## 5. Việc còn lại & bước tiếp theo

### 5.1 Việc CẦN làm ngay

| Bước | Hành động | Trạng thái |
|------|-----------|------------|
| 1 | **Commit + Push** toàn bộ thay đổi Phiên 6 | ✅ Hoàn thành — commit `2cf640d` |
| 2 | **Kiểm tra app** trên Streamlit Cloud (~1-2 phút sau push) | ⏳ Chờ rebuild — mở https://bcl-cri-tool-f7bzdcw6lzg6yz92ouerqz.streamlit.app |
| 3 | **Test HTML export**: nhập 1 BCL mẫu → Trang 6 → Tạo file HTML → mở bằng Chrome → Ctrl+P → Save as PDF | ⏳ Cần test thủ công |

### 5.2 Việc còn lại (ưu tiên thấp — chưa làm)

| # | Vấn đề / Tính năng | Mức ưu tiên | Ghi chú |
|---|---------------------|-------------|---------|
| 1 | **Logo ứng dụng** | Thấp | Đặt file tại `assets/logo.png` (~200×200px) → `utils/sidebar.py` tự nhận |
| 2 | **Điểm mẫu PL2.4 chênh lệch nhỏ** | Thấp | CRI = 0,6647 vs 0,662 gốc — đúng cấp, đúng giải pháp. Cập nhật `data/sample_data.json` khi có bảng điểm gốc chính xác |
| 3 | **Bản đồ phân bố BCL (Trang 5)** | Thấp — v1.1 | Cần Mapbox token hoặc OpenStreetMap; tọa độ GPS tùy chọn |
| 4 | **Lưu dữ liệu SQLite** | Thấp — v1.2 | Session state mất khi đóng tab; giải pháp tạm: xuất Excel/HTML ngay sau nhập |
| 5 | **Phân quyền người dùng** | Thấp — v2.0 | Dùng `st-authenticator` nếu cần |

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
            "solution": dict,
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

**Lưu ý quan trọng — tránh trùng BCL:**
Sau `add_bcl()` trong `pages/3_Nhập_CRI.py`, bắt buộc gán:
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

# export/html_export.py  ← MỚI (Phiên 6)
export_to_html(entry: dict, include_solution=True, include_legal=True) -> bytes
```

---

## 7. Lưu ý vận hành

- **Session state mất khi refresh:** Hành vi mặc định của Streamlit. Người dùng cần xuất Excel/Word/HTML trước khi đóng trình duyệt.
- **Streamlit Cloud tự cập nhật:** Mỗi khi push commit mới lên GitHub, Streamlit Cloud tự rebuild (~1–2 phút).
- **Tên file tiếng Việt trên GitHub/Linux:** `.gitattributes` đã xử lý (LF line endings), hoạt động bình thường.
- **HTML export in PDF:** Yêu cầu Chrome hoặc Edge (không dùng IE/Firefox cũ). Chọn "Save as PDF" thay vì máy in vật lý để có bản PDF chất lượng cao.
- **`bcl_cri_demo.html`:** File demo cục bộ (không phải html_export.py), không track trong git, không ảnh hưởng đến app.

---

*HANDOFF.md — BCL-CRI Tool v1.0*
*Cập nhật: 2026-06-07 — Phiên 6 | Trạng thái: Đã commit và push — `2cf640d` | Working tree: sạch*
