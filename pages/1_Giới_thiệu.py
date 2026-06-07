# -*- coding: utf-8 -*-
"""Trang 1 — Giới thiệu và hướng dẫn sử dụng."""

import streamlit as st
from utils.sidebar import render_sidebar
from utils.ui import APP_NAME, apply_global_styles, render_page_footer, render_page_header, render_workflow_overview

apply_global_styles()
render_sidebar()

render_page_header(
    "Giới thiệu công cụ",
    f"{APP_NAME} được xây dựng để hỗ trợ đánh giá rủi ro, phân loại mức độ ưu tiên "
    "và lựa chọn nhóm giải pháp đóng bãi phù hợp cho bãi chôn lấp chất thải rắn sinh hoạt.",
    section="Tổng quan và hướng dẫn sử dụng",
)

# ── Callout nhanh
st.info(
    "**Để bắt đầu đánh giá:** Chọn trang **Khai báo BCL** trên thanh bên trái → "
    "Nhập thông tin bãi chôn lấp → Nhập 14 thông số CRI → Xem kết quả."
)

st.divider()

# ── Mục đích
col_desc, col_scope = st.columns([3, 2])
with col_desc:
    st.markdown("""
## Mục đích

Công cụ này hỗ trợ các cơ quan quản lý, đơn vị tư vấn và chủ đầu tư:

- **Đánh giá mức độ rủi ro** của bãi chôn lấp không hợp vệ sinh (BCL-KHVS) thông qua
  Chỉ số Rủi ro Tổng hợp (CRI — Contamination Risk Index)
- **Phân loại mức độ đóng bãi** theo 4 cấp rủi ro (thấp / trung bình / cao / rất cao)
- **Khuyến nghị giải pháp** đóng bãi phù hợp (GP 1, GP 2.1, GP 2.2, GP 3)
- **So sánh nhiều BCL** trên cùng một bảng xếp hạng để ưu tiên can thiệp
- **Xuất báo cáo kỹ thuật** dạng Word, PDF và Excel
""")
with col_scope:
    st.markdown("""
## Phạm vi áp dụng

| Đối tượng | Áp dụng |
|-----------|---------|
| BCL không hợp vệ sinh | ✅ Tính CRI đầy đủ |
| BCL hợp vệ sinh đạt chuẩn | ✅ Giải pháp trực tiếp |
| BCL hợp vệ sinh cần bổ sung | ✅ Giải pháp tăng cường |
| Bãi thải công nghiệp | ❌ Ngoài phạm vi |
| Bãi chứa CTNH | ❌ Ngoài phạm vi |

> Phương pháp CRI được xây dựng theo mô hình **nguồn — đường — đối tượng** (Source–Pathway–Receptor).
""")

st.divider()

# ── Quy trình sử dụng
st.markdown("## Quy trình sử dụng công cụ")
render_workflow_overview()

st.divider()

# ── Căn cứ pháp lý
st.markdown("""
## Căn cứ pháp lý và kỹ thuật

| Văn bản | Nội dung áp dụng |
|---------|-----------------|
| **Điều 32, TT 02/2022/TT-BTNMT** | Yêu cầu kỹ thuật đóng bãi CTRSH sau khi kết thúc hoạt động |
| **QCVN 96:2025/BNNMT** | Quy chuẩn kỹ thuật quốc gia về bãi chôn lấp chất thải rắn |
| **TCVN 13766:2023** | Yêu cầu thiết kế bãi chôn lấp hợp vệ sinh |
| **Đề tài TNMT.2024.05.05** | Phương pháp CRI, phân loại mức độ và khuyến nghị giải pháp |
""")

st.divider()

