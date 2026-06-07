# -*- coding: utf-8 -*-
"""Trang 3 — Nhập 14 thông số CRI và tính toán."""

import streamlit as st
from config.parameters import PARAMETERS, PARAMS_BY_GROUP, PARAM_BY_ID
from core.calculator import calculate_cri
from core.classifier import classify_and_recommend, get_top_risk_params
from utils.session import add_bcl, update_bcl
from utils.sidebar import render_sidebar

st.set_page_config(page_title="Nhập thông số CRI — BCL-CRI Tool", layout="wide")
render_sidebar()

st.title("📝 Nhập 14 thông số CRI")

# ── Kiểm tra xem đã có thông tin BCL chưa
saved_info = st.session_state.get("_bcl_saved_info")
if saved_info is None:
    st.info(
        "💡 Chưa có thông tin định danh BCL. Bạn vẫn có thể nhập thông số CRI và tính toán. "
        "Quay lại trang **Khai báo BCL** để bổ sung thông tin định danh trước hoặc sau."
    )
    saved_info = {}

if saved_info.get("loai_bcl") == "HVS":
    st.info(
        "BCL đã khai báo là **hợp vệ sinh (BCL-HVS)** — không cần nhập thông số CRI. "
        "Chuyển sang trang **Kết quả** để xem giải pháp khuyến nghị."
    )
    st.stop()

st.info(
    f"📍 Đang đánh giá: **{saved_info.get('ten_bcl', '')}** "
    f"({saved_info.get('tinh', '')}) — BCL không hợp vệ sinh"
)

# ── Tải dữ liệu mẫu
if st.checkbox("📂 Nạp điểm mẫu từ Ví dụ PL2.4"):
    import json, os
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.json")
    try:
        with open(sample_path, encoding="utf-8") as f:
            sample = json.load(f)
        st.session_state["_cri_scores_draft"] = sample["scores"]
        st.info("Đã nạp điểm mẫu PL2.4. Kết quả kỳ vọng: CRI ≈ 0,662 → Cấp 3.")
    except Exception as e:
        st.error(f"Không thể nạp dữ liệu mẫu: {e}")

scores_draft: dict = st.session_state.get("_cri_scores_draft", {})
notes_draft: dict = st.session_state.get("_cri_notes_draft", {})

st.markdown("""
**Hướng dẫn:**
- Chọn mức mô tả phù hợp nhất với điều kiện thực tế tại bãi chôn lấp.
- Điểm quy đổi (0,25 / 0,50 / 0,75 / 1,00) hiển thị tự động bên phải.
- Nếu chưa có dữ liệu cho thông số nào, chọn *"— Chưa có dữ liệu —"* và nhập lý do.
  Hệ thống sẽ gán điểm 1,00 (nguyên tắc thận trọng).
""")
st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Render một thông số CRI
# ─────────────────────────────────────────────────────────────────────────────
SCORE_OPTIONS = [None, 0.25, 0.50, 0.75, 1.00]
SCORE_NONE_LABEL = "— Chưa có dữ liệu —"

def _score_label(score, options_list):
    """Tạo nhãn hiển thị cho selectbox."""
    for opt in options_list:
        if opt["score"] == score:
            hint = f" ({opt['hint']})" if opt.get("hint") else ""
            return f"{opt['label']}{hint} → {score}"
    return SCORE_NONE_LABEL

def render_param(param: dict, col) -> tuple[float | None, str]:
    """
    Hiển thị một thông số trong cột `col`.
    Trả về (score, note).
    """
    pid = param["id"]
    options = param["options"]

    # Xây dựng labels cho selectbox
    select_labels = [SCORE_NONE_LABEL] + [
        f"{opt['label']} → {opt['score']}"
        + (f" ({opt['hint']})" if opt.get("hint") else "")
        for opt in options
    ]
    select_scores = [None] + [opt["score"] for opt in options]

    # Giá trị hiện tại từ draft
    current_score = scores_draft.get(pid)
    try:
        current_idx = select_scores.index(current_score)
    except ValueError:
        current_idx = 0

    with col:
        # Chỉ số nhóm và trọng số
        st.markdown(
            f"**{pid}** — {param['name']}"
            + (f" ({param['unit']})" if param.get("unit") else ""),
            help=param.get("tooltip", ""),
        )
        selected_idx = st.selectbox(
            label=f"Mức độ {pid}",
            options=range(len(select_labels)),
            format_func=lambda i: select_labels[i],
            index=current_idx,
            key=f"sel_{pid}",
            label_visibility="collapsed",
        )
        score = select_scores[selected_idx]

        # Hiển thị điểm quy đổi
        if score is not None:
            color_map = {0.25: "#2ecc71", 0.50: "#f39c12", 0.75: "#e67e22", 1.00: "#e74c3c"}
            color = color_map.get(score, "#888")
            st.markdown(
                f'<span style="color:{color};font-weight:bold;font-size:1.1rem;">'
                f"Điểm: {score}</span>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<span style="color:#999;">Điểm: chưa chọn → sẽ gán 1,00</span>',
                unsafe_allow_html=True,
            )

        # Ô nhập lý do nếu thiếu dữ liệu
        note = ""
        if score is None:
            note = st.text_input(
                f"Lý do thiếu dữ liệu ({pid})",
                value=notes_draft.get(pid, ""),
                placeholder="Ví dụ: chưa có số liệu địa chất, đang chờ khảo sát...",
                key=f"note_{pid}",
                label_visibility="visible",
            )

    return score, note


# ─────────────────────────────────────────────────────────────────────────────
# NHÓM H — Nguồn nguy hại
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("🔴 Nhóm H — Nguồn nguy hại (trọng số nhóm: 0,28)")
st.caption("4 thông số đánh giá mức độ nguy hại của nguồn ô nhiễm tại bãi chôn lấp.")

