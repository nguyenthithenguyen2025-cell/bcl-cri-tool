# -*- coding: utf-8 -*-
"""
Định nghĩa 6 nhóm giải pháp đóng bãi chôn lấp và điều kiện áp dụng.
Nguồn: Đề tài TNMT.2024.05.05, Trường ĐH Thủy Lợi (2026).

Sơ đồ phân loại:
  BCL-HVS đạt chuẩn     → GP_21 (Đóng bãi cơ bản)
  BCL-HVS cần bổ sung   → GP_22 (Đóng bãi tăng cường)
  BCL-KHVS Cấp 1        → GP_1  (Đơn giản/phủ xanh)
  BCL-KHVS Cấp 2        → GP_21 (Đóng bãi cơ bản)
  BCL-KHVS Cấp 3        → GP_22 (Đóng bãi tăng cường)
  BCL-KHVS Cấp 4        → GP_3  (Nâng cao)
"""

# ─────────────────────────────────────────────────────────────────────────────
# NHÓM GIẢI PHÁP 1 — Đóng bãi đơn giản (phủ xanh)
# Áp dụng: BCL-KHVS có CRI < 0,36 (Cấp 1 — rủi ro thấp)
# ─────────────────────────────────────────────────────────────────────────────
GP_1 = {
    "id": "GP_1",
    "name": "Nhóm GP 1 — Đóng bãi đơn giản, phủ xanh",
    "short_name": "GP 1",
    "applicable_to": ["BCL-KHVS Cấp 1"],
    "cri_range": (0.00, 0.36),
    "description": (
        "Áp dụng cho BCL-KHVS có mức rủi ro thấp (CRI < 0,36). "
        "Giải pháp tập trung vào che phủ bề mặt và phủ xanh, "
        "không yêu cầu hệ thống kỹ thuật phức tạp."
    ),
    "mandatory_items": [
        "San gạt, tạo mái dốc ổn định (độ dốc mái ≤ 1:3)",
        "Phủ lớp đất tối thiểu dày 0,5 m",
        "Trồng cỏ và cây bụi chịu hạn phủ toàn bộ bề mặt",
        "Xây dựng rãnh thoát nước mưa xung quanh bãi",
        "Cắm biển báo cảnh báo khu vực bãi đã đóng",
    ],
    "optional_items": [
        "Hệ thống thoát khí đơn giản (ống thoát khí thụ động)",
        "Rào chắn xung quanh ngăn xâm nhập trái phép",
        "Quan trắc môi trường định kỳ (tối thiểu 1 năm/lần)",
    ],
    "monitoring_period": "Tối thiểu 5 năm sau khi hoàn thành đóng bãi",
    "estimated_cost_level": "Thấp",
    "advantages": [
        "Chi phí thấp, thi công đơn giản",
        "Có thể thực hiện bằng nguồn lực địa phương",
        "Phù hợp với bãi nhỏ, ít ô nhiễm",
    ],
    "disadvantages": [
        "Không kiểm soát được nước rỉ rác và khí bãi rác",
        "Yêu cầu theo dõi lâu dài để phát hiện vấn đề phát sinh",
    ],
    "legal_basis": "Điều 32, Thông tư 02/2022/TT-BTNMT",
}

