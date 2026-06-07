# -*- coding: utf-8 -*-
"""
BCL-CRI Decision Support Tool — Entry point.
Chạy: streamlit run app.py
"""

import streamlit as st
from utils.ui import (
    APP_NAME,
    APP_VERSION,
    HOST_ORG,
    PROJECT_NAME,
    apply_global_styles,
    render_page_header,
    render_status_summary,
    render_workflow_overview,
)

st.set_page_config(
    page_title=APP_NAME,
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": (
            f"**{APP_NAME}**\n\n"
            f"Phiên bản {APP_VERSION} — {PROJECT_NAME}\n"
            f"{HOST_ORG}, 2026\n\n"
            "Căn cứ: TT 02/2022/TT-BTNMT | QCVN 96:2025/BNNMT | TCVN 13766:2023"
        ),
    },
)

apply_global_styles()

# ── Sidebar — điều hướng và thông tin session
from utils.sidebar import render_sidebar
render_sidebar()

# ── Trang chủ (khi truy cập app.py trực tiếp)
render_page_header(
    APP_NAME,
    "Ứng dụng hỗ trợ cơ quan quản lý, địa phương và đơn vị tư vấn đánh giá rủi ro "
    "bãi chôn lấp chất thải rắn sinh hoạt, phân loại mức độ ưu tiên và lựa chọn nhóm "
    "giải pháp đóng bãi phù hợp.",
    section="Tổng quan",
)

render_status_summary()

st.divider()
st.markdown("### Quy trình sử dụng")
render_workflow_overview()

st.divider()
st.info(
    "Bắt đầu tại trang **Khai báo BCL** trong thanh điều hướng bên trái. "
    "Công cụ cho phép nhập nhiều bãi chôn lấp, so sánh mức độ rủi ro và xuất hồ sơ kỹ thuật."
)
