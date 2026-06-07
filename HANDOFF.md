# HANDOFF NOTE — BCL-CRI Decision Support Tool

**Ngày cập nhật:** 2026-06-07 (Phiên 5)
**Dự án:** Công cụ Hỗ trợ Quyết định Đóng bãi Chôn lấp CTRSH
**Thư mục dự án:** `D:\1. AI_landfill\landfill-cri-tool\`
**Git:** Branch `master` — Commit hiện tại: `54b7f05`
**GitHub:** https://github.com/nguyenthithenguyen2025-cell/bcl-cri-tool
**App URL:** https://bcl-cri-tool-f7bzdcw6lzg6yz92ouerqz.streamlit.app

---

## 1. Trạng thái dự án hiện tại

| Sprint | Nội dung | Trạng thái |
|--------|----------|-----------|
| Sprint 1 | Core logic (calculator, classifier, config) | ✅ HOÀN THÀNH |
| Sprint 2 | Giao diện 6 trang Streamlit | ✅ HOÀN THÀNH |
| Sprint 3 | Biểu đồ (6 loại) + Export Excel/Word | ✅ HOÀN THÀNH |
| Sprint 4 | Test + Sửa lỗi + Git commit | ✅ HOÀN THÀNH |
| Sprint 5 | HTML demo để kiểm tra trước | ✅ HOÀN THÀNH |
| Sprint 6 | Deploy GitHub + Streamlit Cloud | ✅ HOÀN THÀNH |
| Phiên 5 | Tinh chỉnh UI/UX theo phản hồi | ✅ HOÀN THÀNH |

**Git working tree hiện tại:** Sạch — tất cả file đã commit và push.

---

## 2. Lịch sử thay đổi theo phiên

### Phiên 5 — 2026-06-07 (mới nhất)

**Commit:** `54b7f05` — UX: show content on all pages even when no BCL data exists

#### 2.1 Sửa giao diện `pages/2_Khai_báo_BCL.py`

| Thay đổi | Chi tiết |
|----------|---------|
| Đổi tiêu đề mục 1 | "Thông tin định danh" → **"Thông tin chung về bãi chôn lấp"** |
| Xóa trường Huyện/Quận/Thị xã | Bỏ `huyen` khỏi form và khỏi dict lưu kết quả |
| Sửa nhãn trường Xã | "Xã / Phường / Thị trấn" → **"Xã / Phường"** |

#### 2.2 Cải thiện UX khi chưa có dữ liệu — 4 trang

**Vấn đề cũ:** Trang 3, 4, 5, 6 hoàn toàn trắng trơn nếu người dùng chưa khai báo BCL, gây bất tiện và khó hiểu.

**Giải pháp đã áp dụng:**

| Trang | Thay đổi |
|-------|---------|
| **Trang 3 — Nhập CRI** | Bỏ `st.stop()` — hiện đầy đủ form 14 thông số ngay cả khi chưa khai báo BCL; thay cảnh báo cứng bằng thông báo nhẹ (info) |
| **Trang 4 — Kết quả** | Giữ `st.stop()` nhưng thêm mô tả các nội dung sẽ xuất hiện (thẻ CRI, 4 biểu đồ, phân tích, giải pháp) |
| **Trang 5 — So sánh** | Giữ `st.stop()` nhưng thêm mô tả (bảng xếp hạng, bộ lọc, 2 biểu đồ, xuất Excel) |
| **Trang 6 — Xuất báo cáo** | Giữ `st.stop()` nhưng thêm mô tả 3 định dạng xuất (Excel, Word, PDF) |

---

### Phiên 4 — 2026-06-07

- Commit 2 file tồn đọng (`.gitignore`, `HANDOFF.md`)
- Tạo GitHub repo public: `nguyenthithenguyen2025-cell/bcl-cri-tool`
- Push toàn bộ code lên GitHub qua `gh repo create`
- Deploy lên Streamlit Community Cloud (thao tác web thủ công)
- Test thủ công 5 bước — không có lỗi
- URL app: https://bcl-cri-tool-f7bzdcw6lzg6yz92ouerqz.streamlit.app

### Phiên 3 — 2026-06-07

- Tạo file HTML demo `bcl_cri_demo.html` (không track trong git)
- Cập nhật `.gitignore`

### Phiên 1–2 — 2026-06-07

- Xây dựng toàn bộ app Streamlit (Sprint 1–4): 31 files
- Core logic, giao diện 6 trang, 6 biểu đồ, xuất Excel/Word

---

## 3. Tất cả file dự án (31 files trong git)

```
landfill-cri-tool/
├── app.py                          ✅ Entry point Streamlit
├── requirements.txt                ✅ streamlit, plotly, pandas, openpyxl, python-docx
├── .streamlit/config.toml          ✅ Theme xanh dương, layout wide
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
│   ├── 2_Khai_báo_BCL.py           ✅ Form nhập thông tin BCL — đã tinh chỉnh Phiên 5
│   ├── 3_Nhập_CRI.py               ✅ Form 14 thông số CRI — hiện cả khi chưa có BCL info
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
│   ├── excel_export.py             ✅ export_to_excel() → BytesIO
│   └── word_export.py              ✅ export_to_word() → BytesIO
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