# ─────────────────────────────────────────────────────────────────────────────
# NHÓM GIẢI PHÁP 2.1 — Đóng bãi cơ bản
# Áp dụng: BCL-HVS đạt chuẩn QCVN 96:2025
#           BCL-KHVS có CRI 0,36 – < 0,53 (Cấp 2)
# ─────────────────────────────────────────────────────────────────────────────
GP_21 = {
    "id": "GP_21",
    "name": "Nhóm GP 2.1 — Đóng bãi cơ bản",
    "short_name": "GP 2.1",
    "applicable_to": ["BCL-HVS đạt chuẩn", "BCL-KHVS Cấp 2"],
    "cri_range": (0.36, 0.53),
    "description": (
        "Áp dụng cho BCL-HVS đã đạt tiêu chuẩn QCVN 96:2025 và BCL-KHVS có CRI "
        "từ 0,36 đến dưới 0,53 (rủi ro trung bình). "
        "Yêu cầu lớp phủ kỹ thuật cơ bản và hệ thống thoát nước."
    ),
    "mandatory_items": [
        "San gạt, tạo mái dốc ổn định (độ dốc mái ≤ 1:3, chiều cao mái ≤ 10 m)",
        "Lớp phủ kỹ thuật tối thiểu 3 lớp: lớp thoát nước, lớp cách ly (đất sét k ≤ 10⁻⁷ cm/s dày ≥ 0,5 m), lớp bảo vệ và trồng cây",
        "Hệ thống thoát nước mưa mái dốc và xung quanh bãi",
        "Hệ thống thoát khí bãi rác thụ động (ống thu khí đứng, khoảng cách 30–50 m)",
        "Trồng cây phủ xanh toàn bộ bề mặt",
        "Biển báo cảnh báo và hàng rào ngăn cách",
        "Quan trắc môi trường định kỳ",
    ],
    "optional_items": [
        "Xử lý nước rỉ rác nếu hệ thống thu gom còn tồn đọng",
        "Đo lún bề mặt định kỳ (đặc biệt với bãi chứa chất thải hữu cơ cao)",
    ],
    "monitoring_period": "Tối thiểu 10 năm sau khi hoàn thành đóng bãi",
    "estimated_cost_level": "Trung bình",
    "advantages": [
        "Kiểm soát được nước thấm và khí bãi rác ở mức cơ bản",
        "Chi phí hợp lý, áp dụng được cho nhiều loại bãi",
    ],
    "disadvantages": [
        "Không phù hợp nếu nước rỉ rác đang gây ô nhiễm nghiêm trọng",
        "Cần theo dõi lún bề mặt lâu dài",
    ],
    "legal_basis": "Điều 32, Thông tư 02/2022/TT-BTNMT; QCVN 96:2025/BNNMT",
}

# ─────────────────────────────────────────────────────────────────────────────
# NHÓM GIẢI PHÁP 2.2 — Đóng bãi tăng cường
# Áp dụng: BCL-HVS cần bổ sung thêm hạng mục để đạt QCVN 96:2025
#           BCL-KHVS có CRI 0,53 – < 0,69 (Cấp 3)
# ─────────────────────────────────────────────────────────────────────────────
GP_22 = {
    "id": "GP_22",
    "name": "Nhóm GP 2.2 — Đóng bãi tăng cường",
    "short_name": "GP 2.2",
    "applicable_to": ["BCL-HVS cần bổ sung", "BCL-KHVS Cấp 3"],
    "cri_range": (0.53, 0.69),
    "description": (
        "Áp dụng cho BCL-HVS chưa đạt đầy đủ yêu cầu kỹ thuật và BCL-KHVS có CRI "
        "từ 0,53 đến dưới 0,69 (rủi ro cao). "
        "Yêu cầu hệ thống thu gom và xử lý nước rỉ rác, kiểm soát khí tích cực."
    ),
    "mandatory_items": [
        "Tất cả hạng mục của GP 2.1",
        "Hệ thống thu gom và xử lý nước rỉ rác đạt QCVN 40:2025/BNNMT",
        "Hệ thống thu khí bãi rác chủ động (giếng thu khí, đường ống, đốt/thu hồi)",
        "Lớp phủ kỹ thuật tăng cường: thêm lớp màng địa kỹ thuật HDPE nếu cần",
        "Hệ thống quan trắc nước ngầm (giếng quan trắc thượng và hạ lưu)",
        "Kế hoạch ứng phó sự cố nước rỉ rác và khí bãi rác",
    ],
    "optional_items": [
        "Hàng rào cây xanh cách ly tạo vùng đệm",
        "Hệ thống thu hồi và phát điện từ khí bãi rác (nếu lượng khí đủ lớn)",
        "Gia cố mái dốc nếu có nguy cơ trượt lở",
    ],
    "monitoring_period": "Tối thiểu 15 năm sau khi hoàn thành đóng bãi",
    "estimated_cost_level": "Cao",
    "advantages": [
        "Kiểm soát toàn diện nước rỉ rác và khí bãi rác",
        "Phù hợp với bãi có ô nhiễm trung bình, vị trí gần khu dân cư",
    ],
    "disadvantages": [
        "Chi phí đầu tư và vận hành cao",
        "Yêu cầu nhân lực kỹ thuật vận hành hệ thống xử lý",
    ],
    "legal_basis": "Điều 32, Thông tư 02/2022/TT-BTNMT; QCVN 96:2025/BNNMT; QCVN 40:2025/BNNMT",
}

