# -*- coding: utf-8 -*-
"""Trang 6 — Xuất báo cáo kỹ thuật (Excel, Word, PDF) và lưu/tải phiên."""

import streamlit as st
from utils.session import get_all_bcl, count_bcl, export_session_json, import_session_json
from utils.sidebar import render_sidebar
from utils.ui import apply_global_styles, render_page_header

apply_global_styles()
render_sidebar()
render_page_header(
    "Xuất hồ sơ và báo cáo kỹ thuật",
    "Tạo file Excel, Word, HTML/PDF và JSON để lưu trữ hồ sơ đánh giá, chia sẻ kết quả "
    "hoặc tiếp tục phiên làm việc sau.",
    section="Bước 05 — Xuất hồ sơ",
)

if count_bcl() == 0:
    st.info(
        "💡 Chưa có BCL nào. Hãy vào trang **Khai báo BCL** → **Nhập thông số CRI** "
        "để có dữ liệu trước khi xuất báo cáo."
    )

    st.subheader("Tải phiên làm việc đã lưu")
    st.caption("Nếu bạn đã xuất phiên thành file JSON trước đó, hãy tải lại để tiếp tục.")
    uploaded_restore = st.file_uploader(
        "Chọn file JSON phiên làm việc (.json):",
        type=["json"],
        key="restore_empty",
    )
    if uploaded_restore is not None:
        n_added, err = import_session_json(uploaded_restore.getvalue())
        if err:
            st.error(f"❌ {err}")
        elif n_added == 0:
            st.warning("File không chứa BCL mới nào (có thể đã tồn tại trong phiên hiện tại).")
        else:
            st.success(f"✅ Đã tải lại {n_added} BCL từ phiên cũ.")
            st.rerun()

    st.divider()
    st.markdown("""
**Trang này hỗ trợ xuất các định dạng sau:**
- **Excel (.xlsx):** 3 sheet — Thông tin BCL | Điểm CRI | Kết quả & Giải pháp
- **Word (.docx):** Báo cáo kỹ thuật đầy đủ theo mẫu (thông tin BCL, bảng CRI, biểu đồ, giải pháp, căn cứ pháp lý)
- **PDF:** In trực tiếp từ file HTML bằng Chrome/Edge (Ctrl+P)
- **JSON:** Lưu toàn bộ phiên làm việc để tải lại sau
    """)
    st.stop()

all_bcl = get_all_bcl()

# ── Chọn BCL cần xuất
st.subheader("1. Chọn BCL cần xuất")
export_mode = st.radio(
    "Phạm vi xuất:",
    ["Chọn một BCL", "Xuất tất cả BCL"],
    horizontal=True,
)

selected_entries = []
if export_mode == "Chọn một BCL":
    bcl_options = {e["id"]: f"{e['info'].get('ten_bcl', '')} ({e['id']})" for e in all_bcl}
    sel_id = st.selectbox(
        "Chọn BCL:",
        options=list(bcl_options.keys()),
        format_func=lambda x: bcl_options[x],
    )
    selected_entries = [e for e in all_bcl if e["id"] == sel_id]
else:
    selected_entries = all_bcl
    st.info(f"Sẽ xuất tất cả {len(all_bcl)} BCL.")

st.divider()

# ── Tuỳ chọn báo cáo
st.subheader("2. Nội dung báo cáo")
include_charts = st.checkbox("Bao gồm biểu đồ (radar, gauge, bar)", value=True)
include_solution_detail = st.checkbox("Bao gồm chi tiết giải pháp đóng bãi", value=True)
include_legal = st.checkbox("Bao gồm căn cứ pháp lý", value=True)

st.divider()

# ════════════════════════════════════════════════════════
# XUẤT EXCEL
# ════════════════════════════════════════════════════════
st.subheader("3. Xuất Excel (.xlsx)")
st.caption("3 sheet: Thông tin BCL | Điểm CRI | Kết quả & Giải pháp")