h_params = [PARAM_BY_ID[pid] for pid in PARAMS_BY_GROUP["H"]]
h_cols = st.columns(len(h_params))
h_scores = {}
h_notes = {}

for i, param in enumerate(h_params):
    score, note = render_param(param, h_cols[i])
    h_scores[param["id"]] = score
    h_notes[param["id"]] = note

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# NHÓM P — Đường lan truyền
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("🟡 Nhóm P — Đường lan truyền (trọng số nhóm: 0,40)")
st.caption("6 thông số đánh giá khả năng lan truyền ô nhiễm từ bãi ra môi trường xung quanh.")

p_params = [PARAM_BY_ID[pid] for pid in PARAMS_BY_GROUP["P"]]
# 6 thông số — hiển thị 3 cột, 2 hàng
p_row1 = st.columns(3)
p_row2 = st.columns(3)
p_cols = p_row1 + p_row2
p_scores = {}
p_notes = {}

for i, param in enumerate(p_params):
    score, note = render_param(param, p_cols[i])
    p_scores[param["id"]] = score
    p_notes[param["id"]] = note

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# NHÓM R — Đối tượng tiếp nhận
# ─────────────────────────────────────────────────────────────────────────────
st.subheader("🟠 Nhóm R — Đối tượng tiếp nhận (trọng số nhóm: 0,32)")
st.caption("4 thông số đánh giá mức độ nhạy cảm của các đối tượng có thể bị ảnh hưởng.")

r_params = [PARAM_BY_ID[pid] for pid in PARAMS_BY_GROUP["R"]]
r_cols = st.columns(len(r_params))
r_scores = {}
r_notes = {}

for i, param in enumerate(r_params):
    score, note = render_param(param, r_cols[i])
    r_scores[param["id"]] = score
    r_notes[param["id"]] = note

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# AUTO-TÍNH CRI VÀ AUTO-LƯU (thay thế nút "Tính CRI")
# ─────────────────────────────────────────────────────────────────────────────
all_scores = {**h_scores, **p_scores, **r_scores}
all_notes = {**h_notes, **p_notes, **r_notes}

# Luôn lưu draft
st.session_state["_cri_scores_draft"] = all_scores
st.session_state["_cri_notes_draft"] = all_notes

# Tính CRI
result = calculate_cri(all_scores)
classify = classify_and_recommend(result["CRI"], bcl_type="KHVS")
result["risk"] = classify["risk"]
result["solution"] = classify["solution"]

# Auto-lưu vào bcl_list khi ít nhất 1 điểm đã được chọn
n_selected = sum(1 for s in all_scores.values() if s is not None)
n_missing = 14 - n_selected

if n_selected > 0:
    if st.session_state.get("_bcl_active_editing_id"):
        update_bcl(
            st.session_state["_bcl_active_editing_id"],
            scores=all_scores,
            missing_notes=all_notes,
            result=result,
        )
        bcl_id = st.session_state["_bcl_active_editing_id"]
    else:
        bcl_id = add_bcl(
            info=saved_info,
            scores=all_scores,
            missing_notes=all_notes,
            result=result,
        )
        st.session_state["_bcl_active_editing_id"] = bcl_id

# ── Hiển thị kết quả live
st.divider()
cri_val = result["CRI"]
color = classify["risk"]["color"]

st.markdown(f"### Kết quả CRI — {saved_info.get('ten_bcl', '(chưa đặt tên)')}")

if n_missing > 0:
    st.caption(
        f"⚠️ {n_missing}/14 thông số chưa chọn — đang gán điểm 1,00 (nguyên tắc thận trọng). "
        "CRI hiển thị có thể cao hơn thực tế."
    )

col_r1, col_r2, col_r3, col_r4 = st.columns(4)
with col_r1:
    st.metric("Chỉ số H (Nguồn)", f"{result['H']:.4f}")
with col_r2:
    st.metric("Chỉ số P (Đường)", f"{result['P']:.4f}")
with col_r3:
    st.metric("Chỉ số R (Đối tượng)", f"{result['R']:.4f}")
with col_r4:
    st.metric("CRI tổng hợp", f"{cri_val:.4f}")

st.markdown(
    f'<div style="background:{color};color:white;padding:12px 20px;border-radius:8px;'
    f'font-size:1.1rem;font-weight:bold;">'
    f"🎯 {classify['risk']['label']} — Giải pháp: {classify['solution']['short_name']}"
    f"</div>",
    unsafe_allow_html=True,
)

# Top thông số rủi ro
filled = {k: v if v is not None else 1.00 for k, v in all_scores.items()}
top3 = get_top_risk_params(filled, n=3)
if top3 and n_selected > 0:
    st.markdown("**Top 3 thông số rủi ro cao nhất:**")
    for t in top3:
        st.markdown(
            f"- **{t['id']}** ({t['name']}): điểm = {t['score']}, "
            f"đóng góp = {t['contribution']:.4f}"
        )

if n_selected > 0:
    st.info(
        f"✅ Dữ liệu lưu tự động. "
        "Chuyển sang trang **Kết quả & Phân tích** để xem biểu đồ chi tiết."
    )
else:
    st.info("Chọn ít nhất một thông số để lưu kết quả vào danh sách BCL.")

# ── Nút Nhập lại
st.divider()
col_b, _ = st.columns([3, 5])
with col_b:
    if st.button("🔄 Nhập lại thông số CRI", use_container_width=True,
                 help="Xóa tất cả điểm đã chọn, giữ lại BCL trong danh sách"):
        st.session_state.pop("_cri_scores_draft", None)
        st.session_state.pop("_cri_notes_draft", None)
        st.rerun()
