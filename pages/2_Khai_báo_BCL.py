# -*- coding: utf-8 -*-
"""Trang 2 — Khai báo thông tin cơ bản bãi chôn lấp."""

import streamlit as st
from utils.validators import get_bcl_info_warnings, validate_bcl_info
from utils.sidebar import render_sidebar
from utils.session import get_all_bcl, get_bcl, set_active_bcl
from utils.ui import apply_global_styles, render_page_footer, render_page_header

apply_global_styles()
render_sidebar()
render_page_header(
    "Khai báo thông tin bãi chôn lấp",
    "Nhập thông tin định danh, vị trí, quy mô, lịch sử hoạt động và loại hình bãi chôn lấp. "
    "Các trường đánh dấu * là bắt buộc.",
    section="Bước 01 — Khai báo BCL",
)

# ── Chọn BCL đang chỉnh sửa
all_entries = get_all_bcl()
if all_entries:
    options = ["__new__"] + [entry["id"] for entry in all_entries]
    active_editing_id = st.session_state.get("_bcl_active_editing_id")
    active_view_id = st.session_state.get("bcl_active_id")
    default_id = active_editing_id or active_view_id
    default_index = options.index(default_id) if default_id in options else 0

    selected_edit_id = st.selectbox(
        "Chọn BCL để chỉnh sửa thông tin chung:",
        options=options,
        index=default_index,
        format_func=lambda x: (
            "➕ Tạo BCL mới"
            if x == "__new__"
            else f"{get_bcl(x)['info'].get('ten_bcl', '(chưa đặt tên)')} ({x})"
        ),
        key="bcl_info_edit_selector",
    )

    if selected_edit_id == "__new__":
        state_keys = ["_bcl_active_editing_id", "_bcl_saved_info", "_bcl_form_draft",
                      "_cri_scores_draft", "_cri_notes_draft", "bcl_active_id"]
        if any(st.session_state.get(key) is not None for key in state_keys):
            for key in ["_bcl_active_editing_id", "_bcl_saved_info", "_bcl_form_draft",
                        "_cri_scores_draft", "_cri_notes_draft"]:
                st.session_state.pop(key, None)
            st.session_state["bcl_active_id"] = None
            st.rerun()
    elif selected_edit_id != st.session_state.get("_bcl_active_editing_id"):
        selected_entry = get_bcl(selected_edit_id)
        if selected_entry:
            st.session_state["_bcl_active_editing_id"] = selected_edit_id
            st.session_state["_bcl_form_draft"] = selected_entry.get("info", {})
            st.session_state["_bcl_saved_info"] = selected_entry.get("info", {})
            st.session_state["_cri_scores_draft"] = selected_entry.get("scores", {})
            st.session_state["_cri_notes_draft"] = selected_entry.get("missing_notes", {})
            set_active_bcl(selected_edit_id)
            st.rerun()

# ── Dữ liệu mẫu (nếu người dùng muốn thử)
if st.checkbox("📂 Nạp dữ liệu mẫu từ Ví dụ PL2.4"):
    import json, os
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.json")
    try:
        with open(sample_path, encoding="utf-8") as f:
            sample = json.load(f)
        st.session_state["_bcl_form_draft"] = sample["info"]
        st.info("Đã nạp dữ liệu mẫu PL2.4. Các trường bên dưới đã được điền.")
    except Exception as e:
        st.error(f"Không thể nạp dữ liệu mẫu: {e}")

draft = st.session_state.get("_bcl_form_draft", {})

st.divider()

# ═══════════════════════════════════════════════════════
# PHẦN 1 — THÔNG TIN ĐỊNH DANH
# ═══════════════════════════════════════════════════════
st.subheader("1. Thông tin chung về bãi chôn lấp")
col1, col2 = st.columns(2)

with col1:
    ten_bcl = st.text_input(
        "Tên bãi chôn lấp *",
        value=draft.get("ten_bcl", ""),
        placeholder="Ví dụ: BCL Hạ Đình, BCL Nam Sơn...",
    )
    tinh = st.text_input(
        "Tỉnh / Thành phố *",
        value=draft.get("tinh", ""),
        placeholder="Ví dụ: Hà Nội, TP. Hồ Chí Minh...",
    )
