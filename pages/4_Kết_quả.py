# -*- coding: utf-8 -*-
"""Trang 4 — Kết quả và phân tích cho một BCL."""

import streamlit as st
from utils.session import get_all_bcl, set_active_bcl, count_bcl
from utils.charts import (
    radar_chart,
    gauge_chart,
    bar_group_chart,
    score_heatmap,
)
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Kết quả — BCL-CRI Tool", layout="wide")
render_sidebar()
st.title("📊 Kết quả & Phân tích")

if count_bcl() == 0:
    st.info(
        "💡 Chưa có BCL nào được đánh giá. "
        "Hãy vào trang **Khai báo BCL** → **Nhập thông số CRI** để bắt đầu."
    )
    st.markdown("""
**Trang này sẽ hiển thị sau khi có kết quả:**
- Thẻ kết quả chính: CRI, cấp rủi ro (1–4), màu phân loại (xanh / vàng / cam / đỏ)
- Biểu đồ radar 14 thông số, đồng hồ CRI, biểu đồ cột H/P/R, bảng nhiệt điểm
- Phân tích tự động: top 3 thông số có mức rủi ro cao nhất
- Giải pháp đóng bãi khuyến nghị: hạng mục bắt buộc, tùy chọn, ưu/nhược điểm, căn cứ pháp lý
    """)
    st.stop()

# ── Chọn BCL để xem
all_bcl = get_all_bcl()
bcl_options = {e["id"]: f"{e['info'].get('ten_bcl', '')} ({e['id']})" for e in all_bcl}

selected_id = st.selectbox(
    "Chọn bãi chôn lấp để xem kết quả:",
    options=list(bcl_options.keys()),
    format_func=lambda x: bcl_options[x],
    index=0,
)
set_active_bcl(selected_id)

entry = next((e for e in all_bcl if e["id"] == selected_id), None)
if entry is None:
    st.error("Không tìm thấy dữ liệu BCL.")
    st.stop()

info = entry["info"]
result = entry.get("result", {})
scores = entry.get("scores", {})
risk = result.get("risk", {})
solution = result.get("solution", {})

st.divider()

# ════════════════════════════════════════════════════════
# PHẦN 1 — THẺ KẾT QUẢ CHÍNH
# ════════════════════════════════════════════════════════
color = risk.get("color", "#95a5a6")
cri_val = result.get("CRI")
loai_bcl = info.get("loai_bcl", "KHVS")

st.markdown(
    f'<div style="background:{color};color:white;padding:16px 24px;border-radius:10px;'
    f'margin-bottom:16px;">'
    f'<span style="font-size:1.6rem;font-weight:bold;">'
    f'{info.get("ten_bcl", "")}</span><br>'
    f'<span style="font-size:1.1rem;">{risk.get("label", "")}</span>'
    + (f' | CRI = {cri_val:.4f}' if cri_val else "")
    + f'</div>',
    unsafe_allow_html=True,
)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Chỉ số H", f"{result['H']:.4f}" if result.get("H") else "—")
with col2:
    st.metric("Chỉ số P", f"{result['P']:.4f}" if result.get("P") else "—")
with col3:
    st.metric("Chỉ số R", f"{result['R']:.4f}" if result.get("R") else "—")
with col4:
    st.metric("CRI", f"{cri_val:.4f}" if cri_val else "—")
with col5:
    st.metric("Cấp rủi ro", risk.get("level", "—") or "HVS")

if result.get("assumed_max"):
    st.warning(
        f"⚠️ {len(result['assumed_max'])} thông số được gán điểm 1,00 do thiếu dữ liệu: "
        f"{', '.join(result['assumed_max'])}. CRI có thể cao hơn thực tế."
    )

st.divider()

# ════════════════════════════════════════════════════════
# PHẦN 2 — BIỂU ĐỒ
# ════════════════════════════════════════════════════════
if loai_bcl == "KHVS" and scores:
    st.subheader("Biểu đồ phân tích")

    col_g1, col_g2 = st.columns([3, 2])
    with col_g1:
        st.markdown("**Biểu đồ radar — 14 thông số CRI**")
        fig_radar = radar_chart(scores)
        if fig_radar:
            st.plotly_chart(fig_radar, use_container_width=True)

    with col_g2:
        if cri_val:
            st.markdown("**Đồng hồ CRI**")
            fig_gauge = gauge_chart(cri_val, risk.get("level", 1))
            if fig_gauge:
                st.plotly_chart(fig_gauge, use_container_width=True)

    col_g3, col_g4 = st.columns(2)
    with col_g3:
        st.markdown("**So sánh chỉ số H / P / R**")
        fig_bar = bar_group_chart(
            result.get("H"), result.get("P"), result.get("R")
        )
        if fig_bar:
            st.plotly_chart(fig_bar, use_container_width=True)

    with col_g4:
        st.markdown("**Điểm từng thông số**")
        fig_heat = score_heatmap(scores)
        if fig_heat:
            st.plotly_chart(fig_heat, use_container_width=True)

    st.divider()