## 4. Vấn đề còn tồn đọng & việc cần làm tiếp

| # | Vấn đề / Tính năng | Mức ưu tiên | Ghi chú |
|---|---------------------|-------------|---------|
| 1 | **Logo ứng dụng** | Thấp | Đặt file tại `assets/logo.png` (~200×200px, nền trắng/trong suốt) → `utils/sidebar.py` tự nhận |
| 2 | **Điểm mẫu PL2.4 chênh lệch nhỏ** | Thấp | CRI = 0,6647 vs 0,662 gốc — đúng cấp, đúng giải pháp. Cập nhật `data/sample_data.json` khi có bảng điểm gốc chính xác |
| 3 | **PDF export** | Thấp | Chưa implement — hiện người dùng xuất từ Word (File → Print → Save as PDF) |
| 4 | **Nội dung Trang 1 — Giới thiệu** | Trung bình | Có thể bổ sung sơ đồ quy trình, mô tả phương pháp CRI chi tiết hơn |
| 5 | **Tinh chỉnh nội dung form Trang 2** | Đang làm | Người dùng đang chỉnh từng trường theo yêu cầu thực tế |
| 6 | **Bản đồ phân bố BCL (Trang 5)** | Thấp — v1.1 | Cần Mapbox token hoặc OpenStreetMap; tọa độ GPS tùy chọn |
| 7 | **Lưu dữ liệu SQLite** | Thấp — v1.2 | Session state mất khi đóng tab; giải pháp tạm: xuất Excel ngay sau nhập |
| 8 | **Phân quyền người dùng** | Thấp — v2.0 | Dùng `st-authenticator` nếu cần |

---

## 5. Chi tiết kỹ thuật quan trọng

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
```

---

## 6. Lưu ý vận hành

- **Session state mất khi refresh:** Hành vi mặc định của Streamlit. Người dùng cần xuất Excel/Word trước khi đóng trình duyệt.
- **Streamlit Cloud tự cập nhật:** Mỗi khi push commit mới lên GitHub, Streamlit Cloud tự rebuild (~1–2 phút).
- **Tên file tiếng Việt trên GitHub/Linux:** `.gitattributes` đã xử lý (LF line endings), hoạt động bình thường.
- **Windows `WinError 10054`** trong `streamlit_log.txt`: Noise bình thường khi chạy local trên Windows, không xuất hiện trên Streamlit Cloud.
- **`bcl_cri_demo.html`:** File demo cục bộ, không track trong git, không ảnh hưởng đến app.

---

*HANDOFF.md — BCL-CRI Tool v1.0*  
*Cập nhật: 2026-06-07 — Phiên 5 | Trạng thái: App đã deploy, đang tinh chỉnh UI theo yêu cầu*
