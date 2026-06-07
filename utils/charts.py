# -*- coding: utf-8 -*-
"""
Tạo các biểu đồ Plotly cho ứng dụng BCL-CRI.
Tất cả hàm trả về plotly.graph_objects.Figure hoặc None nếu thiếu dữ liệu.
"""

import math
import plotly.graph_objects as go
import plotly.express as px
from config.parameters import PARAMETERS, PARAM_BY_ID, RISK_COLORS

# Màu cấp rủi ro (chuỗi hex không có #)
_COLORS = {k: v for k, v in RISK_COLORS.items()}


def _risk_color(level: int) -> str:
    return _COLORS.get(level, "#95a5a6")


def radar_chart(scores: dict[str, float]) -> go.Figure | None:
    """
    Biểu đồ radar 14 thông số CRI.
    """
    params = PARAMETERS
    if not scores or not params:
        return None

    labels = [f"{p['id']}\n{p['name'][:15]}..." if len(p['name']) > 15 else f"{p['id']}\n{p['name']}" for p in params]
    values = [scores.get(p["id"]) or 1.00 for p in params]

    # Đóng vòng
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    # Màu theo nhóm
    group_colors = {"H": "#e74c3c", "P": "#f39c12", "R": "#2980b9"}
    line_color = "#e74c3c"  # màu chính

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(231,76,60,0.15)",
        line=dict(color=line_color, width=2),
        name="Điểm CRI",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1.1], tickvals=[0.25, 0.5, 0.75, 1.0]),
        ),
        showlegend=False,
        height=420,
        margin=dict(t=30, b=30, l=60, r=60),
        paper_bgcolor="white",
    )
    return fig


def gauge_chart(cri: float, risk_level: int) -> go.Figure | None:
    """
    Đồng hồ đo CRI (0,25 – 1,00).
    """
    if cri is None:
        return None

    color = _risk_color(risk_level)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cri,
        number={"suffix": "", "font": {"size": 36}},
        title={"text": "CRI", "font": {"size": 18}},
        gauge={
            "axis": {"range": [0.25, 1.00], "tickwidth": 1},
            "bar": {"color": color},
            "steps": [
                {"range": [0.25, 0.36], "color": RISK_COLORS[1]},
                {"range": [0.36, 0.53], "color": RISK_COLORS[2]},
                {"range": [0.53, 0.69], "color": RISK_COLORS[3]},
                {"range": [0.69, 1.00], "color": RISK_COLORS[4]},
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.85,
                "value": cri,
            },
        },
    ))
    fig.update_layout(height=300, margin=dict(t=30, b=10, l=20, r=20), paper_bgcolor="white")
    return fig


def bar_group_chart(H: float, P: float, R: float) -> go.Figure | None:
    """
    Bar chart so sánh chỉ số H, P, R với đường ngưỡng phân cấp.
    """
    if H is None or P is None or R is None:
        return None

    fig = go.Figure()
    groups = ["H (Nguồn)", "P (Đường)", "R (Đối tượng)"]
    values = [H, P, R]
    colors = ["#e74c3c", "#f39c12", "#2980b9"]

    fig.add_trace(go.Bar(
        x=groups,
        y=values,
        marker_color=colors,
        text=[f"{v:.4f}" for v in values],
        textposition="outside",
        name="Chỉ số nhóm",
    ))

    # Đường ngưỡng
    for threshold, label, color in [
        (0.36, "Cấp 1/2", RISK_COLORS[2]),
        (0.53, "Cấp 2/3", RISK_COLORS[3]),
        (0.69, "Cấp 3/4", RISK_COLORS[4]),
    ]:
        fig.add_hline(
            y=threshold,
            line_dash="dot",
            line_color=color,
            annotation_text=label,
            annotation_position="right",
        )

    fig.update_layout(
        yaxis=dict(range=[0, 1.1], title="Giá trị"),
        height=320,
        showlegend=False,
        margin=dict(t=20, b=30, l=40, r=60),
        paper_bgcolor="white",
    )
    return fig


