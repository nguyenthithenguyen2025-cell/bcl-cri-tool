# -*- coding: utf-8 -*-
"""
Tính toán chỉ số CRI theo phương pháp trung bình nhân có trọng số.

Công thức:
  H = Σ(wi · Hi)   với trọng số trong nhóm H (tổng = 1,00)
  P = Σ(wi · Pi)   với trọng số trong nhóm P (normalize về 1,00 từ tổng gốc 1,01)
  R = Σ(wi · Ri)   với trọng số trong nhóm R (tổng = 1,00)
  CRI = H^0,28 × P^0,40 × R^0,32

Phạm vi hợp lệ: CRI ∈ [0,25; 1,00]
Nguồn: Đề tài TNMT.2024.05.05, Trường ĐH Thủy Lợi (2026).
"""

import math
from typing import Optional
from config.parameters import PARAMETERS, PARAMS_BY_GROUP, GROUP_EXPONENTS, PARAM_BY_ID


def _build_weights() -> dict[str, dict[str, float]]:
    """
    Xây dựng dict trọng số đã normalize cho từng nhóm.
    Nhóm P có tổng gốc = 1,01 → chia đều để tổng = 1,00.
    """
    weights: dict[str, dict[str, float]] = {}
    for group, ids in PARAMS_BY_GROUP.items():
        raw = {pid: PARAM_BY_ID[pid]["weight"] for pid in ids}
        total = sum(raw.values())
        weights[group] = {pid: w / total for pid, w in raw.items()}
    return weights


# Trọng số đã normalize — tính một lần khi module được nạp
_WEIGHTS: dict[str, dict[str, float]] = _build_weights()


def calculate_group_index(group: str, scores: dict[str, float]) -> Optional[float]:
    """
    Tính chỉ số trung bình cộng có trọng số cho một nhóm (H, P hoặc R).

    Args:
        group  : "H", "P", hoặc "R"
        scores : {param_id: score} — chỉ cần chứa các id thuộc nhóm này

    Returns:
        Chỉ số nhóm [0,25 – 1,00], hoặc None nếu thiếu dữ liệu.
    """
    group_weights = _WEIGHTS[group]
    total_weight = 0.0
    weighted_sum = 0.0

    for pid, w in group_weights.items():
        if pid not in scores or scores[pid] is None:
            return None
        weighted_sum += w * scores[pid]
        total_weight += w

    if total_weight == 0:
        return None

    # total_weight ≈ 1,00 sau normalize — chia để phòng trường hợp làm tròn
    return weighted_sum / total_weight


def calculate_cri(scores: dict[str, float]) -> dict:
    """
    Tính toán đầy đủ: H, P, R và CRI từ dict điểm 14 thông số.

    Args:
        scores: {param_id: score} với 14 thông số.
                Điểm hợp lệ: 0,25 / 0,50 / 0,75 / 1,00.
                Nếu thiếu thông số → giả định 1,00 (rủi ro tối đa, trường hợp thận trọng nhất).

    Returns:
        Dict kết quả:
          {
            "H": float,
            "P": float,
            "R": float,
            "CRI": float,
            "missing_params": list[str],   # danh sách id bị thiếu
            "assumed_max": list[str],       # danh sách id được gán 1,00
          }
    """
    missing_params: list[str] = []
    assumed_max: list[str] = []

    # Điền giá trị mặc định 1,00 cho thông số thiếu
    filled_scores: dict[str, float] = {}
    for p in PARAMETERS:
        pid = p["id"]
        if pid not in scores or scores[pid] is None:
            filled_scores[pid] = 1.00
            missing_params.append(pid)
            assumed_max.append(pid)
        else:
            filled_scores[pid] = float(scores[pid])

    h = calculate_group_index("H", filled_scores)
    p = calculate_group_index("P", filled_scores)
    r = calculate_group_index("R", filled_scores)

    if h is None or p is None or r is None:
        return {
            "H": h, "P": p, "R": r, "CRI": None,
            "missing_params": missing_params,
            "assumed_max": assumed_max,
            "error": "Không thể tính CRI do thiếu dữ liệu nhóm.",
        }

    # CRI = H^0.28 × P^0.40 × R^0.32
    exp_h = GROUP_EXPONENTS["H"]
    exp_p = GROUP_EXPONENTS["P"]
    exp_r = GROUP_EXPONENTS["R"]

    # Đảm bảo domain hợp lệ (tránh lỗi số âm)
    h = max(0.25, min(1.00, h))
    p = max(0.25, min(1.00, p))
    r = max(0.25, min(1.00, r))

    cri = math.pow(h, exp_h) * math.pow(p, exp_p) * math.pow(r, exp_r)
    cri = round(max(0.25, min(1.00, cri)), 4)

    return {
        "H": round(h, 4),
        "P": round(p, 4),
        "R": round(r, 4),
        "CRI": cri,
        "missing_params": missing_params,
        "assumed_max": assumed_max,
    }


def get_weights_info() -> dict:
    """
    Trả về thông tin trọng số (gốc và sau normalize) để hiển thị trên giao diện.
    """
    info = {}
    for group, ids in PARAMS_BY_GROUP.items():
        info[group] = []
        for pid in ids:
            raw_w = PARAM_BY_ID[pid]["weight"]
            norm_w = _WEIGHTS[group][pid]
            info[group].append({
                "id": pid,
                "name": PARAM_BY_ID[pid]["name"],
                "weight_raw": raw_w,
                "weight_normalized": round(norm_w, 5),
            })
    return info