# ── Phương pháp CRI — chi tiết
with st.expander("📐 Phương pháp tính CRI — công thức và 14 thông số", expanded=False):
    st.markdown("### Công thức tính CRI")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("**Bước 1 — Chỉ số từng nhóm (trung bình cộng có trọng số):**")
        st.latex(r"H = \sum_{i=1}^{4} w_{Hi} \cdot H_i \quad (\text{4 thông số})")
        st.latex(r"P = \sum_{j=1}^{6} w_{Pj} \cdot P_j \quad (\text{6 thông số})")
        st.latex(r"R = \sum_{k=1}^{4} w_{Rk} \cdot R_k \quad (\text{4 thông số})")
    with col_f2:
        st.markdown("**Bước 2 — CRI tổng hợp (trung bình nhân có trọng số nhóm):**")
        st.latex(r"CRI = H^{0{,}28} \times P^{0{,}40} \times R^{0{,}32}")
        st.markdown("""
**Trọng số nhóm:** H = 0,28 · P = 0,40 · R = 0,32 *(tổng = 1,00)*

**Phạm vi CRI:** [0,25 ; 1,00] — điểm 0,25 là mức thấp nhất, 1,00 là cao nhất.

**Thang điểm:** mỗi thông số quy đổi thành 0,25 / 0,50 / 0,75 / 1,00
theo ngưỡng mô tả hoặc giá trị số thực.
""")

    st.markdown("### Phân loại cấp rủi ro")
    st.markdown("""
| Giá trị CRI | Cấp | Mức độ rủi ro | Giải pháp (BCL-KHVS) | Màu |
|-------------|-----|----------------|----------------------|-----|
| < 0,36 | Cấp 1 | Rủi ro thấp | GP 1 — Phủ xanh đơn giản | 🟢 |
| 0,36 – < 0,53 | Cấp 2 | Rủi ro trung bình | GP 2.1 — Đóng bãi cơ bản | 🟡 |
| 0,53 – < 0,69 | Cấp 3 | Rủi ro cao | GP 2.2 — Đóng bãi tăng cường | 🟠 |
| 0,69 – 1,00 | Cấp 4 | Rủi ro rất cao | GP 3 — Can thiệp nâng cao | 🔴 |
""")

    st.markdown("### 14 thông số CRI")

    tab_h, tab_p, tab_r = st.tabs(["Nhóm H — Nguồn nguy hại (trọng số 0,28)", "Nhóm P — Đường lan truyền (trọng số 0,40)", "Nhóm R — Đối tượng tiếp nhận (trọng số 0,32)"])

    with tab_h:
        st.markdown("""
| Mã | Thông số | Trọng số | Thang điểm (điểm → ngưỡng) |
|----|----------|----------|----------------------------|
| **H1** | Thời gian ngừng tiếp nhận chất thải (năm) | 0,35 | 0,25 → >20 năm · 0,50 → 10–20 năm · 0,75 → 5–10 năm · 1,00 → <5 năm |
| **H2** | Diện tích bãi chôn lấp (ha) | 0,32 | 0,25 → <1 ha · 0,50 → 1–3 ha · 0,75 → 3–5 ha · 1,00 → >5 ha |
| **H3** | Thành phần chất thải nguy hại (%) | 0,15 | 0,25 → <1% · 0,50 → 1–2% · 0,75 → 2–5% · 1,00 → >5% |
| **H4** | Lượng nước rỉ rác quan sát được | 0,18 | 0,25 → Không có · 0,50 → Ít, cục bộ · 0,75 → Nhiều, lan rộng · 1,00 → Tràn ra ngoài |

*Tổng trọng số H = 1,00*
""")
    with tab_p:
        st.markdown("""
| Mã | Thông số | Trọng số | Thang điểm (điểm → ngưỡng) |
|----|----------|----------|----------------------------|
| **P1** | Tình trạng lớp phủ bề mặt | 0,15 | 0,25 → Kín tốt · 0,50 → Cơ bản · 0,75 → Kém · 1,00 → Không có |
| **P2** | Lượng mưa trung bình năm (mm/năm) | 0,12 | 0,25 → <1.000 · 0,50 → 1.000–1.400 · 0,75 → 1.400–2.400 · 1,00 → >2.400 |
| **P3** | Đặc điểm địa chất khu vực BCL | 0,22 | 0,25 → Sét dày (k<10⁻⁷) · 0,50 → Á sét · 0,75 → Cát/cuội sỏi · 1,00 → Đá vôi/karst |
| **P4** | Khoảng cách đến nguồn nước mặt (m) | 0,17 | 0,25 → >1.000 m · 0,50 → 500–1.000 m · 0,75 → 100–500 m · 1,00 → <100 m |
| **P5** | Khoảng cách đến mực nước ngầm (m) | 0,23 | 0,25 → >20 m · 0,50 → 15–20 m · 0,75 → 5–15 m · 1,00 → <5 m |
| **P6** | Độ dốc địa hình khu vực BCL (%) | 0,12 | 0,25 → <5% · 0,50 → 5–15% · 0,75 → 15–30% · 1,00 → >30% |

*Tổng trọng số P = 1,01 (làm tròn từ tài liệu gốc — hệ thống tự chuẩn hóa về 1,00)*
""")
    with tab_r:
        st.markdown("""
| Mã | Thông số | Trọng số | Thang điểm (điểm → ngưỡng) |
|----|----------|----------|----------------------------|
| **R1** | Mục đích sử dụng nguồn nước mặt và nước ngầm | 0,39 | 0,25 → Công nghiệp · 0,50 → Nông nghiệp/TS · 0,75 → Sinh hoạt (có xử lý) · 1,00 → Sinh hoạt trực tiếp |
| **R2** | Số người trong phạm vi 1.000 m (người) | 0,24 | 0,25 → <4 · 0,50 → 4–100 · 0,75 → 100–500 · 1,00 → >500 |
| **R3** | Tỷ lệ khiếu nại/phản ánh cộng đồng (%) | 0,20 | 0,25 → <5% · 0,50 → 5–15% · 0,75 → 15–30% · 1,00 → >30% |
| **R4** | Khoảng cách đến hệ sinh thái cần bảo vệ (m) | 0,17 | 0,25 → >1.000 m · 0,50 → 250–1.000 m · 0,75 → 50–250 m · 1,00 → <50 m |

*Tổng trọng số R = 1,00*
""")

