# -*- coding: utf-8 -*-
"""
Xuất báo cáo kỹ thuật BCL-CRI ra file HTML (in thành PDF qua trình duyệt).
Không cần thư viện bên ngoài ngoài thư viện chuẩn.
"""

from datetime import date
from config.parameters import PARAMETERS
from core.classifier import generate_technical_analysis

RISK_COLORS_HEX = {
    1: "#2ecc71",
    2: "#f39c12",
    3: "#e67e22",
    4: "#e74c3c",
}

RISK_LABELS = {
    1: "Cấp 1 — Rủi ro thấp",
    2: "Cấp 2 — Rủi ro trung bình",
    3: "Cấp 3 — Rủi ro cao",
    4: "Cấp 4 — Rủi ro rất cao",
}


def _fmt(val, decimals=4) -> str:
    if val is None:
        return "—"
    if isinstance(val, float):
        return f"{val:.{decimals}f}".replace(".", ",")
    return str(val)


def export_to_html(
    entry: dict,
    include_solution: bool = True,
    include_legal: bool = True,
    report_meta: dict | None = None,
) -> bytes:
    """
    Tạo báo cáo kỹ thuật dạng HTML cho một BCL.
    Người dùng mở file trong trình duyệt và in (Ctrl+P → Save as PDF).

    Returns:
        bytes — nội dung file HTML đã encode UTF-8.
    """
    info = entry.get("info", {})
    result = entry.get("result", {})
    scores = entry.get("scores", {})
    missing_notes = entry.get("missing_notes", {})
    risk = result.get("risk", {})
    solution = result.get("solution", {})
    assumed_max = result.get("assumed_max", [])
    analysis = generate_technical_analysis(entry)
    report_meta = report_meta or {}

    ten_bcl = info.get("ten_bcl", "Bãi chôn lấp")
    tinh = info.get("tinh", "")
    lv = risk.get("level")
    risk_color = RISK_COLORS_HEX.get(lv, "#888")
    risk_label = risk.get("label", "")
    cri_val = result.get("CRI")
    today = date.today().strftime("%d/%m/%Y")
    report_date = report_meta.get("ngay_bao_cao") or today
    org = report_meta.get("don_vi_thuc_hien") or "—"
    evaluator = report_meta.get("nguoi_lap") or "—"
    reviewer = report_meta.get("nguoi_kiem_tra") or "—"

    # ── CSS
    css = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    color: #111;
    background: #fff;
    margin: 0;
    padding: 0;
}
.page {
    width: 210mm;
    min-height: 297mm;
    margin: 0 auto;
    padding: 20mm 20mm 20mm 25mm;
}
h1 { font-size: 14pt; color: #1f77b4; margin: 14px 0 6px; border-bottom: 1.5px solid #1f77b4; padding-bottom: 3px; }
h2 { font-size: 12pt; color: #1f77b4; margin: 10px 0 4px; }
p { margin: 5px 0; line-height: 1.55; }
table { width: 100%; border-collapse: collapse; margin: 8px 0; font-size: 11pt; }
th, td { border: 1px solid #999; padding: 5px 8px; vertical-align: top; }
th { background: #dde8f5; font-weight: bold; text-align: left; }
.title-block { text-align: center; margin-bottom: 16px; }
.title-block h0 { font-size: 14pt; font-weight: bold; color: #1f77b4; line-height: 1.4; }
.title-block .sub { font-size: 11pt; margin-top: 4px; }
.cover {
    min-height: 250mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
}
.cover-title { text-align: center; margin-top: 28mm; }
.cover-title .main { font-size: 17pt; color: #1f77b4; font-weight: bold; margin-bottom: 8px; }
.cover-title .submain { font-size: 13pt; font-weight: bold; line-height: 1.45; }
.cover-meta { width: 82%; margin: 28px auto 0; }
.risk-badge {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 13pt;
    color: #fff;
    margin: 8px 0;
}
.assumed { font-style: italic; color: #c0392b; }
.footer { margin-top: 20px; font-size: 9pt; color: #666; border-top: 1px solid #ccc; padding-top: 6px; font-style: italic; }
ul { margin: 4px 0 4px 18px; }
ul li { margin: 3px 0; }
@media print {
    body { margin: 0; }
    .page { width: 100%; padding: 15mm 15mm 15mm 20mm; }
    .no-print { display: none; }
}
.print-btn {
    position: fixed; top: 16px; right: 16px;
    background: #1f77b4; color: #fff;
    border: none; border-radius: 6px;
    padding: 10px 22px; font-size: 12pt; cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,.25);
}
.print-btn:hover { background: #1560a0; }
"""

    # ── Phần thông tin BCL
    loai_bcl_str = (
        "Không hợp vệ sinh (BCL-KHVS)"
        if info.get("loai_bcl") == "KHVS"
        else "Hợp vệ sinh (BCL-HVS)"
    )

    info_rows = ""
    for label, val in [
        ("Tên bãi chôn lấp", info.get("ten_bcl")),
        ("Tỉnh / Thành phố", info.get("tinh")),
        ("Xã / Phường", info.get("xa")),
        ("Vĩ độ", info.get("toa_do_lat")),
        ("Kinh độ", info.get("toa_do_lon")),
        ("Loại BCL", loai_bcl_str),
        ("Diện tích (ha)", _fmt(info.get("dien_tich_ha"), 2)),
        ("Thể tích ước tính (m³)", _fmt(info.get("the_tich_m3"), 0)),
        ("Chiều cao ước tính (m)", _fmt(info.get("chieu_cao_m"), 1)),
        ("Năm bắt đầu hoạt động", info.get("nam_bat_dau")),
        ("Năm ngừng tiếp nhận", info.get("nam_ngung")),
        ("Ghi chú", info.get("ghi_chu") or "—"),
    ]:
        info_rows += f"<tr><td style='font-weight:bold; width:40%;'>{label}</td><td>{val or '—'}</td></tr>\n"

    # ── Phần kết quả CRI
    cri_section = ""
    if info.get("loai_bcl") == "KHVS":
        cri_display = _fmt(cri_val)
        sol_name = solution.get("short_name", "") if solution else ""

        group_rows = ""
        for grp, val, desc, exp in [
            ("H — Nguồn nguy hại", result.get("H"), "Đặc tính nguồn ô nhiễm", "0,28"),
            ("P — Đường lan truyền", result.get("P"), "Khả năng di chuyển ô nhiễm", "0,40"),
            ("R — Đối tượng tiếp nhận", result.get("R"), "Mức độ nhạy cảm của đối tượng", "0,32"),
            ("CRI tổng hợp", cri_val, "H^0,28 × P^0,40 × R^0,32", "—"),
        ]:
            bold = "font-weight:bold;" if grp == "CRI tổng hợp" else ""
            group_rows += (
                f"<tr style='{bold}'>"
                f"<td>{grp}</td><td>{_fmt(val)}</td><td>{desc}</td><td>{exp}</td>"
                "</tr>\n"
            )

        score_rows = ""
        for p in PARAMETERS:
            pid = p["id"]
            score = scores.get(pid)
            is_assumed = pid in assumed_max
            score_str = _fmt(score, 2) if score is not None else "1,00"
            cls = " class='assumed'" if is_assumed else ""
            note = " (*)" if is_assumed else ""
            score_rows += (
                f"<tr><td>{pid}</td>"
                f"<td{cls}>{p['name']}{note}</td>"
                f"<td>{p['group']}</td>"
                f"<td style='text-align:center;'>{score_str}</td>"
                f"<td>{missing_notes.get(pid, '—') if is_assumed else '—'}</td></tr>\n"
            )

        cri_section = f"""
<h1>2. Kết quả tính toán Chỉ số Rủi ro Tổng hợp (CRI)</h1>
<p>
  <span class="risk-badge" style="background:{risk_color};">
    CRI = {cri_display} &nbsp;|&nbsp; {risk_label}
  </span>
</p>
<p>Giải pháp khuyến nghị: <strong>{sol_name}</strong></p>

<h2>2.1. Chỉ số từng nhóm</h2>
<table>
  <tr><th>Nhóm</th><th>Chỉ số</th><th>Mô tả</th><th>Trọng số nhóm</th></tr>
  {group_rows}
</table>

<h2>2.2. Điểm 14 thông số CRI</h2>
<table>
  <tr><th>Mã</th><th>Tên thông số</th><th>Nhóm</th><th>Điểm</th><th>Lý do thiếu dữ liệu</th></tr>
  {score_rows}
</table>
<p class="assumed">(*) Thông số được gán điểm 1,00 do thiếu dữ liệu (nguyên tắc thận trọng).</p>
"""

    # ── Phần giải pháp
    analysis_section = ""
    if info.get("loai_bcl") == "KHVS" and result.get("CRI") is not None:
        group_items = "".join(
            f"<li><strong>{item['group']} — {item['name']}:</strong> {item['comment']}</li>"
            for item in analysis.get("group_comments", [])
        )
        top_items = "".join(
            f"<li><strong>{item['id']} — {item['name']}:</strong> điểm {item['score']}, "
            f"đóng góp {item['contribution']:.4f}</li>"
            for item in analysis.get("top_risks", [])[:5]
        )
        action_items = "".join(
            f"<li>{item}</li>"
            for item in analysis.get("recommended_actions", [])
        )
        data_items = "".join(
            f"<li>{item}</li>"
            for item in analysis.get("data_quality_notes", [])
        )
        analysis_section = f"""
<h1>3. Phân tích chuyên môn</h1>
<p>{analysis.get("summary", "")}</p>
<h2>3.1. Nhận xét theo nhóm H/P/R</h2>
<ul>{group_items}</ul>
{f'<p><strong>{analysis.get("dominant_group")}</strong></p>' if analysis.get("dominant_group") else ''}
<h2>3.2. Thông số chi phối rủi ro</h2>
<ul>{top_items}</ul>
{f'<h2>3.3. Chất lượng dữ liệu</h2><ul>{data_items}</ul>' if data_items else ''}
<h2>3.4. Khuyến nghị kỹ thuật tiếp theo</h2>
<ul>{action_items}</ul>
"""

    # ── Phần giải pháp
    solution_section = ""
    if include_solution and solution:
        mandatory = "".join(f"<li>{item}</li>" for item in solution.get("mandatory_items", []))
        optional = "".join(f"<li>{item}</li>" for item in solution.get("optional_items", []))
        monitoring = solution.get("monitoring_period", "—")
        solution_section = f"""
<h1>4. Giải pháp đóng bãi khuyến nghị</h1>
<p><strong>{solution.get("name", "")}</strong></p>
<p>{solution.get("description", "")}</p>

<h2>4.1. Hạng mục bắt buộc</h2>
<ul>{mandatory}</ul>

<h2>4.2. Hạng mục khuyến nghị thêm</h2>
<ul>{optional}</ul>

<h2>4.3. Thời gian quản lý sau đóng bãi</h2>
<p>{monitoring}</p>
"""

    # ── Phần pháp lý
    legal_section = ""
    if include_legal:
        legal_basis = solution.get("legal_basis", "") if solution else ""
        legal_section = f"""
<h1>5. Căn cứ pháp lý</h1>
<ul>
  <li>Điều 32, Thông tư 02/2022/TT-BTNMT ngày 10/01/2022 của Bộ Tài nguyên và Môi trường</li>
  <li>QCVN 96:2025/BNNMT — Quy chuẩn kỹ thuật quốc gia về bãi chôn lấp chất thải rắn</li>
  <li>TCVN 13766:2023 — Chất thải rắn — Bãi chôn lấp hợp vệ sinh — Yêu cầu thiết kế</li>
  <li>Đề tài TNMT.2024.05.05 — Trường Đại học Thủy Lợi (2026) — Phương pháp CRI</li>
</ul>
{f'<p>Căn cứ áp dụng cho giải pháp: {legal_basis}</p>' if legal_basis else ''}
"""

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Báo cáo CRI — {ten_bcl}</title>
  <style>{css}</style>
</head>
<body>
<button class="print-btn no-print" onclick="window.print()">🖨️ In / Lưu PDF</button>

<div class="page">

  <div class="cover">
    <div>
      <div style="text-align:center; font-weight:bold;">{org.upper() if org != '—' else 'ĐƠN VỊ THỰC HIỆN'}</div>
      <div class="cover-title">
        <div class="main">BÁO CÁO KỸ THUẬT</div>
        <div class="submain">ĐÁNH GIÁ RỦI RO VÀ LỰA CHỌN GIẢI PHÁP CAN THIỆP, ĐÓNG BÃI CHÔN LẤP CTRSH</div>
        <div style="margin-top:18px; font-size:13pt; font-weight:bold;">{ten_bcl}</div>
      </div>
      <table class="cover-meta">
        <tr><td style="font-weight:bold; width:38%;">Tỉnh/Thành phố</td><td>{tinh or '—'}</td></tr>
        <tr><td style="font-weight:bold;">Xã/Phường</td><td>{info.get('xa') or '—'}</td></tr>
        <tr><td style="font-weight:bold;">Đơn vị thực hiện</td><td>{org}</td></tr>
        <tr><td style="font-weight:bold;">Người lập</td><td>{evaluator}</td></tr>
        <tr><td style="font-weight:bold;">Người kiểm tra</td><td>{reviewer}</td></tr>
        <tr><td style="font-weight:bold;">Ngày lập báo cáo</td><td>{report_date}</td></tr>
      </table>
    </div>
    <div style="text-align:center; font-style:italic; font-size:10pt;">
      Báo cáo được tạo từ Công cụ hỗ trợ lựa chọn giải pháp đóng bãi chôn lấp CTRSH.
    </div>
  </div>

  <div class="title-block">
    <div class="h0" style="font-size:14pt; font-weight:bold; color:#1f77b4; line-height:1.4;">
      BÁO CÁO ĐÁNH GIÁ RỦI RO VÀ GIẢI PHÁP ĐÓNG BÃI CHÔN LẤP
    </div>
    <div class="sub">Chỉ số Rủi ro Tổng hợp (CRI) — Đề tài TNMT.2024.05.05</div>
    <div class="sub" style="margin-top:4px; font-style:italic;">Ngày lập báo cáo: {report_date}</div>
  </div>

  <h1>Thông tin báo cáo</h1>
  <table>
    <tr><td style="font-weight:bold; width:40%;">Đơn vị thực hiện</td><td>{org}</td></tr>
    <tr><td style="font-weight:bold;">Người lập</td><td>{evaluator}</td></tr>
    <tr><td style="font-weight:bold;">Người kiểm tra</td><td>{reviewer}</td></tr>
    <tr><td style="font-weight:bold;">Ngày lập báo cáo</td><td>{report_date}</td></tr>
  </table>

  <h1>1. Thông tin bãi chôn lấp</h1>
  <table>
    {info_rows}
  </table>

  {cri_section}
  {analysis_section}
  {solution_section}
  {legal_section}

  <div class="footer">
    Báo cáo được tạo tự động bởi Công cụ hỗ trợ lựa chọn giải pháp đóng bãi chôn lấp CTRSH — {report_date}.<br>
    Kết quả mang tính hỗ trợ quyết định, không thay thế đánh giá kỹ thuật chuyên ngành.
  </div>

</div>
</body>
</html>"""

    return html.encode("utf-8")
