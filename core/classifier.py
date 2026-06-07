# -*- coding: utf-8 -*-
"""
Phân loại mức độ rủi ro và khuyến nghị giải pháp đóng bãi dựa trên CRI.
"""

from config.parameters import CRI_THRESHOLDS, RISK_LABELS, RISK_COLORS
from config.solutions import SOLUTION_MAPPING


def classify_risk(cri: float) -> dict:
    """
    Phân loại mức độ rủi ro từ giá trị CRI.

    Returns:
        {
          "level": int,          # 1, 2, 3, hoặc 4
          "label": str,          # "Cấp 1 — Rủi ro thấp" ...
          "color": str,          # mã màu hex
          "cri": float,
        }
    """
    for threshold, level in CRI_THRESHOLDS:
        if cri < threshold:
            return {
                "level": level,
                "label": RISK_LABELS[level],
                "color": RISK_COLORS[level],
                "cri": cri,
            }
    # Trường hợp CRI = 1.00 đúng biên trên
    return {
        "level": 4,
        "label": RISK_LABELS[4],
        "color": RISK_COLORS[4],
        "cri": cri,
    }


def get_solution(bcl_type: str, risk_level: int = None) -> dict:
    """
    Tra cứu giải pháp khuyến nghị theo loại BCL và cấp rủi ro.

    Args:
        bcl_type   : "KHVS" hoặc "HVS"
        risk_level : 1–4 (chỉ dùng khi bcl_type == "KHVS")
                     Với BCL-HVS, dùng hvs_status thay thế.

    Returns:
        Dict giải pháp từ config/solutions.py
    """
    if bcl_type == "KHVS":
        key = f"KHVS_CAP_{risk_level}"
    elif bcl_type == "HVS_DAT_CHUAN":
        key = "HVS_DAT_CHUAN"
    elif bcl_type == "HVS_CAN_BO_SUNG":
        key = "HVS_CAN_BO_SUNG"
    else:
        key = "KHVS_CAP_4"   # mặc định thận trọng nhất

    return SOLUTION_MAPPING.get(key, SOLUTION_MAPPING["KHVS_CAP_4"])


def classify_and_recommend(
    cri: float,
    bcl_type: str = "KHVS",
    hvs_status: str = None,
) -> dict:
    """
    Kết hợp phân loại rủi ro và khuyến nghị giải pháp.

    Args:
        cri        : Giá trị CRI (0,25 – 1,00). None nếu là BCL-HVS.
        bcl_type   : "KHVS" (mặc định) hoặc "HVS"
        hvs_status : "DAT_CHUAN" hoặc "CAN_BO_SUNG" (chỉ khi bcl_type == "HVS")

    Returns:
        {
          "risk": dict,           # kết quả classify_risk()
          "solution": dict,       # giải pháp từ config/solutions.py
          "classification_key": str,
        }
    """
    if bcl_type == "HVS":
        status = hvs_status or "CAN_BO_SUNG"
        solution_key = f"HVS_{status}"
        solution = SOLUTION_MAPPING.get(solution_key, SOLUTION_MAPPING["HVS_CAN_BO_SUNG"])
        return {
            "risk": {
                "level": None,
                "label": "BCL hợp vệ sinh — không tính CRI",
                "color": "#95a5a6",
                "cri": None,
            },
            "solution": solution,
            "classification_key": solution_key,
        }

    risk = classify_risk(cri)
    solution = get_solution("KHVS", risk["level"])

    return {
        "risk": risk,
        "solution": solution,
        "classification_key": f"KHVS_CAP_{risk['level']}",
    }


def get_top_risk_params(scores: dict[str, float], n: int = 3) -> list[dict]:
    """
    Xác định n thông số có điểm cao nhất (rủi ro nhất) để hiển thị phân tích.

    Args:
        scores : {param_id: score}
        n      : số thông số muốn lấy (mặc định 3)

    Returns:
        Danh sách dict [{id, name, group, score, weight_normalized}]
        sắp xếp theo score giảm dần.
    """
    from config.parameters import PARAM_BY_ID
    from core.calculator import _WEIGHTS

    items = []
    for pid, score in scores.items():
        if score is None:
            continue
        param = PARAM_BY_ID.get(pid)
        if param is None:
            continue
        group = param["group"]
        w_norm = _WEIGHTS[group].get(pid, 0)
        items.append({
            "id": pid,
            "name": param["name"],
            "group": group,
            "score": score,
            "weight_normalized": round(w_norm, 4),
            "contribution": round(score * w_norm, 4),
        })

    # Sắp xếp theo điểm rồi đến đóng góp
    items.sort(key=lambda x: (x["score"], x["contribution"]), reverse=True)
    return items[:n]
