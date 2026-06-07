# -*- coding: utf-8 -*-
"""
Kiểm tra tính hợp lệ của dữ liệu đầu vào.
"""

from config.parameters import PARAMETERS, VALID_SCORES, PARAMS_BY_GROUP


def validate_bcl_info(info: dict) -> list[str]:
    """
    Kiểm tra thông tin cơ bản BCL.

    Returns:
        Danh sách thông báo lỗi (rỗng nếu hợp lệ).
    """
    errors = []

    if not info.get("ten_bcl", "").strip():
        errors.append("Tên bãi chôn lấp không được để trống.")

    if not info.get("tinh", "").strip():
        errors.append("Tỉnh/thành phố không được để trống.")

    dien_tich = info.get("dien_tich_ha")
    if dien_tich is not None:
        try:
            dt = float(dien_tich)
            if dt <= 0:
                errors.append("Diện tích bãi phải lớn hơn 0.")
            elif dt > 1000:
                errors.append("Diện tích bãi nhập vào lớn hơn 1.000 ha — hãy kiểm tra lại.")
        except (ValueError, TypeError):
            errors.append("Diện tích bãi phải là số thực dương.")

    loai_bcl = info.get("loai_bcl", "")
    if loai_bcl not in ("HVS", "KHVS"):
        errors.append("Loại bãi chôn lấp phải là 'HVS' hoặc 'KHVS'.")

    return errors


def validate_scores(scores: dict) -> dict:
    """
    Kiểm tra điểm 14 thông số CRI.

    Args:
        scores: {param_id: score | None}

    Returns:
        {
          "errors": list[str],            # lỗi cứng (giá trị sai)
          "warnings": list[str],          # cảnh báo (thiếu dữ liệu → gán 1,00)
          "missing_ids": list[str],       # danh sách thông số chưa nhập
          "invalid_ids": list[str],       # danh sách thông số có giá trị sai
        }
    """
    errors = []
    warnings = []
    missing_ids = []
    invalid_ids = []

    param_ids = [p["id"] for p in PARAMETERS]

    for pid in param_ids:
        val = scores.get(pid)
        if val is None:
            missing_ids.append(pid)
            warnings.append(
                f"Thông số {pid} chưa có dữ liệu → sẽ gán điểm 1,00 (rủi ro tối đa)."
            )
        else:
            try:
                fval = float(val)
                if fval not in VALID_SCORES:
                    errors.append(
                        f"Thông số {pid} có điểm {fval} không hợp lệ. "
                        f"Giá trị phải là một trong: {VALID_SCORES}."
                    )
                    invalid_ids.append(pid)
            except (ValueError, TypeError):
                errors.append(f"Thông số {pid}: giá trị '{val}' không phải số.")
                invalid_ids.append(pid)

    return {
        "errors": errors,
        "warnings": warnings,
        "missing_ids": missing_ids,
        "invalid_ids": invalid_ids,
    }


def validate_missing_notes(missing_ids: list[str], notes: dict) -> list[str]:
    """
    Kiểm tra xem người dùng đã nhập lý do cho các thông số thiếu chưa.

    Args:
        missing_ids : danh sách param_id chưa có điểm
        notes       : {param_id: note_text}

    Returns:
        Danh sách cảnh báo với các thông số thiếu nhưng chưa có lý do.
    """
    warnings = []
    for pid in missing_ids:
        note = notes.get(pid, "").strip()
        if not note:
            warnings.append(
                f"Thông số {pid}: chưa nhập lý do thiếu dữ liệu "
                f"(hệ thống vẫn xử lý được, nhưng nên ghi rõ lý do để lưu hồ sơ)."
            )
    return warnings


def validate_cri_result(result: dict) -> list[str]:
    """
    Kiểm tra kết quả tính CRI có hợp lệ không.

    Returns:
        Danh sách cảnh báo (rỗng nếu hợp lệ).
    """
    warnings = []

    cri = result.get("CRI")
    if cri is None:
        warnings.append("Không tính được CRI. Kiểm tra lại dữ liệu đầu vào.")
        return warnings

    if not (0.25 <= cri <= 1.00):
        warnings.append(
            f"CRI = {cri:.4f} nằm ngoài phạm vi [0,25 – 1,00]. "
            "Kết quả cần được kiểm tra lại."
        )

    for group in ("H", "P", "R"):
        val = result.get(group)
        if val is not None and not (0.25 <= val <= 1.00):
            warnings.append(
                f"Chỉ số nhóm {group} = {val:.4f} nằm ngoài phạm vi [0,25 – 1,00]."
            )

    if result.get("assumed_max"):
        count = len(result["assumed_max"])
        warnings.append(
            f"{count} thông số được gán điểm 1,00 do thiếu dữ liệu: "
            f"{', '.join(result['assumed_max'])}. "
            "CRI có thể cao hơn thực tế — cần bổ sung dữ liệu để có kết quả chính xác hơn."
        )

    return warnings
