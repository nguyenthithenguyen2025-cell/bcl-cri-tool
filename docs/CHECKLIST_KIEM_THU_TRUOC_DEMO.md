# Checklist kiểm thử trước khi demo

## 1. Kiểm thử cục bộ

- [ ] Chạy `python -m unittest discover -s tests -v`.
- [ ] Kết quả đạt toàn bộ test.
- [ ] Chạy `streamlit run app.py`.
- [ ] Mở được app tại `http://localhost:8501`.
- [ ] Sidebar hiển thị đúng tên section.
- [ ] Không có lỗi Python trên terminal.

## 2. Kiểm thử nhập dữ liệu

- [ ] Tạo một BCL-KHVS mới.
- [ ] Kiểm tra lỗi năm ngừng tiếp nhận nhỏ hơn năm bắt đầu.
- [ ] Kiểm tra cảnh báo tọa độ thiếu một trong hai giá trị.
- [ ] Nhập dữ liệu hợp lệ và xác nhận hồ sơ tự lưu.
- [ ] Nạp điểm mẫu PL2.4.
- [ ] Kiểm tra CRI mẫu khoảng 0,6647 và phân loại Cấp 3.
- [ ] Thử chọn một thông số “Chưa có dữ liệu” và xác nhận hệ thống yêu cầu lý do.

## 3. Kiểm thử kết quả

- [ ] Trang “Lựa chọn giải pháp can thiệp, đóng bãi” hiển thị H, P, R, CRI.
- [ ] Biểu đồ radar, gauge, bar và heatmap hiển thị.
- [ ] Phân tích chuyên môn theo H/P/R hiển thị.
- [ ] Thông số chi phối rủi ro hiển thị.
- [ ] Giải pháp khuyến nghị có hạng mục bắt buộc và hạng mục bổ sung.

## 4. Kiểm thử xuất báo cáo

- [ ] Nhập thông tin đơn vị thực hiện, người lập, người kiểm tra.
- [ ] Xuất Excel thành công.
- [ ] Excel có sheet “0. Thông tin báo cáo”.
- [ ] Xuất Word thành công.
- [ ] Word có trang bìa và tiếng Việt không lỗi font.
- [ ] Xuất HTML thành công.
- [ ] HTML mở được bằng Chrome/Edge và có thể in PDF.
- [ ] Xuất JSON thành công.
- [ ] Tải lại JSON và xác nhận dữ liệu phục hồi.

## 5. Kiểm thử Streamlit Cloud

- [ ] Push commit mới lên GitHub.
- [ ] Đợi Streamlit Cloud rebuild.
- [ ] Mở URL app công khai.
- [ ] Kiểm tra các trang chính.
- [ ] Tạo BCL mẫu và xuất ít nhất một báo cáo.

## 6. Các lỗi cần ghi nhận

| STT | Mô tả lỗi | Trang/chức năng | Mức độ | Hướng xử lý |
|-----|-----------|-----------------|--------|-------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