def score_heatmap(scores: dict[str, float]) -> go.Figure | None:
    """
    Heatmap điểm từng thông số theo màu rủi ro.
    """
    if not scores:
        return None

    h_ids = [p["id"] for p in PARAMETERS if p["group"] == "H"]
    p_ids = [p["id"] for p in PARAMETERS if p["group"] == "P"]
    r_ids = [p["id"] for p in PARAMETERS if p["group"] == "R"]

    # Sắp xếp thành ma trận 3 × max_col
    max_col = max(len(h_ids), len(p_ids), len(r_ids))

    def pad(lst):
        return lst + [None] * (max_col - len(lst))

    row_labels = ["H — Nguồn", "P — Đường", "R — Đối tượng"]
    col_data = [pad(h_ids), pad(p_ids), pad(r_ids)]

    z = []
    text = []
    for row in col_data:
        z_row = []
        t_row = []
        for pid in row:
            if pid is None:
                z_row.append(None)
                t_row.append("")
            else:
                s = scores.get(pid) or 1.00
                z_row.append(s)
                t_row.append(f"{pid}<br>{s}")
        z.append(z_row)
        text.append(t_row)

    col_labels = [f"#{i+1}" for i in range(max_col)]

    fig = go.Figure(go.Heatmap(
        z=z,
        x=col_labels,
        y=row_labels,
        text=text,
        texttemplate="%{text}",
        colorscale=[
            [0.00, RISK_COLORS[1]],
            [0.25, RISK_COLORS[1]],
            [0.50, RISK_COLORS[2]],
            [0.75, RISK_COLORS[3]],
            [1.00, RISK_COLORS[4]],
        ],
        zmin=0.25,
        zmax=1.00,
        showscale=True,
        colorbar=dict(
            tickvals=[0.25, 0.50, 0.75, 1.00],
            ticktext=["0,25 (Thấp)", "0,50", "0,75", "1,00 (Rất cao)"],
        ),
    ))
    fig.update_layout(
        height=260,
        margin=dict(t=10, b=10, l=120, r=60),
        paper_bgcolor="white",
    )
    return fig


def comparison_bar_chart(summary_list: list[dict]) -> go.Figure | None:
    """
    Biểu đồ cột so sánh H, P, R của nhiều BCL.
    """
    if not summary_list:
        return None

    names = [s["ten_bcl"] for s in summary_list]
    h_vals = [s["H"] for s in summary_list]
    p_vals = [s["P"] for s in summary_list]
    r_vals = [s["R"] for s in summary_list]

    fig = go.Figure()
    for vals, label, color in [
        (h_vals, "H (Nguồn)", "#e74c3c"),
        (p_vals, "P (Đường)", "#f39c12"),
        (r_vals, "R (Đối tượng)", "#2980b9"),
    ]:
        fig.add_trace(go.Bar(
            name=label,
            x=names,
            y=vals,
            marker_color=color,
        ))

    fig.update_layout(
        barmode="group",
        yaxis=dict(range=[0, 1.1], title="Giá trị"),
        height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=40, b=60, l=40, r=20),
        paper_bgcolor="white",
    )
    return fig


def scatter_cri_area(summary_list: list[dict]) -> go.Figure | None:
    """
    Scatter plot: CRI theo diện tích BCL. Màu theo cấp rủi ro.
    """
    if not summary_list:
        return None

    fig = go.Figure()
    level_groups = {1: [], 2: [], 3: [], 4: []}
    for s in summary_list:
        lv = s.get("risk_level") or 1
        level_groups.setdefault(lv, []).append(s)

    level_labels = {1: "Cấp 1 — Thấp", 2: "Cấp 2 — TB", 3: "Cấp 3 — Cao", 4: "Cấp 4 — Rất cao"}

    for level, items in level_groups.items():
        if not items:
            continue
        fig.add_trace(go.Scatter(
            x=[s["dien_tich_ha"] for s in items],
            y=[s["CRI"] for s in items],
            mode="markers+text",
            text=[s["ten_bcl"] for s in items],
            textposition="top center",
            marker=dict(
                size=14,
                color=RISK_COLORS.get(level, "#999"),
                line=dict(width=1, color="white"),
            ),
            name=level_labels.get(level, ""),
        ))

    # Đường ngưỡng
    for threshold, label in [(0.36, "Cấp 1/2"), (0.53, "Cấp 2/3"), (0.69, "Cấp 3/4")]:
        fig.add_hline(
            y=threshold,
            line_dash="dot",
            line_color="#999",
            annotation_text=label,
            annotation_position="right",
        )

    fig.update_layout(
        xaxis=dict(title="Diện tích (ha)"),
        yaxis=dict(title="CRI", range=[0.2, 1.05]),
        height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=40, b=40, l=50, r=60),
        paper_bgcolor="white",
    )
    return fig


