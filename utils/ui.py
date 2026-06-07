# -*- coding: utf-8 -*-
"""Các thành phần giao diện dùng chung cho BCL-CRI Tool."""

from __future__ import annotations

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
BRANDING_EXTENSIONS = [".png", ".webp", ".jpg", ".jpeg", ".svg"]


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
    padding-top: 1.8rem;
    padding-bottom: 2rem;
  }
  .app-eyebrow {
    color: #52616b;
    font-size: 0.88rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0;
    margin-bottom: 0.25rem;
  }
  .app-page-title {
    color: #12344d;
    font-size: 1.85rem;
    font-weight: 700;
    line-height: 1.25;
    margin: 0 0 0.35rem 0;
  }
  .app-page-desc {
    color: #425466;
    font-size: 1rem;
    line-height: 1.55;
    margin-bottom: 1rem;
    max-width: 1120px;
  }
  .status-card {
    border: 1px solid #d8e1ea;
    border-radius: 8px;
    padding: 0.85rem 0.95rem;
    background: #ffffff;
  }
  .status-label {
    color: #52616b;
    font-size: 0.78rem;
    margin-bottom: 0.25rem;
  }
  .status-value {
    color: #12344d;
    font-size: 1.35rem;
    font-weight: 700;
  }
  .workflow-card {
    border: 1px solid #d8e1ea;
    border-left: 4px solid #1f77b4;
    border-radius: 8px;
    padding: 0.85rem 0.95rem;
    background: #f8fbfd;
    min-height: 128px;
  }
  .workflow-step {
    color: #1f77b4;
    font-size: 0.78rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
  }
  .workflow-title {
    color: #12344d;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
  }
  .workflow-desc {
    color: #425466;
    font-size: 0.84rem;
    line-height: 1.45;
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
