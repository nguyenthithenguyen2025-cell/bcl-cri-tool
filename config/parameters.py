# -*- coding: utf-8 -*-
"""
14 thông số CRI — trọng số và ngưỡng điểm.
Nguồn: Đề tài TNMT.2024.05.05, Trường ĐH Thủy Lợi (2026).

Lưu ý trọng số nhóm P:
  Trọng số gốc tài liệu: tổng = 1,01 (làm tròn).
  Trong tính toán, calculator.py tự động normalize về 1,00 bằng cách
  chia mỗi trọng số cho tổng thực tế (1,01).
"""

# ── Trọng số 3 nhóm (dùng làm số mũ trong CRI = H^0.28 × P^0.40 × R^0.32)
GROUP_EXPONENTS = {
    "H": 0.28,
    "P": 0.40,
    "R": 0.32,
}

# ── Màu cấp rủi ro
RISK_COLORS = {
    1: "#2ecc71",   # Xanh lá — rủi ro thấp
    2: "#f39c12",   # Vàng    — rủi ro trung bình
    3: "#e67e22",   # Cam     — rủi ro cao
    4: "#e74c3c",   # Đỏ      — rủi ro rất cao
}

RISK_LABELS = {
    1: "Cấp 1 — Rủi ro thấp",
    2: "Cấp 2 — Rủi ro trung bình",
    3: "Cấp 3 — Rủi ro cao",
    4: "Cấp 4 — Rủi ro rất cao",
}

# ── Ngưỡng CRI phân cấp rủi ro
CRI_THRESHOLDS = [
    (0.36, 1),   # CRI < 0.36  → Cấp 1
    (0.53, 2),   # 0.36 ≤ CRI < 0.53 → Cấp 2
    (0.69, 3),   # 0.53 ≤ CRI < 0.69 → Cấp 3
    (1.01, 4),   # CRI ≥ 0.69 → Cấp 4
]

# ── Điểm hợp lệ
VALID_SCORES = [0.25, 0.50, 0.75, 1.00]

# ─────────────────────────────────────────────────────────────────────────────
# ĐỊNH NGHĨA 14 THÔNG SỐ CRI
# Mỗi thông số gồm:
#   id            : mã thông số (chuỗi)
#   name          : tên tiếng Việt
#   group         : nhóm ("H", "P", "R")
#   weight        : trọng số trong nhóm (số thực, theo tài liệu gốc)
#   unit          : đơn vị đo (None nếu là mô tả)
#   input_type    : "numeric" (có ngưỡng số) hoặc "descriptive" (chọn mô tả)
#   options       : danh sách dict {label, score, hint}
#                   - label: nhãn hiển thị trên giao diện
#                   - score: điểm quy đổi (0.25/0.50/0.75/1.00)
#                   - hint : gợi ý thêm (có thể None)
#   tooltip       : giải thích ngắn gọn cho người dùng
# ─────────────────────────────────────────────────────────────────────────────

