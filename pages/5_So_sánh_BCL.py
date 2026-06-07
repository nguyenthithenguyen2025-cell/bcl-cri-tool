# -*- coding: utf-8 -*-
"""Trang 5 — So sánh nhiều BCL (bảng xếp hạng CRI)."""

import streamlit as st
import pandas as pd
from utils.session import get_bcl_summary_list, count_bcl
from utils.sidebar import render_sidebar

st.set_page_config(page_title="So sánh BCL — BCL-CRI Tool", layout="wide")
render_sidebar()
st.title("🏆 Bảng xếp hạng — So sánh nhiều BCL")

if count_bcl() == 0:
    st.info(
        "💡 Chưa có BCL nào. Hãy vào trang **Khai báo BCL** → **Nhập thông số CRI** "
        "để thêm ít nhất một BCL. Thêm nhiều BCL để so sánh."
    )
    st.markdown("""
**Trang này sẽ hiển thị sau khi có dữ liệu:**
- Bảng xếp hạng tất cả BCL theo CRI giảm dần (màu nền theo cấp rủi ro)
- Bộ lọc theo tỉnh/thành, cấp rủi ro, giải pháp khuyến nghị
- Biểu đồ so sánh chỉ số H / P / R giữa các BCL
- Biểu đồ phân tán CRI theo diện tích BCL
- Xuất bảng xếp hạng sang Excel
    """)
    st.stop()

if count_bcl() == 1:
    st.info(
        "💡 Hiện chỉ có 1 BCL. Thêm BCL khác để so sánh. "
        "Dữ liệu một BCL vẫn được hiển thị dưới đây."
    )

summary = get_bcl_summary_list()

# ── Bộ lọc
st.subheader("Bộ lọc")
filter_col1, filter_col2, filter_col3 = st.columns(3)

all_tinh = sorted(set(s["tinh"] for s in summary if s["tinh"]))
all_levels = sorted(set(s["risk_level"] for s in summary if s["risk_level"] is not None))
all_solutions = sorted(set(s["solution_name"] for s in summary if s["solution_name"]))

with filter_col1:
    sel_tinh = st.multiselect("Lọc theo tỉnh/thành:", options=all_tinh)
with filter_col2:
    sel_levels = st.multiselect(
        "Lọc theo cấp rủi ro:",
        options=all_levels,
        format_func=lambda x: f"Cấp {x}",
    )
with filter_col3:
    sel_solutions = st.multiselect("Lọc theo giải pháp:", options=all_solutions)

# Áp dụng bộ lọc
filtered = summary
if sel_tinh:
    filtered = [s for s in filtered if s["tinh"] in sel_tinh]
if sel_levels:
    filtered = [s for s in filtered if s["risk_level"] in sel_levels]
if sel_solutions:
    filtered = [s for s in filtered if s["solution_name"] in sel_solutions]

st.caption(f"Hiển thị {len(filtered)}/{len(summary)} BCL")
st.divider()

# ════════════════════════════════════════════════════════
# BẢNG XẾP HẠNG
# ════════════════════════════════════════════════════════
st.subheader("Bảng xếp hạng theo CRI")

RISK_LEVEL_LABELS = {1: "Cấp 1 — Thấp", 2: "Cấp 2 — TB", 3: "Cấp 3 — Cao", 4: "Cấp 4 — Rất cao"}
RISK_EMOJI = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴", None: "⚪"}

rows = []
for i, s in enumerate(filtered, 1):
    cri_str = f"{s['CRI']:.4f}" if s["CRI"] is not None else "BCL-HVS"
    h_str = f"{s['H']:.4f}" if s["H"] is not None else "—"
    p_str = f"{s['P']:.4f}" if s["P"] is not None else "—"
    r_str = f"{s['R']:.4f}" if s["R"] is not None else "—"
    level = s["risk_level"]
    level_str = RISK_EMOJI.get(level, "⚪") + " " + RISK_LEVEL_LABELS.get(level, "BCL-HVS")
    rows.append({
        "STT": i,
        "Tên BCL": s["ten_bcl"],
        "Tỉnh": s["tinh"],
        "DT (ha)": s["dien_tich_ha"],
        "H": h_str,
        "P": p_str,
        "R": r_str,
        "CRI": cri_str,
        "Cấp rủi ro": level_str,
        "Giải pháp KN": s["solution_name"],
        "ID": s["id"],
    })

