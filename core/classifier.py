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


def _group_level(value: float | None) -> tuple[str, str]:
    """Diễn giải định tính cho chỉ số nhóm H/P/R."""
    if value is None:
        return "Chưa có dữ liệu", "Chưa đủ dữ liệu để nhận xét nhóm này."
    if value < 0.36:
        return "thấp", "mức đóng góp rủi ro thấp"
    if value < 0.53:
        return "trung bình", "mức đóng góp rủi ro trung bình"
    if value < 0.69:
        return "cao", "mức đóng góp rủi ro cao"
    return "rất cao", "mức đóng góp rủi ro rất cao"


def _dominant_group(result: dict) -> str | None:
    """Xác định nhóm H/P/R có chỉ số cao nhất."""
    values = {g: result.get(g) for g in ("H", "P", "R") if result.get(g) is not None}
    if not values:
        return None
    return max(values, key=values.get)


def generate_technical_analysis(entry: dict) -> dict:
    """
    Tạo diễn giải chuyên môn cho kết quả CRI.

    Args:
        entry: dữ liệu một BCL trong session.

    Returns:
        Dict gồm summary, group_comments, dominant_group, top_risks,
        data_quality_notes, recommended_actions.
    """
    from config.parameters import PARAM_BY_ID

    info = entry.get("info", {})
    result = entry.get("result", {})
    scores = entry.get("scores", {})
    missing_notes = entry.get("missing_notes", {})
    risk = result.get("risk", {})
    solution = result.get("solution", {})
    cri = result.get("CRI")

    if info.get("loai_bcl") == "HVS":
        return {
            "summary": (
                "Bãi chôn lấp được khai báo là BCL hợp vệ sinh nên không tính chỉ số CRI. "
                "Việc lựa chọn giải pháp căn cứ vào mức độ đáp ứng yêu cầu kỹ thuật theo QCVN 96:2025/BNNMT."
            ),
            "group_comments": [],
            "dominant_group": None,
            "top_risks": [],
            "data_quality_notes": [],
            "recommended_actions": [
                "Rà soát hồ sơ hoàn công và hiện trạng công trình hạ tầng kỹ thuật.",
                "Kiểm tra khả năng vận hành hệ thống thoát nước mưa, thu gom nước rỉ rác và kiểm soát khí.",
                "Lập kế hoạch quản lý sau đóng bãi theo nhóm giải pháp được khuyến nghị.",
            ],
        }

    if cri is None:
        return {
            "summary": "BCL-KHVS chưa có kết quả CRI. Cần hoàn thành nhập thông số trước khi phân tích.",
            "group_comments": [],
            "dominant_group": None,
            "top_risks": [],
            "data_quality_notes": [],
            "recommended_actions": ["Hoàn thiện 14 thông số CRI và lý do thiếu dữ liệu nếu có."],
        }

    level = risk.get("level")
    solution_name = solution.get("short_name", "giải pháp khuyến nghị")
    summary = (
        f"CRI = {cri:.4f}, thuộc {risk.get('label', 'mức rủi ro chưa xác định')}. "
        f"Kết quả này tương ứng với nhóm {solution_name}. "
        "CRI càng cao cho thấy yêu cầu kiểm soát nguồn ô nhiễm, đường lan truyền và đối tượng tiếp nhận càng chặt chẽ."
    )

    group_names = {
        "H": "Nguồn nguy hại",
        "P": "Đường lan truyền",
        "R": "Đối tượng tiếp nhận",
    }
    group_interpretations = {
        "H": "phản ánh quy mô, tuổi bãi, thành phần nguy hại và biểu hiện nước rỉ rác tại nguồn",
        "P": "phản ánh khả năng ô nhiễm di chuyển qua lớp phủ, nước mưa, địa chất, nước mặt, nước ngầm và địa hình",
        "R": "phản ánh mức độ nhạy cảm của cộng đồng, nguồn nước sử dụng và hệ sinh thái xung quanh",
    }
    group_comments = []
    for group in ("H", "P", "R"):
        value = result.get(group)
        level_text, desc = _group_level(value)
        group_comments.append({
            "group": group,
            "name": group_names[group],
            "value": value,
            "level": level_text,
            "comment": (
                f"Nhóm {group} — {group_names[group]} đạt {value:.4f}, ở {desc}; "
                f"nhóm này {group_interpretations[group]}."
                if value is not None
                else f"Nhóm {group} — {group_names[group]} chưa đủ dữ liệu để nhận xét."
            ),
        })

    dominant = _dominant_group(result)
    dominant_comment = None
    if dominant:
        dominant_comment = (
            f"Nhóm chi phối cần ưu tiên xem xét là nhóm {dominant} — "
            f"{group_names[dominant]}, do có chỉ số cao nhất trong ba nhóm H/P/R."
        )

    filled_scores = {pid: score if score is not None else 1.00 for pid, score in scores.items()}
    top_risks = get_top_risk_params(filled_scores, n=5)
    for item in top_risks:
        param = PARAM_BY_ID.get(item["id"], {})
        item["technical_note"] = param.get("tooltip", "")

    assumed = result.get("assumed_max", [])
    data_quality_notes = []
    if assumed:
        data_quality_notes.append(
            f"Có {len(assumed)} thông số được xử lý theo nguyên tắc thận trọng và gán điểm 1,00: "
            f"{', '.join(assumed)}."
        )
        for pid in assumed:
            note = missing_notes.get(pid, "")
            if note:
                data_quality_notes.append(f"{pid}: {note}")

    recommended_actions = []
    if level in (1, 2):
        recommended_actions.extend([
            "Hoàn thiện hồ sơ hiện trạng và duy trì quan trắc sau đóng bãi theo tần suất phù hợp.",
            "Ưu tiên kiểm tra các thông số có điểm 0,75 hoặc 1,00 để tránh bỏ sót điểm nóng cục bộ.",
        ])
    elif level == 3:
        recommended_actions.extend([
            "Tổ chức khảo sát bổ sung về nước rỉ rác, nước ngầm và hiện trạng lớp phủ trước khi lập phương án đóng bãi.",
            "Ưu tiên thiết kế hệ thống thu gom, xử lý nước rỉ rác và kiểm soát khí bãi rác.",
            "Rà soát khoảng cách đến khu dân cư, nguồn nước và hệ sinh thái nhạy cảm để xác định vùng bảo vệ.",
        ])
    elif level == 4:
        recommended_actions.extend([
            "Thực hiện khảo sát chi tiết và đánh giá rủi ro môi trường ở mức dự án trước khi triển khai can thiệp.",
            "Xem xét phương án can thiệp nâng cao, cô lập ô nhiễm hoặc đào chuyển có kiểm soát nếu điều kiện hiện trường yêu cầu.",
            "Thiết lập kế hoạch ứng phó sự cố nước rỉ rác, khí bãi rác và trượt lở trong giai đoạn chuẩn bị đóng bãi.",
        ])

    if assumed:
        recommended_actions.append(
            "Bổ sung dữ liệu còn thiếu để giảm bất định của kết quả CRI trước khi dùng cho quyết định đầu tư chính thức."
        )

    return {
        "summary": summary,
        "group_comments": group_comments,
        "dominant_group": dominant_comment,
        "top_risks": top_risks,
        "data_quality_notes": data_quality_notes,
        "recommended_actions": recommended_actions,
    }