# ════════════════════════════════════════════════════════
# PHẦN 3 — PHÂN TÍCH TỰ ĐỘNG
# ════════════════════════════════════════════════════════
if loai_bcl == "KHVS" and scores:
    from core.classifier import get_top_risk_params
    filled_scores = {k: v if v is not None else 1.00 for k, v in scores.items()}
    top3 = get_top_risk_params(filled_scores, n=3)

    st.subheader("Phân tích tự động")
    if top3:
        st.markdown("**Top 3 thông số có mức rủi ro cao nhất:**")
        for i, t in enumerate(top3, 1):
            color_p = {0.25: "🟢", 0.50: "🟡", 0.75: "🟠", 1.00: "🔴"}.get(t["score"], "⚪")
            st.markdown(
                f"{i}. {color_p} **{t['id']} — {t['name']}**: "
                f"điểm = {t['score']} | đóng góp vào nhóm {t['group']} = {t['contribution']:.4f}"
            )

    if cri_val:
        if cri_val < 0.36:
            st.success(
                "CRI thấp cho thấy bãi có mức độ ô nhiễm và rủi ro tiềm năng thấp. "
                "Giải pháp đóng bãi đơn giản (phủ xanh) có thể đủ điều kiện áp dụng."
            )
        elif cri_val < 0.53:
            st.info(
                "CRI ở mức trung bình. Bãi cần được đóng theo yêu cầu kỹ thuật cơ bản "
                "(lớp phủ kỹ thuật + thoát khí thụ động) và theo dõi dài hạn."
            )
        elif cri_val < 0.69:
            st.warning(
                "CRI cao — bãi có nguy cơ ô nhiễm đáng kể. Cần đóng bãi tăng cường với "
                "hệ thống thu gom và xử lý nước rỉ rác, thu khí chủ động."
            )
        else:
            st.error(
                "CRI rất cao — bãi có nguy cơ ô nhiễm nghiêm trọng. "
                "Cần can thiệp nâng cao hoặc đào chuyển chất thải. "
                "Khuyến nghị khảo sát chi tiết và lập đề án can thiệp ngay."
            )

    st.divider()

# ════════════════════════════════════════════════════════
# PHẦN 4 — GIẢI PHÁP KHUYẾN NGHỊ
# ════════════════════════════════════════════════════════
st.subheader("Giải pháp đóng bãi khuyến nghị")

if solution:
    st.markdown(f"### {solution.get('name', '')}")
    st.markdown(solution.get("description", ""))

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("**Hạng mục bắt buộc:**")
        for item in solution.get("mandatory_items", []):
            st.markdown(f"- {item}")

    with col_s2:
        st.markdown("**Hạng mục khuyến nghị thêm:**")
        for item in solution.get("optional_items", []):
            st.markdown(f"- {item}")

    col_s3, col_s4 = st.columns(2)
    with col_s3:
        st.markdown("**Ưu điểm:**")
        for a in solution.get("advantages", []):
            st.markdown(f"✅ {a}")
    with col_s4:
        st.markdown("**Hạn chế:**")
        for d in solution.get("disadvantages", []):
            st.markdown(f"⚠️ {d}")

    st.markdown(
        f"**Thời gian quản lý sau đóng bãi:** {solution.get('monitoring_period', '—')}"
    )
    st.markdown(
        f"**Mức chi phí ước tính:** {solution.get('estimated_cost_level', '—')}"
    )
    st.caption(f"Căn cứ pháp lý: {solution.get('legal_basis', '—')}")

# ── Gợi ý tiếp theo
st.divider()
col_nx1, col_nx2 = st.columns(2)
with col_nx1:
    st.info("👉 Thêm BCL khác: quay lại trang **Khai báo BCL**")
with col_nx2:
    st.info("👉 So sánh tất cả BCL: chuyển sang trang **So sánh BCL**")
