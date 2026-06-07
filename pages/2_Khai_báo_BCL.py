# -*- coding: utf-8 -*-
"""Trang 2 — Khai báo thông tin cơ bản bãi chôn lấp."""

import streamlit as st
from utils.validators import validate_bcl_info
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Khai báo BCL — BCL-CRI Tool", layout="wide")
render_sidebar()
st.title("📋 Khai báo thông tin bãi chôn lấp")
st.caption(
    "Nhập thông tin định danh và đặc điểm vật lý của bãi chôn lấp. "
    "Các trường đánh dấu * là bắt buộc."
)

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
        "Xã / Phường / Thị trấn",
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
# NÚT LƯU
# ═══════════════════════════════════════════════════════
col_btn1, col_btn2, _ = st.columns([2, 2, 4])

with col_btn1:
    btn_save = st.button("💾 Lưu thông tin BCL", type="primary", use_container_width=True)

with col_btn2:
    btn_clear = st.button("🔄 Nhập lại", use_container_width=True)

if btn_clear:
    st.session_state.pop("_bcl_form_draft", None)
    st.session_state.pop("_bcl_saved_info", None)
    st.rerun()

if btn_save:
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
    if errors:
        for err in errors:
            st.error(err)
    else:
        # Lưu vào session draft (sẽ kết hợp với scores ở Trang 3)
        st.session_state["_bcl_saved_info"] = info
        st.session_state.pop("_bcl_form_draft", None)
        # Xóa context chỉnh sửa cũ — BCL mới sẽ được tạo từ đầu
        st.session_state.pop("_bcl_active_editing_id", None)
        st.session_state.pop("_cri_scores_draft", None)
        st.session_state.pop("_cri_notes_draft", None)

        st.success(f"✅ Đã lưu thông tin: **{ten_bcl}** ({tinh})")

        if loai_bcl == "HVS":
            # BCL-HVS — tính ngay giải pháp, lưu vào session BCL list
            from core.classifier import classify_and_recommend
            from utils.session import add_bcl

            result = classify_and_recommend(cri=None, bcl_type="HVS", hvs_status=hvs_status)
            bcl_id = add_bcl(
                info=info,
                scores={},
                missing_notes={},
                result={
                    "H": None, "P": None, "R": None, "CRI": None,
                    "risk": result["risk"],
                    "solution": result["solution"],
                    "missing_params": [],
                    "assumed_max": [],
                },
            )
            st.info(
                f"BCL-HVS không cần tính CRI. "
                f"Giải pháp khuyến nghị: **{result['solution']['short_name']}**. "
                "Chuyển sang trang **Kết quả** để xem chi tiết."
            )
        else:
            st.info("Chuyển sang trang **Nhập thông số CRI** để tiếp tục đánh giá.")