df = pd.DataFrame(rows)
if not df.empty:
    st.dataframe(
        df.drop(columns=["ID"]),
        use_container_width=True,
        height=min(400, 60 + 40 * len(df)),
        hide_index=True,
    )
else:
    st.info("Không có BCL nào khớp với bộ lọc.")

st.divider()

# ════════════════════════════════════════════════════════
# BIỂU ĐỒ SO SÁNH
# ════════════════════════════════════════════════════════
if len(filtered) > 0:
    from utils.charts import comparison_bar_chart, scatter_cri_area

    st.subheader("Biểu đồ so sánh")

    khvs_data = [s for s in filtered if s["CRI"] is not None]

    if khvs_data:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("**So sánh chỉ số H / P / R của các BCL-KHVS**")
            fig_cbar = comparison_bar_chart(khvs_data)
            if fig_cbar:
                st.plotly_chart(fig_cbar, use_container_width=True)

        with col_c2:
            st.markdown("**CRI theo diện tích BCL**")
            fig_scatter = scatter_cri_area(khvs_data)
            if fig_scatter:
                st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Không có BCL-KHVS nào trong bộ lọc hiện tại để hiển thị biểu đồ.")

    st.divider()

# ════════════════════════════════════════════════════════
# XUẤT DANH SÁCH EXCEL
# ════════════════════════════════════════════════════════
st.subheader("Xuất danh sách")

if not df.empty:
    from io import BytesIO
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

    def make_ranking_excel(data: list[dict]) -> BytesIO:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Bảng xếp hạng BCL"

        headers = [
            "STT", "Tên BCL", "Tỉnh/TP", "Diện tích (ha)",
            "H", "P", "R", "CRI", "Cấp rủi ro", "Giải pháp khuyến nghị",
        ]
        ws.append(headers)

        # Style header
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1f77b4")
            cell.alignment = Alignment(horizontal="center", wrap_text=True)

        LEVEL_COLORS = {1: "2ecc71", 2: "f39c12", 3: "e67e22", 4: "e74c3c"}

        for i, s in enumerate(data, 1):
            row = [
                i,
                s["ten_bcl"],
                s["tinh"],
                s["dien_tich_ha"],
                f"{s['H']:.4f}" if s["H"] else "—",
                f"{s['P']:.4f}" if s["P"] else "—",
                f"{s['R']:.4f}" if s["R"] else "—",
                f"{s['CRI']:.4f}" if s["CRI"] else "BCL-HVS",
                RISK_LEVEL_LABELS.get(s["risk_level"], "BCL-HVS"),
                s["solution_name"],
            ]
            ws.append(row)

            level = s["risk_level"]
            if level and level in LEVEL_COLORS:
                fill = PatternFill("solid", fgColor=LEVEL_COLORS[level] + "40")
                for cell in ws[ws.max_row]:
                    cell.fill = fill

        ws.column_dimensions["A"].width = 6
        ws.column_dimensions["B"].width = 30
        ws.column_dimensions["C"].width = 20
        for col in ["D", "E", "F", "G", "H"]:
            ws.column_dimensions[col].width = 12
        ws.column_dimensions["I"].width = 22
        ws.column_dimensions["J"].width = 20

        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)
        return buf

    excel_buf = make_ranking_excel(filtered)
    st.download_button(
        label="📥 Tải xuống bảng xếp hạng (.xlsx)",
        data=excel_buf,
        file_name="Bang_xep_hang_BCL_CRI.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