def risk_distribution_chart(summary_list: list[dict]) -> go.Figure | None:
    """
    Biểu đồ phân bố số BCL theo cấp rủi ro.
    """
    if not summary_list:
        return None

    counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for item in summary_list:
        level = item.get("risk_level")
        if level in counts:
            counts[level] += 1

    labels = {
        1: "Cấp 1 — Thấp",
        2: "Cấp 2 — Trung bình",
        3: "Cấp 3 — Cao",
        4: "Cấp 4 — Rất cao",
    }
    levels = [1, 2, 3, 4]
    values = [counts[level] for level in levels]

    fig = go.Figure(go.Bar(
        x=[labels[level] for level in levels],
        y=values,
        marker_color=[RISK_COLORS[level] for level in levels],
        text=values,
        textposition="outside",
    ))
    fig.update_layout(
        yaxis=dict(title="Số lượng BCL", rangemode="tozero"),
        xaxis=dict(title="Cấp rủi ro"),
        height=320,
        showlegend=False,
        margin=dict(t=30, b=70, l=50, r=20),
        paper_bgcolor="white",
    )
    return fig


def province_distribution_chart(summary_list: list[dict]) -> go.Figure | None:
    """
    Biểu đồ số BCL theo tỉnh/thành phố.
    """
    if not summary_list:
        return None

    counts: dict[str, int] = {}
    for item in summary_list:
        province = item.get("tinh") or "Chưa rõ địa phương"
        counts[province] = counts.get(province, 0) + 1

    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    provinces = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    fig = go.Figure(go.Bar(
        x=values,
        y=provinces,
        orientation="h",
        marker_color="#1f77b4",
        text=values,
        textposition="outside",
    ))
    fig.update_layout(
        xaxis=dict(title="Số lượng BCL", rangemode="tozero"),
        yaxis=dict(title=""),
        height=max(300, 60 + 32 * len(provinces)),
        showlegend=False,
        margin=dict(t=30, b=40, l=140, r=30),
        paper_bgcolor="white",
    )
    return fig


def priority_top_chart(summary_list: list[dict], n: int = 10) -> go.Figure | None:
    """
    Biểu đồ top BCL-KHVS cần ưu tiên theo CRI.
    """
    khvs = [item for item in summary_list if item.get("CRI") is not None]
    if not khvs:
        return None

    top_items = sorted(khvs, key=lambda x: x["CRI"], reverse=True)[:n]
    names = [item["ten_bcl"] for item in top_items]
    values = [item["CRI"] for item in top_items]
    colors = [RISK_COLORS.get(item.get("risk_level"), "#95a5a6") for item in top_items]

    fig = go.Figure(go.Bar(
        x=values,
        y=names,
        orientation="h",
        marker_color=colors,
        text=[f"{v:.4f}" for v in values],
        textposition="outside",
    ))
    fig.update_layout(
        xaxis=dict(title="CRI", range=[0.25, 1.05]),
        yaxis=dict(title="", autorange="reversed"),
        height=max(320, 70 + 34 * len(top_items)),
        showlegend=False,
        margin=dict(t=30, b=40, l=170, r=60),
        paper_bgcolor="white",
    )
    return fig