with col2:
    xa = st.text_input(
        "Xã / Phường",
        value=draft.get("xa", ""),
    )
    col2a, col2b = st.columns(2)
    with col2a:
        toa_do_lat = st.number_input(
            "Vĩ độ (Latitude)",
            min_value=8.0, max_value=24.0,
            value=float(draft["toa_do_lat"]) if draft.get("toa_do_lat") else None,
            step=0.0001, format="%.4f",
            help="Tọa độ WGS84 — ví dụ: 21.0285",
        )
    with col2b:
        toa_do_lon = st.number_input(
            "Kinh độ (Longitude)",
            min_value=102.0, max_value=110.0,
            value=float(draft["toa_do_lon"]) if draft.get("toa_do_lon") else None,
            step=0.0001, format="%.4f",
            help="Tọa độ WGS84 — ví dụ: 105.8412",
        )

st.divider()

# ═══════════════════════════════════════════════════════
# PHẦN 2 — LOẠI HÌNH BCL (RẼ NHÁNH)
# ═══════════════════════════════════════════════════════
st.subheader("2. Loại hình bãi chôn lấp *")
loai_bcl = st.radio(
    "Chọn loại hình bãi chôn lấp:",
    options=["KHVS", "HVS"],
    format_func=lambda x: (
        "BCL không hợp vệ sinh (BCL-KHVS) — cần tính CRI"
        if x == "KHVS"
        else "BCL hợp vệ sinh (BCL-HVS) — không cần tính CRI"
    ),
    index=0 if draft.get("loai_bcl", "KHVS") == "KHVS" else 1,
    horizontal=True,
)

hvs_status = None
if loai_bcl == "HVS":
    st.info(
        "**BCL hợp vệ sinh** không cần tính CRI. "
        "Hệ thống sẽ phân loại theo mức độ đạt chuẩn QCVN 96:2025/BNNMT."
    )
    hvs_status = st.radio(
        "Mức độ đáp ứng tiêu chuẩn QCVN 96:2025:",
        options=["DAT_CHUAN", "CAN_BO_SUNG"],
        format_func=lambda x: (
            "Đạt chuẩn — BCL đã có đầy đủ công trình hạ tầng theo QCVN 96:2025"
            if x == "DAT_CHUAN"
            else "Cần bổ sung — BCL chưa đáp ứng đầy đủ, cần bổ sung một số hạng mục"
        ),
        horizontal=True,
    )
else:
    st.info(
        "**BCL không hợp vệ sinh** cần đánh giá CRI. "
        "Sau khi lưu thông tin này, chuyển sang trang **Nhập thông số CRI**."
    )

st.divider()

# ═══════════════════════════════════════════════════════
# PHẦN 3 — ĐẶC ĐIỂM VẬT LÝ
# ═══════════════════════════════════════════════════════
st.subheader("3. Đặc điểm vật lý")
col3, col4 = st.columns(2)

with col3:
    dien_tich_ha = st.number_input(
        "Diện tích khu chôn lấp (ha) *",
        min_value=0.01, max_value=1000.0,
        value=float(draft["dien_tich_ha"]) if draft.get("dien_tich_ha") else 1.0,
        step=0.1, format="%.2f",
        help="Tổng diện tích khu vực chôn lấp (không tính hạ tầng phụ trợ)",
    )
    chieu_cao_m = st.number_input(
        "Chiều cao ước tính (m)",
        min_value=0.0, max_value=100.0,
        value=float(draft["chieu_cao_m"]) if draft.get("chieu_cao_m") else 0.0,
        step=0.5, format="%.1f",
    )

with col4:
    the_tich_m3 = st.number_input(
        "Thể tích ước tính (m³)",
        min_value=0.0,
        value=float(draft["the_tich_m3"]) if draft.get("the_tich_m3") else 0.0,
        step=100.0, format="%.0f",
        help="Ước tính tổng thể tích chất thải đã chôn lấp",
    )

    col4a, col4b = st.columns(2)
    with col4a:
        nam_bat_dau = st.number_input(
            "Năm bắt đầu hoạt động",
            min_value=1980, max_value=2026,
            value=int(draft["nam_bat_dau"]) if draft.get("nam_bat_dau") else 2000,
            step=1,
        )
    with col4b:
        nam_ngung = st.number_input(
            "Năm ngừng tiếp nhận",
            min_value=1980, max_value=2030,
            value=int(draft["nam_ngung"]) if draft.get("nam_ngung") else 2020,
            step=1,
            help="Năm bãi chính thức ngừng tiếp nhận chất thải",
        )

