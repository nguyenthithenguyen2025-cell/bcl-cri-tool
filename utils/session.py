# -*- coding: utf-8 -*-
"""
Quản lý session state Streamlit cho nhiều BCL trong một phiên làm việc.

Cấu trúc dữ liệu mỗi BCL trong session:
  st.session_state["bcl_list"] = [
    {
      "id": str,              # UUID tự sinh, dùng làm khóa duy nhất
      "info": dict,           # Thông tin cơ bản BCL (Trang 2)
      "scores": dict,         # {param_id: score} 14 thông số (Trang 3)
      "missing_notes": dict,  # {param_id: lý do thiếu dữ liệu}
      "result": dict,         # {H, P, R, CRI, risk, solution} (sau tính toán)
      "created_at": str,      # ISO datetime
    },
    ...
  ]
  st.session_state["bcl_active_id"] = str   # BCL đang xem/chỉnh sửa
"""

import uuid
from datetime import datetime
import streamlit as st


def _ensure_session():
    if "bcl_list" not in st.session_state:
        st.session_state["bcl_list"] = []
    if "bcl_active_id" not in st.session_state:
        st.session_state["bcl_active_id"] = None


def add_bcl(info: dict, scores: dict, missing_notes: dict, result: dict) -> str:
    """
    Thêm BCL mới vào session. Trả về id của BCL vừa thêm.
    """
    _ensure_session()
    bcl_id = str(uuid.uuid4())[:8].upper()   # ID ngắn, dễ nhận diện
    entry = {
        "id": bcl_id,
        "info": info,
        "scores": scores,
        "missing_notes": missing_notes,
        "result": result,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    st.session_state["bcl_list"].append(entry)
    st.session_state["bcl_active_id"] = bcl_id
    return bcl_id


def update_bcl(bcl_id: str, info: dict = None, scores: dict = None,
               missing_notes: dict = None, result: dict = None) -> bool:
    """
    Cập nhật thông tin BCL đã có. Trả về True nếu tìm thấy và cập nhật thành công.
    """
    _ensure_session()
    for entry in st.session_state["bcl_list"]:
        if entry["id"] == bcl_id:
            if info is not None:
                entry["info"] = info
            if scores is not None:
                entry["scores"] = scores
            if missing_notes is not None:
                entry["missing_notes"] = missing_notes
            if result is not None:
                entry["result"] = result
            return True
    return False


def remove_bcl(bcl_id: str) -> bool:
    """
    Xóa BCL khỏi session. Trả về True nếu tìm thấy và xóa thành công.
    """
    _ensure_session()
    before = len(st.session_state["bcl_list"])
    st.session_state["bcl_list"] = [
        e for e in st.session_state["bcl_list"] if e["id"] != bcl_id
    ]
    removed = len(st.session_state["bcl_list"]) < before
    if removed and st.session_state["bcl_active_id"] == bcl_id:
        remaining = st.session_state["bcl_list"]
        st.session_state["bcl_active_id"] = remaining[-1]["id"] if remaining else None
    return removed


def get_bcl(bcl_id: str) -> dict | None:
    """
    Lấy dữ liệu một BCL theo id. Trả về None nếu không tìm thấy.
    """
    _ensure_session()
    for entry in st.session_state["bcl_list"]:
        if entry["id"] == bcl_id:
            return entry
    return None


def get_all_bcl() -> list[dict]:
    """
    Lấy toàn bộ danh sách BCL trong session.
    """
    _ensure_session()
    return st.session_state["bcl_list"]


def get_active_bcl() -> dict | None:
    """
    Lấy BCL đang được chọn (active). Trả về None nếu chưa có BCL nào.
    """
    _ensure_session()
    active_id = st.session_state.get("bcl_active_id")
    if active_id is None:
        return None
    return get_bcl(active_id)


def set_active_bcl(bcl_id: str):
    """
    Đặt BCL đang xem/chỉnh sửa.
    """
    _ensure_session()
    st.session_state["bcl_active_id"] = bcl_id


def count_bcl() -> int:
    """
    Đếm số BCL đã nhập trong session.
    """
    _ensure_session()
    return len(st.session_state["bcl_list"])


def get_bcl_summary_list() -> list[dict]:
    """
    Trả về danh sách tóm tắt tất cả BCL, sắp xếp theo CRI giảm dần.
    Dùng cho Trang 5 (So sánh BCL).

    BCL chưa có CRI (BCL-HVS) được xếp cuối bảng.
    """
    _ensure_session()
    summary = []
    for entry in st.session_state["bcl_list"]:
        info = entry.get("info", {})
        result = entry.get("result", {})
        cri = result.get("CRI")
        risk = result.get("risk", {})
        solution = result.get("solution", {})

        summary.append({
            "id": entry["id"],
            "ten_bcl": info.get("ten_bcl", ""),
            "tinh": info.get("tinh", ""),
            "huyen": info.get("huyen", ""),
            "dien_tich_ha": info.get("dien_tich_ha"),
            "loai_bcl": info.get("loai_bcl", "KHVS"),
            "H": result.get("H"),
            "P": result.get("P"),
            "R": result.get("R"),
            "CRI": cri,
            "risk_level": risk.get("level"),
            "risk_label": risk.get("label", ""),
            "risk_color": risk.get("color", "#cccccc"),
            "solution_name": solution.get("short_name", ""),
            "created_at": entry.get("created_at", ""),
        })

    # Sắp xếp: BCL-KHVS (có CRI) theo CRI giảm dần, BCL-HVS (không có CRI) xếp cuối
    has_cri = [s for s in summary if s["CRI"] is not None]
    no_cri = [s for s in summary if s["CRI"] is None]
    has_cri.sort(key=lambda x: x["CRI"], reverse=True)

    return has_cri + no_cri


def clear_all_bcl():
    """
    Xóa toàn bộ dữ liệu BCL trong session (dùng cho nút Reset).
    """
    st.session_state["bcl_list"] = []
    st.session_state["bcl_active_id"] = None
