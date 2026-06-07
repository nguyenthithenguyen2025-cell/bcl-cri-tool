# -*- coding: utf-8 -*-
"""Trang 1 — Giới thiệu và hướng dẫn sử dụng."""

import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Giới thiệu — BCL-CRI Tool", layout="wide")
render_sidebar()

st.title("📖 Giới thiệu công cụ")

# ── Mục đích
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

> Phương pháp CRI được xây dựng theo mô hình nguồn — đường — đối tượng (Source–Pathway–Receptor)
> và được kiểm chứng trên dữ liệu BCL tại Việt Nam.
""")

st.divider()

# ── Sơ đồ quy trình
st.markdown("## Quy trình sử dụng công cụ")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("""
    **Bước 1**

    📋 Khai báo thông tin BCL
    - Tên, vị trí
    - Diện tích
    - Loại BCL
    """)
with col2:
    st.markdown("""
    **Bước 2**

    📝 Nhập 14 thông số CRI
    - Nhóm H (nguồn)
    - Nhóm P (đường)
    - Nhóm R (đối tượng)
    """)
with col3:
    st.markdown("""
    **Bước 3**

    🔢 Tính toán tự động
    - H, P, R từng nhóm
    - CRI tổng hợp
    - Phân loại cấp rủi ro
    """)
with col4:
    st.markdown("""
    **Bước 4**

    📊 Xem kết quả
    - Biểu đồ trực quan
    - Giải pháp khuyến nghị
    - Phân tích thông số
    """)
with col5:
    st.markdown("""
    **Bước 5**

    📄 Xuất báo cáo
    - Word/PDF (hồ sơ)
    - Excel (số liệu)
    - So sánh nhiều BCL
    """)

st.divider()

# ── Phương pháp CRI
with st.expander("📐 Phương pháp tính CRI — chi tiết", expanded=False):
    st.markdown("""
    ### Công thức tính CRI

    **Bước 1 — Tính chỉ số từng nhóm (trung bình cộng có trọng số):**
    """)
    st.latex(r"H = \sum_{i=1}^{4} w_{Hi} \cdot H_i")
    st.latex(r"P = \sum_{j=1}^{6} w_{Pj} \cdot P_j")
    st.latex(r"R = \sum_{k=1}^{4} w_{Rk} \cdot R_k")
    st.markdown("**Bước 2 — Tính CRI (trung bình nhân có trọng số):**")
    st.latex(r"CRI = H^{0{,}28} \times P^{0{,}40} \times R^{0{,}32}")

    st.markdown("""
    ### Thang điểm từng thông số

    Mỗi thông số được quy đổi thành điểm theo 4 mức:

    | Điểm | Mức độ rủi ro |
    |------|---------------|
    | 0,25 | Thấp |
    | 0,50 | Trung bình |
    | 0,75 | Cao |
    | 1,00 | Rất cao |

    ### Phân loại cấp rủi ro

    | Giá trị CRI | Cấp | Mức độ | Màu |
    |-------------|-----|--------|-----|
    | < 0,36 | Cấp 1 | Rủi ro thấp | 🟢 |
    | 0,36 – < 0,53 | Cấp 2 | Rủi ro trung bình | 🟡 |
    | 0,53 – < 0,69 | Cấp 3 | Rủi ro cao | 🟠 |
    | 0,69 – 1,00 | Cấp 4 | Rủi ro rất cao | 🔴 |
    """)

# ── Lưu ý
st.markdown("""
## Lưu ý khi sử dụng

1. **Phạm vi áp dụng:** Công cụ được thiết kế cho BCL-KHVS. BCL hợp vệ sinh (BCL-HVS)
   không cần tính CRI — chỉ cần kiểm tra tiêu chí đạt chuẩn QCVN 96:2025.

2. **Thiếu dữ liệu:** Nếu một thông số chưa có dữ liệu, hệ thống sẽ tự động gán điểm 1,00
   (rủi ro tối đa — nguyên tắc thận trọng). Người dùng cần ghi rõ lý do.

3. **Độ chính xác:** Kết quả CRI phụ thuộc vào chất lượng dữ liệu đầu vào.
   Khuyến khích khảo sát thực địa đầy đủ trước khi đánh giá.

4. **Dữ liệu phiên:** Dữ liệu BCL chỉ được lưu trong phiên làm việc hiện tại.
   Hãy xuất Excel/Word để lưu kết quả trước khi đóng trình duyệt.

5. **Tư vấn chuyên môn:** Kết quả của công cụ là hỗ trợ quyết định — không thay thế
   đánh giá kỹ thuật của đơn vị tư vấn chuyên ngành.
""")

st.divider()
st.caption(
    "Nguồn: Đề tài TNMT.2024.05.05, Trường Đại học Thủy Lợi (2026). "
    "Căn cứ pháp lý: Điều 32, TT 02/2022/TT-BTNMT; QCVN 96:2025/BNNMT."
)