ghi_chu = st.text_area(
    "Ghi chú thêm",
    value=draft.get("ghi_chu", ""),
    placeholder="Thông tin bổ sung về lịch sử hoạt động, đặc điểm đặc biệt...",
    height=80,
)

st.divider()

# ═══════════════════════════════════════════════════════
# AUTO-SAVE (thay thế nút Lưu)
# ═══════════════════════════════════════════════════════
info = {
    "ten_bcl": ten_bcl.strip(),
    "tinh": tinh.strip(),
    "xa": xa.strip(),
    "toa_do_lat": toa_do_lat if toa_do_lat else None,
    "toa_do_lon": toa_do_lon if toa_do_lon else None,
    "loai_bcl": loai_bcl,
    "hvs_status": hvs_status,
    "dien_tich_ha": dien_tich_ha,
    "the_tich_m3": the_tich_m3 if the_tich_m3 > 0 else None,
    "chieu_cao_m": chieu_cao_m if chieu_cao_m > 0 else None,
    "nam_bat_dau": int(nam_bat_dau),
    "nam_ngung": int(nam_ngung),
    "ghi_chu": ghi_chu.strip(),
}

errors = validate_bcl_info(info)
data_warnings = get_bcl_info_warnings(info)

if ten_bcl.strip():
    editing_id = st.session_state.get("_bcl_active_editing_id")

    if errors:
        for err in errors:
            st.warning(err)
        st.info("Hồ sơ chưa được lưu tự động do còn lỗi dữ liệu bắt buộc.")
    else:
        st.session_state["_bcl_saved_info"] = info

        for warn in data_warnings:
            st.warning(warn)

    if not errors and loai_bcl == "HVS":
        from core.classifier import classify_and_recommend
        from utils.session import add_bcl, update_bcl, get_bcl as _get_bcl

        hvs_data = classify_and_recommend(cri=None, bcl_type="HVS", hvs_status=hvs_status)
        hvs_result = {
            "H": None, "P": None, "R": None, "CRI": None,
            "risk": hvs_data["risk"],
            "solution": hvs_data["solution"],
            "missing_params": [],
            "assumed_max": [],
        }
        if editing_id and _get_bcl(editing_id):
            update_bcl(editing_id, info=info, scores={}, missing_notes={}, result=hvs_result)
        else:
            new_id = add_bcl(info=info, scores={}, missing_notes={}, result=hvs_result)
            st.session_state["_bcl_active_editing_id"] = new_id
            st.session_state.pop("_cri_scores_draft", None)
            st.session_state.pop("_cri_notes_draft", None)

        if not errors:
            sol_name = hvs_data["solution"]["short_name"]
            st.success(
                f"✅ Lưu tự động — **{ten_bcl}** ({tinh}) — BCL-HVS. "
                f"Giải pháp: **{sol_name}**. "
                "Chuyển sang trang **Kết quả** để xem chi tiết."
            )
    elif not errors:
        # BCL-KHVS: cập nhật info của BCL hiện tại nếu đã có trong danh sách
        if editing_id:
            from utils.session import update_bcl, get_bcl as _get_bcl
            if _get_bcl(editing_id):
                update_bcl(editing_id, info=info)

        if not errors:
            st.success(
                f"✅ Lưu tự động — **{ten_bcl}** ({tinh}) — BCL-KHVS. "
                "Chuyển sang trang **Nhập thông số CRI** để đánh giá."
            )
else:
    st.info("Nhập tên bãi chôn lấp để bắt đầu lưu tự động.")

# ── Nút hành động
st.divider()
col_btn, _ = st.columns([3, 5])
with col_btn:
    if st.button("➕ Thêm BCL mới", use_container_width=True,
                 help="Xóa form hiện tại và bắt đầu khai báo một bãi chôn lấp mới"):
        for key in ["_bcl_active_editing_id", "_bcl_saved_info", "_bcl_form_draft",
                    "_cri_scores_draft", "_cri_notes_draft"]:
            st.session_state.pop(key, None)
        st.session_state["bcl_active_id"] = None
        st.rerun()

render_page_footer()
