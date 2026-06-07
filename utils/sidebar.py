# -*- coding: utf-8 -*-
"""
Sidebar dùng chung cho tất cả các trang.
Gọi render_sidebar() ở đầu mỗi page file để hiển thị danh sách BCL và thông tin pháp lý.
"""

import os
import streamlit as st
from utils.session import count_bcl, get_bcl_summary_list, clear_all_bcl


def render_sidebar():
    """Hiển thị sidebar thống nhất: danh sách BCL và căn cứ pháp lý."""
    with st.sidebar:
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path)
        st.title("BCL-CRI Tool")
        st.caption("Công cụ Hỗ trợ Quyết định Đóng bãi CTRSH")
        st.divider()

        n = count_bcl()
        if n == 0:
            st.info("Chưa có bãi chôn lấp nào được nhập.")
        else:
            st.success(f"**{n} BCL** đã nhập trong phiên này")
            for s in get_bcl_summary_list():
                cri_str = f"CRI = {s['CRI']:.3f}" if s["CRI"] else "BCL-HVS"
                st.caption(f"• {s['ten_bcl']} ({cri_str})")

        st.divider()
        st.caption("**Căn cứ pháp lý:**")
        st.caption("Điều 32, TT 02/2022/TT-BTNMT")
        st.caption("QCVN 96:2025/BNNMT")
        st.caption("TCVN 13766:2023")
        st.divider()
        st.caption("Đề tài TNMT.2024.05.05")
        st.caption("Trường ĐH Thủy Lợi, 2026")

        if n > 0:
            st.divider()
            if st.button("🗑️ Xóa tất cả BCL", type="secondary", use_container_width=True):
                clear_all_bcl()
                st.rerun()
