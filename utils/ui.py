# -*- coding: utf-8 -*-
"""Các thành phần giao diện dùng chung cho BCL-CRI Tool."""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

from utils.session import get_all_bcl


APP_NAME = "Công cụ hỗ trợ lựa chọn giải pháp đóng bãi chôn lấp CTRSH"
APP_SHORT_NAME = "BCL-CRI Tool"
APP_VERSION = "1.1"
PROJECT_NAME = "Đề tài TNMT.2024.05.05"
HOST_ORG = "Trường Đại học Thủy Lợi"
COOPERATING_ORG = "Cơ quan phối hợp"

ROOT_DIR = Path(__file__).resolve().parents[1]
BRANDING_DIR = ROOT_DIR / "assets" / "branding"
BRANDING_LOGOS = [
    {
        "label": "Đơn vị chủ trì",
        "stem": "logo_don_vi_chu_tri",
    },
    {
        "label": "Đề tài",
        "stem": "logo_de_tai",
    },
    {
        "label": "Cơ quan phối hợp",
        "stem": "logo_co_quan_phoi_hop",
    },
]
BRANDING_EXTENSIONS = [".webp", ".png", ".jpg", ".jpeg", ".svg"]


WORKFLOW_STEPS = [
    ("01", "Khai báo BCL", "Thông tin định danh, vị trí, quy mô và loại hình bãi chôn lấp."),
    ("02", "Phân loại BCL", "Xác định BCL-HVS hoặc BCL-KHVS để chọn nhánh đánh giá phù hợp."),
    ("03", "Đánh giá CRI", "Nhập 14 thông số thuộc nhóm H, P và R; xử lý dữ liệu thiếu theo nguyên tắc thận trọng."),
    ("04", "Kết quả và giải pháp", "Tính H/P/R/CRI, phân loại rủi ro và khuyến nghị nhóm giải pháp đóng bãi."),
    ("05", "Xuất hồ sơ", "Xuất Word, HTML/PDF, Excel và lưu/tải phiên làm việc dạng JSON."),
]


def apply_global_styles() -> None:
    """Áp dụng CSS nhẹ để giao diện nhất quán và trang trọng hơn."""
    st.markdown(
        """
<style>
  #MainMenu {visibility: hidden;}
  footer {visibility: hidden;}
  .block-container {
    padding-top: 0.75rem;
    padding-bottom: 2rem;
  }
  .app-eyebrow {
    color: #3d5166;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.2rem;
  }
  .app-page-title {
    color: #0d2e45;
    font-size: 1.75rem;
    font-weight: 700;
    line-height: 1.25;
    margin: 0 0 0.35rem 0;
  }
  .app-page-desc {
    color: #2c3e52;
    font-size: 0.97rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    max-width: 1120px;
  }
  .status-card {
    border: 1px solid #c8d6e2;
    border-top: 3px solid #1a4a6e;
    border-radius: 8px;
    padding: 0.85rem 0.95rem;
    background: #ffffff;
    box-shadow: 0 1px 4px rgba(13,46,69,0.07);
  }
  .status-label {
    color: #3d5166;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }
  .status-value {
    color: #0d2e45;
    font-size: 1.4rem;
    font-weight: 700;
  }
  .workflow-card {
    border: 1px solid #c8d6e2;
    border-left: 4px solid #1a4a6e;
    border-radius: 8px;
    padding: 0.85rem 0.95rem;
    background: #f4f8fc;
    min-height: 128px;
    box-shadow: 0 1px 4px rgba(13,46,69,0.06);
  }
  .workflow-step {
    color: #1a4a6e;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.3rem;
  }
  .workflow-title {
    color: #0d2e45;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
  }
  .workflow-desc {
    color: #2c3e52;
    font-size: 0.83rem;
    line-height: 1.5;
  }
</style>
""",
        unsafe_allow_html=True,
    )


def render_page_header(title: str, description: str, section: str | None = None) -> None:
    """Hiển thị tiêu đề trang theo định dạng thống nhất."""
    if section:
        st.markdown(f"<div class='app-eyebrow'>{section}</div>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='app-page-title'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='app-page-desc'>{description}</div>", unsafe_allow_html=True)


def get_available_branding_logos() -> list[dict]:
    """Trả về các logo nhận diện đã có trên filesystem."""
    available = []
    for logo in BRANDING_LOGOS:
        for ext in BRANDING_EXTENSIONS:
            path = BRANDING_DIR / f"{logo['stem']}{ext}"
            if path.exists():
                available.append({"label": logo["label"], "path": path})
                break
    return available