# ── Lưu ý
st.markdown("## Lưu ý khi sử dụng")

col_note1, col_note2 = st.columns(2)
with col_note1:
    st.markdown("""
**Về dữ liệu đầu vào:**

1. **Phạm vi áp dụng:** Công cụ được thiết kế cho BCL-KHVS. BCL hợp vệ sinh (BCL-HVS) không cần tính CRI — chỉ cần kiểm tra tiêu chí đạt chuẩn QCVN 96:2025.

2. **Thiếu dữ liệu:** Nếu một thông số chưa có dữ liệu, hệ thống sẽ tự động gán điểm 1,00 (rủi ro tối đa — nguyên tắc thận trọng). Người dùng cần ghi rõ lý do.

3. **Độ chính xác:** Kết quả CRI phụ thuộc vào chất lượng dữ liệu đầu vào. Khuyến khích khảo sát thực địa đầy đủ trước khi đánh giá.
""")
with col_note2:
    st.markdown("""
**Về lưu trữ và xuất kết quả:**

4. **Dữ liệu phiên:** Dữ liệu BCL chỉ được lưu trong phiên làm việc hiện tại. Hãy xuất Excel/Word để lưu kết quả trước khi đóng trình duyệt.

5. **Xuất PDF:** Tải xuống file HTML từ trang Xuất báo cáo → mở bằng trình duyệt → Ctrl+P → Lưu dưới dạng PDF.

6. **Tư vấn chuyên môn:** Kết quả của công cụ là hỗ trợ quyết định — không thay thế đánh giá kỹ thuật của đơn vị tư vấn chuyên ngành.
""")

st.divider()
st.caption(
    "Nguồn: Đề tài TNMT.2024.05.05, Trường Đại học Thủy Lợi (2026). "
    "Căn cứ pháp lý: Điều 32, TT 02/2022/TT-BTNMT; QCVN 96:2025/BNNMT."
)

render_page_footer()
