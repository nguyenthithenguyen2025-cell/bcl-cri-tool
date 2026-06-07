# -*- coding: utf-8 -*-
"""Trang tổng quan công cụ."""

import streamlit as st

from utils.sidebar import render_sidebar
from utils.ui import (
    APP_NAME,
    apply_global_styles,
    render_branding_banner,
    render_page_footer,
    render_page_header,
    render_status_summary,
    render_workflow_overview,
)


apply_global_styles()
render_sidebar()
render_branding_banner()

render_page_header(
    APP_NAME,
    "Ứng dụng hỗ trợ cơ quan quản lý, địa phương và đơn vị tư vấn đánh giá rủi ro "
    "bãi chôn lấp chất thải rắn sinh hoạt, phân loại mức độ ưu tiên và lựa chọn nhóm "
    "giải pháp đóng bãi phù hợp.",
    section="Tổng quan công cụ",
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

render_page_footer()