def _img_to_base64(path: Path) -> tuple[str, str]:
    """Trả về (data_uri_prefix, base64_string) cho file ảnh."""
    ext = path.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "webp": "image/webp", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
    data = base64.b64encode(path.read_bytes()).decode()
    return mime, data


def render_branding_banner() -> None:
    """Hiển thị banner nhận diện chuyên nghiệp ở đầu trang."""
    logos = get_available_branding_logos()
    logo_html = ""
    if logos:
        mime, data = _img_to_base64(logos[0]["path"])
        logo_html = (
            f'<img src="data:{mime};base64,{data}" '
            'style="height:80px;max-width:220px;object-fit:contain;'
            'display:block;filter:brightness(0) invert(1);" alt="Logo"/>'
        )

    st.markdown(
        f"""
<div style="
    background:linear-gradient(135deg,#0d2e45 0%,#1a4d72 100%);
    border-radius:10px;
    padding:1rem 1.5rem;
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:1rem;
    margin-bottom:1.5rem;
    box-shadow:0 3px 12px rgba(13,46,69,0.28);
">
  <div style="min-width:0;display:flex;align-items:center;gap:0.85rem;">
    {logo_html}
    <div style="color:rgba(255,255,255,0.72);font-size:0.80rem;">{PROJECT_NAME}</div>
  </div>
  <div style="text-align:right;flex-shrink:0;padding-left:1rem;border-left:1px solid rgba(255,255,255,0.2);">
    <div style="color:rgba(255,255,255,0.62);font-size:0.67rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.1rem;">Công cụ hỗ trợ</div>
    <div style="color:#ffffff;font-size:1.0rem;font-weight:700;">{APP_SHORT_NAME}</div>
    <div style="color:rgba(255,255,255,0.62);font-size:0.75rem;margin-top:0.12rem;">Phiên bản {APP_VERSION}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_page_footer() -> None:
    """Hiển thị footer pháp lý và phiên bản ở cuối mỗi trang."""
    st.markdown(
        f"""
<div style="
    margin-top:2.5rem;
    padding:0.65rem 1rem;
    border-top:2px solid #c8d6e2;
    display:flex;
    justify-content:space-between;
    align-items:center;
    flex-wrap:wrap;
    gap:0.4rem;
    background:#f4f8fc;
    border-radius:0 0 8px 8px;
">
  <div style="color:#5a7085;font-size:0.73rem;line-height:1.5;">
    Căn cứ pháp lý: Điều 32 TT 02/2022/TT-BTNMT &nbsp;·&nbsp; QCVN 96:2025/BNNMT &nbsp;·&nbsp; TCVN 13766:2023
  </div>
  <div style="color:#5a7085;font-size:0.73rem;text-align:right;">
    {APP_SHORT_NAME} v{APP_VERSION} &nbsp;·&nbsp; 2026
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def get_portfolio_status() -> dict[str, int]:
    """Tổng hợp trạng thái danh sách BCL đang có trong phiên làm việc."""
    entries = get_all_bcl()
    total = len(entries)
    hvs = 0
    khvs_done = 0
    khvs_pending = 0

    for entry in entries:
        info = entry.get("info", {})
        result = entry.get("result", {})
        if info.get("loai_bcl") == "HVS":
            hvs += 1
        elif result.get("CRI") is not None:
            khvs_done += 1
        else:
            khvs_pending += 1

    return {
        "total": total,
        "hvs": hvs,
        "khvs_done": khvs_done,
        "khvs_pending": khvs_pending,
    }


def render_status_summary() -> None:
    """Hiển thị tóm tắt trạng thái hồ sơ đang xử lý."""
    status = get_portfolio_status()
    cols = st.columns(4)
    items = [
        ("Tổng số BCL", status["total"]),
        ("BCL-KHVS đã tính CRI", status["khvs_done"]),
        ("BCL-KHVS chưa tính CRI", status["khvs_pending"]),
        ("BCL-HVS", status["hvs"]),
    ]
    for col, (label, value) in zip(cols, items):
        with col:
            st.markdown(
                f"""
<div class="status-card">
  <div class="status-label">{label}</div>
  <div class="status-value">{value}</div>
</div>
""",
                unsafe_allow_html=True,
            )


def render_workflow_overview() -> None:
    """Hiển thị quy trình 5 bước ở dạng thẻ chuyên nghiệp."""
    cols = st.columns(5)
    for col, (number, title, desc) in zip(cols, WORKFLOW_STEPS):
        with col:
            st.markdown(
                f"""
<div class="workflow-card">
  <div class="workflow-step">Bước {number}</div>
  <div class="workflow-title">{title}</div>
  <div class="workflow-desc">{desc}</div>
</div>
""",
                unsafe_allow_html=True,
            )
