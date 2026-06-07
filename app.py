# -*- coding: utf-8 -*-
"""
BCL-CRI Decision Support Tool — Entry point.
Chạy: streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Công cụ CRI — Đóng bãi chôn lấp CTRSH",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": (
            "**Công cụ Hỗ trợ Quyết định Đóng bãi Chôn lấp CTRSH**\n\n"
            "Phiên bản 1.0 — Đề tài TNMT.2024.05.05\n"
            "Trường Đại học Thủy Lợi, 2026\n\n"
            "Căn cứ: TT 02/2022/TT-BTNMT | QCVN 96:2025/BNNMT | TCVN 13766:2023"
        ),
    },
)

# ── CSS toàn cục
st.markdown("""
<style>
  /* Bảng xếp hạng và kết quả */
  .metric-card {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 16px 20px;
    border-left: 5px solid #1f77b4;
    margin-bottom: 12px;
  }
  .risk-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
  }
  /* Ẩn menu mặc định Streamlit */
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar — điều hướng và thông tin session
from utils.sidebar import render_sidebar
render_sidebar()

# ── Trang chủ (khi truy cập app.py trực tiếp)
st.title("♻️ Công cụ Hỗ trợ Quyết định Đóng bãi Chôn lấp CTRSH")
st.markdown(
    "> Tính toán Chỉ số Rủi ro Tổng hợp (CRI), phân loại mức độ và khuyến nghị "
    "giải pháp đóng bãi cho bãi chôn lấp không hợp vệ sinh (BCL-KHVS) tại Việt Nam."
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 📋 Bắt đầu")
    st.markdown(
        "1. **Giới thiệu** — Đọc hướng dẫn sử dụng\n"
        "2. **Khai báo BCL** — Nhập thông tin bãi\n"
        "3. **Nhập thông số CRI** — 14 thông số đánh giá"
    )
with col2:
    st.markdown("### 📊 Xem kết quả")
    st.markdown(
        "4. **Kết quả & Phân tích** — CRI, biểu đồ, giải pháp\n"
        "5. **So sánh BCL** — Bảng xếp hạng nhiều bãi"
    )
with col3:
    st.markdown("### 📄 Xuất báo cáo")
    st.markdown(
        "6. **Xuất báo cáo** — Word, PDF, Excel\n\n"
        "Sử dụng menu **Pages** ở thanh bên trái để điều hướng."
    )

st.divider()
st.info(
    "💡 **Hướng dẫn nhanh:** Chọn trang **Khai báo BCL** ở sidebar bên trái để bắt đầu nhập dữ liệu. "
    "Có thể nhập nhiều BCL và so sánh trên cùng một bảng xếp hạng."
)