# ─────────────────────────────────────────────────────────────────────────────
# NHÓM GIẢI PHÁP 3 — Đóng bãi nâng cao (can thiệp toàn diện)
# Áp dụng: BCL-KHVS có CRI ≥ 0,69 (Cấp 4 — rủi ro rất cao)
# ─────────────────────────────────────────────────────────────────────────────
GP_3 = {
    "id": "GP_3",
    "name": "Nhóm GP 3 — Đóng bãi nâng cao / can thiệp toàn diện",
    "short_name": "GP 3",
    "applicable_to": ["BCL-KHVS Cấp 4"],
    "cri_range": (0.69, 1.01),
    "description": (
        "Áp dụng cho BCL-KHVS có CRI ≥ 0,69 (rủi ro rất cao), đặc biệt khi bãi "
        "gần khu dân cư đông, nguồn nước sinh hoạt hoặc hệ sinh thái nhạy cảm. "
        "Cần đánh giá chi tiết để lựa chọn phương án phù hợp: "
        "can thiệp tại chỗ nâng cao (GP 3a) hoặc đào chuyển/di dời (GP 3b)."
    ),
    "sub_options": [
        {
            "id": "GP_3a",
            "name": "GP 3a — Can thiệp tại chỗ nâng cao",
            "description": "Cải tạo toàn diện hệ thống thu gom, xử lý ô nhiễm tại chỗ",
            "items": [
                "Tất cả hạng mục của GP 2.2",
                "Khảo sát địa chất thủy văn chi tiết và mô hình hóa lan truyền ô nhiễm",
                "Rào chắn thấm (slurry wall, sheet pile) nếu cần ngăn nước rỉ rác",
                "Hệ thống bơm và xử lý nước ngầm bị ô nhiễm (pump-and-treat)",
                "Quan trắc nước ngầm tối thiểu 4 lần/năm",
            ],
        },
        {
            "id": "GP_3b",
            "name": "GP 3b — Đào chuyển/di dời chất thải",
            "description": "Di dời toàn bộ chất thải sang vị trí mới hoặc tái chế",
            "items": [
                "Khảo sát tổng thể đặc tính chất thải và nền đất",
                "Đào toàn bộ chất thải và phân loại (tái chế/xử lý/chôn lấp đúng quy định)",
                "Cải tạo nền đất sau khi di chuyển chất thải",
                "Xử lý nước rỉ rác và đất ô nhiễm còn lại tại chỗ",
            ],
        },
    ],
    "mandatory_items": [
        "Đánh giá rủi ro chi tiết trước khi quyết định phương án (GP 3a hay 3b)",
        "Lập báo cáo đánh giá tác động môi trường nếu can thiệp quy mô lớn",
        "Quan trắc liên tục trong suốt quá trình thi công",
        "Kế hoạch ứng phó sự cố khẩn cấp",
    ],
    "optional_items": [
        "Tái sử dụng khí bãi rác để phát điện",
        "Tái sử dụng đất sau đóng bãi cho mục đích phù hợp",
    ],
    "monitoring_period": "Tối thiểu 20 năm sau khi hoàn thành đóng bãi",
    "estimated_cost_level": "Rất cao",
    "advantages": [
        "Giải quyết triệt để nguy cơ ô nhiễm",
        "Phù hợp với vị trí nhạy cảm cao",
    ],
    "disadvantages": [
        "Chi phí rất cao, thời gian thi công dài",
        "Cần đơn vị tư vấn chuyên sâu và thiết bị chuyên dụng",
        "Rủi ro phát tán ô nhiễm trong quá trình thi công nếu không kiểm soát tốt",
    ],
    "legal_basis": "Điều 32, Thông tư 02/2022/TT-BTNMT; QCVN 96:2025/BNNMT; QCVN 40:2025/BNNMT",
}

# ─────────────────────────────────────────────────────────────────────────────
# MAPPING: Loại BCL + Cấp rủi ro → Giải pháp
# ─────────────────────────────────────────────────────────────────────────────
SOLUTION_MAPPING = {
    # BCL-HVS
    "HVS_DAT_CHUAN":   GP_21,
    "HVS_CAN_BO_SUNG": GP_22,
    # BCL-KHVS theo cấp CRI
    "KHVS_CAP_1": GP_1,
    "KHVS_CAP_2": GP_21,
    "KHVS_CAP_3": GP_22,
    "KHVS_CAP_4": GP_3,
}

ALL_SOLUTIONS = [GP_1, GP_21, GP_22, GP_3]