PARAMETERS = [
    # ════════════════════════════════════════════
    # NHÓM H — Nguồn nguy hại (trọng số nhóm: 0,28)
    # ════════════════════════════════════════════
    {
        "id": "H1",
        "name": "Thời gian ngừng tiếp nhận chất thải",
        "group": "H",
        "weight": 0.35,
        "unit": "năm",
        "input_type": "numeric",
        "options": [
            {"label": "> 20 năm",   "score": 0.25, "hint": "Bãi đã đóng lâu, rủi ro thấp"},
            {"label": "10 – 20 năm","score": 0.50, "hint": None},
            {"label": "5 – 10 năm", "score": 0.75, "hint": None},
            {"label": "< 5 năm",    "score": 1.00, "hint": "Bãi mới đóng hoặc đang hoạt động"},
        ],
        "tooltip": (
            "Tính từ năm bãi chính thức ngừng tiếp nhận chất thải đến thời điểm đánh giá. "
            "Bãi càng lâu đóng, khả năng phân hủy và ổn định hóa học càng cao."
        ),
    },
    {
        "id": "H2",
        "name": "Diện tích bãi chôn lấp",
        "group": "H",
        "weight": 0.32,
        "unit": "ha",
        "input_type": "numeric",
        "options": [
            {"label": "< 1 ha",  "score": 0.25, "hint": "Bãi nhỏ"},
            {"label": "1 – 3 ha","score": 0.50, "hint": None},
            {"label": "3 – 5 ha","score": 0.75, "hint": None},
            {"label": "> 5 ha",  "score": 1.00, "hint": "Bãi lớn, lượng chất thải nhiều"},
        ],
        "tooltip": (
            "Tổng diện tích khu vực chôn lấp (không tính hạ tầng phụ trợ). "
            "Diện tích càng lớn, khối lượng chất thải và lượng nước rỉ rác tiềm năng càng cao."
        ),
    },
    {
        "id": "H3",
        "name": "Thành phần chất thải nguy hại",
        "group": "H",
        "weight": 0.15,
        "unit": "%",
        "input_type": "numeric",
        "options": [
            {"label": "< 1%",   "score": 0.25, "hint": "Hầu như không có CTNH"},
            {"label": "1 – 2%", "score": 0.50, "hint": None},
            {"label": "2 – 5%", "score": 0.75, "hint": None},
            {"label": "> 5%",   "score": 1.00, "hint": "Chứa nhiều chất thải nguy hại"},
        ],
        "tooltip": (
            "Ước tính tỷ lệ % chất thải nguy hại (CTNH) trong tổng khối lượng chất thải đã chôn lấp. "
            "Nguồn ước tính: hồ sơ tiếp nhận chất thải hoặc khảo sát thực địa."
        ),
    },
    {
        "id": "H4",
        "name": "Lượng nước rỉ rác quan sát được",
        "group": "H",
        "weight": 0.18,
        "unit": None,
        "input_type": "descriptive",
        "options": [
            {
                "label": "Không có hoặc rất ít",
                "score": 0.25,
                "hint": "Bãi khô, không quan sát thấy nước rỉ rác",
            },
            {
                "label": "Ít, xuất hiện cục bộ",
                "score": 0.50,
                "hint": "Có nước rỉ rác nhưng chỉ ở một số vị trí, không chảy ra ngoài",
            },
            {
                "label": "Nhiều, lan rộng trong bãi",
                "score": 0.75,
                "hint": "Nước rỉ rác xuất hiện nhiều nơi, có dấu hiệu di chuyển",
            },
            {
                "label": "Rất nhiều, tràn ra ngoài bãi",
                "score": 1.00,
                "hint": "Nước rỉ rác chảy ra ngoài ranh giới bãi hoặc vào nguồn nước",
            },
        ],
        "tooltip": (
            "Đánh giá bằng quan sát thực địa hoặc hồ sơ vận hành. "
            "Nước rỉ rác chứa các chất ô nhiễm hữu cơ và vô cơ có thể gây ô nhiễm nguồn nước."
        ),
    },

    # ════════════════════════════════════════════
    # NHÓM P — Đường lan truyền (trọng số nhóm: 0,40)
    # Lưu ý: tổng trọng số trong nhóm = 1,01 (làm tròn trong tài liệu gốc)
    # → calculator.py tự động normalize về 1,00
    # ════════════════════════════════════════════
    {
        "id": "P1",
        "name": "Tình trạng lớp phủ bề mặt",
        "group": "P",
        "weight": 0.15,
        "unit": None,
        "input_type": "descriptive",
        "options": [
            {
                "label": "Lớp phủ kỹ thuật tốt, kín hoàn toàn",
                "score": 0.25,
                "hint": "Lớp phủ đạt tiêu chuẩn, không có vết nứt hoặc sụt lún",
            },
            {
                "label": "Lớp phủ cơ bản, còn một số điểm hở",
                "score": 0.50,
                "hint": "Có lớp phủ nhưng chưa kín hoàn toàn, còn một số kẽ hở nhỏ",
            },
            {
                "label": "Lớp phủ kém, nhiều kẽ hở hoặc bị xói mòn",
                "score": 0.75,
                "hint": "Lớp phủ xuống cấp, nước mưa có thể thấm vào bãi",
            },
            {
                "label": "Không có lớp phủ hoặc là bãi lộ thiên",
                "score": 1.00,
                "hint": "Bãi không có lớp phủ, chất thải tiếp xúc trực tiếp với môi trường",
            },
        ],
        "tooltip": (
            "Lớp phủ bề mặt (capping) ngăn nước mưa thấm vào khối rác, giảm phát sinh nước rỉ rác. "
            "Đánh giá bằng quan sát thực địa và kiểm tra hồ sơ công trình."
        ),
    },
    {
        "id": "P2",
        "name": "Lượng mưa trung bình năm",
        "group": "P",
        "weight": 0.12,
        "unit": "mm/năm",
        "input_type": "numeric",
        "options": [
            {"label": "< 1.000 mm/năm",          "score": 0.25, "hint": "Vùng khô hạn"},
            {"label": "1.000 – 1.400 mm/năm",    "score": 0.50, "hint": "Vùng mưa trung bình"},
            {"label": "1.400 – 2.400 mm/năm",    "score": 0.75, "hint": "Vùng mưa nhiều"},
            {"label": "> 2.400 mm/năm",           "score": 1.00, "hint": "Vùng mưa rất nhiều"},
        ],
        "tooltip": (
            "Lượng mưa trung bình năm tại vị trí bãi chôn lấp (số liệu trạm khí tượng gần nhất). "
            "Lượng mưa cao làm tăng lượng nước rỉ rác và nguy cơ ô nhiễm."
        ),
    },
    {
        "id": "P3",
        "name": "Đặc điểm địa chất khu vực bãi chôn lấp",
        "group": "P",
        "weight": 0.22,
        "unit": None,
        "input_type": "descriptive",
        "options": [
            {
                "label": "Sét dày, hệ số thấm rất thấp (k < 10⁻⁷ cm/s)",
                "score": 0.25,
                "hint": "Lớp sét tự nhiên dày ≥ 1 m, ngăn chặn tốt sự thấm",
            },
            {
                "label": "Á sét, hệ số thấm trung bình (10⁻⁷ – 10⁻⁵ cm/s)",
                "score": 0.50,
                "hint": "Đất pha sét, có khả năng thấm nhất định",
            },
            {
                "label": "Cát, cuội sỏi — thấm cao (k > 10⁻⁵ cm/s)",
                "score": 0.75,
                "hint": "Đất rời rạc, nước rỉ rác dễ dàng thấm xuống tầng ngầm",
            },
            {
                "label": "Đá vôi/karst hoặc đất nứt nẻ nhiều",
                "score": 1.00,
                "hint": "Địa chất karst hoặc đá nứt nẻ — nước rỉ rác lan nhanh không thể dự báo",
            },
        ],
        "tooltip": (
            "Đặc điểm địa chất nền bãi quyết định tốc độ và hướng lan truyền nước rỉ rác. "
            "Lấy từ hồ sơ khoan địa chất hoặc khảo sát thực địa."
        ),
    },
    {
        "id": "P4",
        "name": "Khoảng cách đến nguồn nước mặt gần nhất",
        "group": "P",
        "weight": 0.17,
        "unit": "m",
        "input_type": "numeric",
        "options": [
            {"label": "> 1.000 m",    "score": 0.25, "hint": "Xa nguồn nước mặt"},
            {"label": "500 – 1.000 m","score": 0.50, "hint": None},
            {"label": "100 – 500 m",  "score": 0.75, "hint": None},
            {"label": "< 100 m",      "score": 1.00, "hint": "Rất gần nguồn nước mặt"},
        ],
        "tooltip": (
            "Khoảng cách từ ranh giới bãi chôn lấp đến sông, suối, hồ hoặc kênh gần nhất. "
            "Đo theo đường thẳng trên bản đồ hoặc thực địa."
        ),
    },
    {
        "id": "P5",
        "name": "Khoảng cách đến mực nước ngầm",
        "group": "P",
        "weight": 0.23,
        "unit": "m",
        "input_type": "numeric",
        "options": [
            {"label": "> 20 m",   "score": 0.25, "hint": "Mực nước ngầm sâu, ít nguy cơ"},
            {"label": "15 – 20 m","score": 0.50, "hint": None},
            {"label": "5 – 15 m", "score": 0.75, "hint": None},
            {"label": "< 5 m",    "score": 1.00, "hint": "Mực nước ngầm rất nông, rủi ro cao"},
        ],
        "tooltip": (
            "Độ sâu từ đáy bãi chôn lấp đến mực nước ngầm mùa mưa (trường hợp bất lợi nhất). "
            "Lấy từ tài liệu địa chất thủy văn hoặc quan trắc giếng."
        ),
    },
    {
        "id": "P6",
        "name": "Độ dốc địa hình khu vực bãi chôn lấp",
        "group": "P",
        "weight": 0.12,
        "unit": "%",
        "input_type": "numeric",
        "options": [
            {"label": "< 5%",    "score": 0.25, "hint": "Địa hình bằng phẳng"},
            {"label": "5 – 15%", "score": 0.50, "hint": "Địa hình dốc nhẹ"},
            {"label": "15 – 30%","score": 0.75, "hint": "Địa hình dốc trung bình"},
            {"label": "> 30%",   "score": 1.00, "hint": "Địa hình dốc cao — dễ xói lở"},
        ],
        "tooltip": (
            "Độ dốc trung bình của địa hình xung quanh bãi. "
            "Dốc cao làm tăng tốc độ chảy tràn và nguy cơ xói lở."
        ),
    },

    # ════════════════════════════════════════════
    # NHÓM R — Đối tượng tiếp nhận (trọng số nhóm: 0,32)
    # ════════════════════════════════════════════
    {
        "id": "R1",
        "name": "Mục đích sử dụng nguồn nước mặt và nước ngầm",
        "group": "R",
        "weight": 0.39,
        "unit": None,
        "input_type": "descriptive",
        "options": [
            {
                "label": "Không sử dụng hoặc chỉ dùng cho công nghiệp không nhạy cảm",
                "score": 0.25,
                "hint": "Không có dân cư hoặc nông nghiệp sử dụng nguồn nước này",
            },
            {
                "label": "Sản xuất nông nghiệp, nuôi trồng thủy sản",
                "score": 0.50,
                "hint": "Nước được dùng tưới tiêu hoặc nuôi cá",
            },
            {
                "label": "Sinh hoạt có qua xử lý nước",
                "score": 0.75,
                "hint": "Nước dùng cho ăn uống nhưng đã qua hệ thống lọc/xử lý",
            },
            {
                "label": "Sinh hoạt trực tiếp, không qua xử lý",
                "score": 1.00,
                "hint": "Dân cư dùng nước giếng hoặc suối trực tiếp không qua xử lý",
            },
        ],
        "tooltip": (
            "Đánh giá mức độ phụ thuộc của cộng đồng vào nguồn nước có nguy cơ bị ảnh hưởng. "
            "Thông tin lấy từ khảo sát hộ dân hoặc số liệu cấp nước địa phương."
        ),
    },
    {
        "id": "R2",
        "name": "Số người sống trong phạm vi 1.000 m quanh bãi chôn lấp",
        "group": "R",
        "weight": 0.24,
        "unit": "người",
        "input_type": "numeric",
        "options": [
            {"label": "< 4 người",       "score": 0.25, "hint": "Hầu như không có dân cư"},
            {"label": "4 – 100 người",   "score": 0.50, "hint": "Dân cư thưa thớt"},
            {"label": "100 – 500 người", "score": 0.75, "hint": "Dân cư trung bình"},
            {"label": "> 500 người",     "score": 1.00, "hint": "Khu vực đông dân"},
        ],
        "tooltip": (
            "Ước tính số dân sinh sống trong bán kính 1.000 m tính từ ranh giới bãi chôn lấp. "
            "Lấy từ số liệu thống kê dân số xã/phường hoặc ảnh vệ tinh."
        ),
    },
    {
        "id": "R3",
        "name": "Tỷ lệ khiếu nại/phản ánh của cộng đồng",
        "group": "R",
        "weight": 0.20,
        "unit": "%",
        "input_type": "numeric",
        "options": [
            {"label": "< 5%",    "score": 0.25, "hint": "Cộng đồng ít phản ánh"},
            {"label": "5 – 15%", "score": 0.50, "hint": None},
            {"label": "15 – 30%","score": 0.75, "hint": None},
            {"label": "> 30%",   "score": 1.00, "hint": "Cộng đồng phản ánh nhiều, bức xúc cao"},
        ],
        "tooltip": (
            "Tỷ lệ % hộ dân trong vùng ảnh hưởng (1.000 m) có khiếu nại hoặc phản ánh về "
            "ô nhiễm từ bãi chôn lấp trong 12 tháng gần nhất."
        ),
    },
    {
        "id": "R4",
        "name": "Khoảng cách đến hệ sinh thái cần bảo vệ gần nhất",
        "group": "R",
        "weight": 0.17,
        "unit": "m",
        "input_type": "numeric",
        "options": [
            {"label": "> 1.000 m",   "score": 0.25, "hint": "Xa khu bảo tồn, vùng đất ngập nước"},
            {"label": "250 – 1.000 m","score": 0.50, "hint": None},
            {"label": "50 – 250 m",  "score": 0.75, "hint": None},
            {"label": "< 50 m",      "score": 1.00, "hint": "Rất gần khu sinh thái nhạy cảm"},
        ],
        "tooltip": (
            "Khoảng cách đến khu bảo tồn thiên nhiên, vùng đất ngập nước, rừng đặc dụng "
            "hoặc hệ sinh thái nhạy cảm gần nhất (đo theo đường thẳng)."
        ),
    },
]


# ── Tra cứu nhanh theo id
PARAM_BY_ID: dict = {p["id"]: p for p in PARAMETERS}

# ── Danh sách id theo nhóm
PARAMS_BY_GROUP: dict = {
    "H": [p["id"] for p in PARAMETERS if p["group"] == "H"],
    "P": [p["id"] for p in PARAMETERS if p["group"] == "P"],
    "R": [p["id"] for p in PARAMETERS if p["group"] == "R"],
}