if st.button("📥 Tạo file Excel", type="primary"):
    from export.excel_export import export_to_excel
    from io import BytesIO

    with st.spinner("Đang tạo file Excel..."):
        try:
            buf = export_to_excel(selected_entries)
            n = len(selected_entries)
            fname = (
                f"CRI_{selected_entries[0]['info'].get('ten_bcl','BCL').replace(' ','_')}.xlsx"
                if n == 1
                else "Danh_sach_BCL_CRI.xlsx"
            )
            st.download_button(
                label=f"💾 Tải xuống Excel ({n} BCL)",
                data=buf,
                file_name=fname,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            st.success("✅ File Excel đã sẵn sàng.")
        except Exception as e:
            st.error(f"Lỗi khi tạo Excel: {e}")

st.divider()

# ════════════════════════════════════════════════════════
# XUẤT WORD
# ════════════════════════════════════════════════════════
st.subheader("4. Xuất Word (.docx)")
st.caption("Báo cáo kỹ thuật đầy đủ theo mẫu: thông tin BCL, bảng CRI, giải pháp, căn cứ pháp lý.")

if st.button("📥 Tạo file Word", type="primary"):
    from export.word_export import export_to_word

    with st.spinner("Đang tạo file Word..."):
        try:
            for entry in selected_entries:
                buf = export_to_word(
                    entry,
                    include_solution=include_solution_detail,
                    include_legal=include_legal,
                )
                ten = entry["info"].get("ten_bcl", "BCL").replace(" ", "_")
                st.download_button(
                    label=f"💾 Tải xuống Word — {entry['info'].get('ten_bcl', '')}",
                    data=buf,
                    file_name=f"BaoCao_CRI_{ten}.docx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument"
                        ".wordprocessingml.document"
                    ),
                    key=f"word_{entry['id']}",
                )
            st.success("✅ File Word đã sẵn sàng.")
        except Exception as e:
            st.error(f"Lỗi khi tạo Word: {e}")

st.divider()

# ════════════════════════════════════════════════════════
# XUẤT HTML / PDF
# ════════════════════════════════════════════════════════
st.subheader("5. Xuất HTML → In thành PDF")
st.caption(
    "Tải file HTML → mở bằng trình duyệt (Chrome/Edge) → Ctrl+P → 'Save as PDF'. "
    "Hỗ trợ đầy đủ tiếng Việt, không cần cài thêm phần mềm."
)

if st.button("📥 Tạo file HTML (in PDF)", type="primary"):
    from export.html_export import export_to_html

    with st.spinner("Đang tạo file HTML..."):
        try:
            for entry in selected_entries:
                html_bytes = export_to_html(
                    entry,
                    include_solution=include_solution_detail,
                    include_legal=include_legal,
                )
                ten = entry["info"].get("ten_bcl", "BCL").replace(" ", "_")
                st.download_button(
                    label=f"💾 Tải xuống HTML — {entry['info'].get('ten_bcl', '')}",
                    data=html_bytes,
                    file_name=f"BaoCao_CRI_{ten}.html",
                    mime="text/html; charset=utf-8",
                    key=f"html_{entry['id']}",
                )
            st.success("✅ File HTML đã sẵn sàng. Mở file bằng trình duyệt rồi nhấn Ctrl+P để in thành PDF.")
        except Exception as e:
            st.error(f"Lỗi khi tạo HTML: {e}")

st.divider()

# ════════════════════════════════════════════════════════
# LƯU / TẢI PHIÊN LÀM VIỆC (JSON)
# ════════════════════════════════════════════════════════
st.subheader("6. Lưu / Tải phiên làm việc")
st.caption(
    "Lưu toàn bộ dữ liệu BCL trong phiên hiện tại thành file JSON. "
    "Tải lại file này lần sau để tiếp tục mà không cần nhập lại từ đầu."
)

col_save, col_load = st.columns(2)

with col_save:
    st.markdown("**Lưu phiên hiện tại**")
    from datetime import datetime as _dt
    fname_json = f"BCL_CRI_phien_{_dt.now().strftime('%Y%m%d_%H%M')}.json"
    json_bytes = export_session_json()
    st.download_button(
        label=f"💾 Tải xuống JSON ({count_bcl()} BCL)",
        data=json_bytes,
        file_name=fname_json,
        mime="application/json",
        type="primary",
    )
    st.caption(f"File: `{fname_json}`")

with col_load:
    st.markdown("**Tải lại phiên cũ**")
    uploaded_json = st.file_uploader(
        "Chọn file JSON đã lưu:",
        type=["json"],
        key="restore_full",
    )
    if uploaded_json is not None:
        n_added, err = import_session_json(uploaded_json.getvalue())
        if err:
            st.error(f"❌ {err}")
        elif n_added == 0:
            st.info("Không có BCL mới — tất cả ID đã tồn tại trong phiên hiện tại.")
        else:
            st.success(f"✅ Đã nhập thêm {n_added} BCL từ file.")
            st.rerun()

st.divider()

# ════════════════════════════════════════════════════════
# LƯU Ý
# ════════════════════════════════════════════════════════
st.info("""
**Lưu ý khi xuất báo cáo:**
- **Excel:** Phù hợp để lưu trữ và xử lý số liệu thêm.
- **Word:** Phù hợp để trình ký hoặc đính kèm hồ sơ kỹ thuật (định dạng .docx).
- **HTML → PDF:** Mở file HTML bằng Chrome/Edge → Ctrl+P → Destination: Save as PDF → Print. Hỗ trợ đầy đủ tiếng Việt.
- **JSON:** Lưu toàn bộ phiên làm việc. Tải lại file này để tiếp tục mà không cần nhập lại.
- Nếu Word hiển thị font lỗi, hãy kiểm tra font chữ đã được cài đặt trên máy tính.
""")
