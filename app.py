# -*- coding: utf-8 -*-
import streamlit as st
from utils.ui import APP_NAME, APP_VERSION, HOST_ORG, PROJECT_NAME, get_available_branding_logos, _img_to_base64

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

pages = [
    st.Page("pages/0_Tổng_quan_công_cụ.py", title="Tổng quan công cụ"),
    st.Page("pages/1_Giới_thiệu.py", title="Giới thiệu và hướng dẫn"),
    st.Page("pages/2_Khai_báo_BCL.py", title="Khai báo bãi chôn lấp"),
    st.Page("pages/3_Nhập_CRI.py", title="Đánh giá CRI"),
    st.Page(
        "pages/4_Kết_quả.py",
        title="Lựa chọn giải pháp can thiệp, đóng bãi",
    ),
    st.Page("pages/5_So_sánh_BCL.py", title="So sánh bãi chôn lấp"),
    st.Page("pages/6_Xuất_báo_cáo.py", title="Xuất hồ sơ và báo cáo"),
]

# Logo đặt trước st.navigation() để xuất hiện trên đầu sidebar, trước các link điều hướng
with st.sidebar:
    logos = get_available_branding_logos()
    if logos:
        mime, data = _img_to_base64(logos[0]["path"])
        st.markdown(
            f'<img src="data:{mime};base64,{data}" '
            'style="max-width:160px;margin:0.5rem 0 0.25rem 0;display:block;" alt="Logo"/>',
            unsafe_allow_html=True,
        )

current_page = st.navigation(pages)
current_page.run()
