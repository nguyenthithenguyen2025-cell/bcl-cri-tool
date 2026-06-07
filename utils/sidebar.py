# -*- coding: utf-8 -*-
"""
Sidebar dùng chung cho tất cả các trang.
Gọi render_sidebar() ở đầu mỗi page file để hiển thị danh sách BCL và thông tin pháp lý.
"""

import os
import streamlit as st
from utils.session import count_bcl, get_bcl_summary_list, clear_all_bcl
from utils.ui import (
    APP_NAME,
    APP_SHORT_NAME,
    APP_VERSION,
    HOST_ORG,
    PROJECT_NAME,
    get_available_branding_logos,
    get_portfolio_status,
)


def render_sidebar():
    """Hiển thị sidebar thống nhất: danh sách BCL và căn cứ pháp lý."""
    with st.sidebar:
        logos = get_available_branding_logos()
        if logos:
            if len(logos) == 1:
                st.image(str(logos[0]["path"]), use_container_width=True)
            else:
                logo_cols = st.columns(len(logos))
                for col, logo in zip(logo_cols, logos):
                    with col:
                        st.image(str(logo["path"]), use_container_width=True)
        else:
            legacy_logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
            if os.path.exists(legacy_logo_path):
                st.image(legacy_logo_path)
        st.markdown(f"### {APP_SHORT_NAME}")
        st.caption(APP_NAME)
        st.caption(f"Phiên bản {APP_VERSION} | {PROJECT_NAME}")
        st.divider()

        n = count_bcl()
        status = get_portfolio_status()
        st.markdown("**Trạng thái hồ sơ**")
        st.caption(f"Tổng số BCL: **{status['total']}**")
        st.caption(f"BCL-KHVS đã tính CRI: **{status['khvs_done']}**")
        st.caption(f"BCL-KHVS chưa tính CRI: **{status['khvs_pending']}**")
        st.caption(f"BCL-HVS: **{status['hvs']}**")
        st.divider()

        st.markdown("**Danh sách BCL trong phiên**")
        if n == 0:
            st.info("Chưa có bãi chôn lấp nào được nhập.")
        else:
            for s in get_bcl_summary_list():
                cri_str = (
                    f"CRI = {s['CRI']:.3f}"
                    if s["CRI"] is not None
                    else s.get("status_label", "Chưa tính CRI")
                )
                st.caption(f"• {s['ten_bcl']} ({cri_str})")

        st.divider()
        st.markdown("**Quy trình nghiệp vụ**")
        st.caption("01. Khai báo BCL")
        st.caption("02. Phân loại BCL")
        st.caption("03. Đánh giá CRI")
        st.caption("04. Kết quả và giải pháp")
        st.caption("05. Xuất hồ sơ")

        st.divider()
        st.markdown("**Căn cứ pháp lý và kỹ thuật**")
        st.caption("Điều 32, TT 02/2022/TT-BTNMT")
        st.caption("QCVN 96:2025/BNNMT")
        st.caption("TCVN 13766:2023")
        st.caption(PROJECT_NAME)
        st.caption(f"{HOST_ORG}, 2026")

        if n > 0:
            st.divider()
            if st.button("🗑️ Xóa tất cả BCL", type="secondary", use_container_width=True):
                clear_all_bcl()
                st.rerun()
