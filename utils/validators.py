# -*- coding: utf-8 -*-
"""
Kiểm tra tính hợp lệ của dữ liệu đầu vào.
"""

from datetime import datetime

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

    nam_bat_dau = info.get("nam_bat_dau")
    nam_ngung = info.get("nam_ngung")
    if nam_bat_dau is not None and nam_ngung is not None:
        try:
            start = int(nam_bat_dau)
            stop = int(nam_ngung)
            current_year = datetime.now().year
            if start < 1980 or start > current_year:
                errors.append(f"Năm bắt đầu hoạt động phải nằm trong khoảng 1980–{current_year}.")
            if stop < start:
                errors.append("Năm ngừng tiếp nhận không được nhỏ hơn năm bắt đầu hoạt động.")
        except (ValueError, TypeError):
            errors.append("Năm bắt đầu và năm ngừng tiếp nhận phải là số nguyên hợp lệ.")

    lat = info.get("toa_do_lat")
    lon = info.get("toa_do_lon")
    if (lat is None) != (lon is None):
        errors.append("Nếu nhập tọa độ, cần nhập đủ cả vĩ độ và kinh độ.")
    if lat is not None and lon is not None:
        try:
            flat = float(lat)
            flon = float(lon)
            if not (8.0 <= flat <= 24.0 and 102.0 <= flon <= 110.0):
                errors.append("Tọa độ nhập vào nằm ngoài phạm vi hợp lý của Việt Nam.")
        except (ValueError, TypeError):
            errors.append("Tọa độ phải là giá trị số hợp lệ.")

    loai_bcl = info.get("loai_bcl", "")
    if loai_bcl not in ("HVS", "KHVS"):
        errors.append("Loại bãi chôn lấp phải là 'HVS' hoặc 'KHVS'.")

    return errors


def get_bcl_info_warnings(info: dict) -> list[str]:
    """
    Cảnh báo dữ liệu bất thường nhưng chưa phải lỗi bắt buộc.

    Returns:
        Danh sách cảnh báo để người dùng kiểm tra lại trước khi dùng cho hồ sơ.
    """
    warnings = []

    dien_tich = info.get("dien_tich_ha")
    if dien_tich is not None:
        try:
            dt = float(dien_tich)
            if dt > 100:
                warnings.append("Diện tích bãi lớn hơn 100 ha — cần kiểm tra lại đơn vị hoặc phạm vi khai báo.")
        except (ValueError, TypeError):
            pass

    chieu_cao = info.get("chieu_cao_m")
    if chieu_cao is not None:
        try:
            height = float(chieu_cao)
            if height > 50:
                warnings.append("Chiều cao ước tính lớn hơn 50 m — cần kiểm tra lại số liệu hiện trường.")
        except (ValueError, TypeError):
            pass

    the_tich = info.get("the_tich_m3")
    if the_tich is not None:
        try:
            volume = float(the_tich)
            if volume > 10_000_000:
                warnings.append("Thể tích ước tính lớn hơn 10 triệu m³ — cần kiểm tra lại số liệu hoặc đơn vị.")
        except (ValueError, TypeError):
            pass

    nam_bat_dau = info.get("nam_bat_dau")
    nam_ngung = info.get("nam_ngung")
    if nam_bat_dau is not None and nam_ngung is not None:
        try:
            start = int(nam_bat_dau)
            stop = int(nam_ngung)
            if stop - start > 50:
                warnings.append("Thời gian hoạt động lớn hơn 50 năm — cần kiểm tra lại lịch sử vận hành.")
            if stop > datetime.now().year:
                warnings.append("Năm ngừng tiếp nhận nằm trong tương lai — cần xác nhận đây là kế hoạch dự kiến.")
        except (ValueError, TypeError):
            pass

    return warnings


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
        Danh sách lỗi/cảnh báo với các thông số thiếu nhưng chưa có lý do.
    """
    warnings = []
    for pid in missing_ids:
        note = notes.get(pid, "").strip()
        if not note:
            warnings.append(
                f"Thông số {pid}: chưa nhập lý do thiếu dữ liệu "
                f"(cần ghi rõ lý do trước khi lưu kết quả vào hồ sơ)."
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
