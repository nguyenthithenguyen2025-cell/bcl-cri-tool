# Công cụ hỗ trợ lựa chọn giải pháp đóng bãi chôn lấp CTRSH

**BCL-CRI Tool**

Ứng dụng web tính toán Chỉ số Rủi ro Tổng hợp (CRI) và khuyến nghị giải pháp đóng bãi cho bãi chôn lấp không hợp vệ sinh tại Việt Nam.

**Căn cứ:** Đề tài TNMT.2024.05.05, Trường ĐH Thủy Lợi (2026) | TT 02/2022/TT-BTNMT | QCVN 96:2025/BNNMT

---

## Cài đặt và chạy

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Kiểm thử

```bash
python -m unittest discover -s tests -v
```

## Tài liệu dự án

- [PROJECT_BRIEF.md](PROJECT_BRIEF.md) — Mô tả đầy đủ: mục tiêu, phương pháp CRI, kiến trúc
- [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) — Kế hoạch phát triển 5 sprint
