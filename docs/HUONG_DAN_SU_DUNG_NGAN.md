# Hướng dẫn sử dụng ngắn — Công cụ hỗ trợ lựa chọn giải pháp đóng bãi chôn lấp CTRSH

## 1. Mục đích sử dụng

Công cụ hỗ trợ cán bộ quản lý, địa phương và đơn vị tư vấn đánh giá rủi ro bãi chôn lấp chất thải rắn sinh hoạt, tính chỉ số CRI và lựa chọn nhóm giải pháp can thiệp, đóng bãi phù hợp.

Kết quả của công cụ là cơ sở hỗ trợ ra quyết định ban đầu, không thay thế khảo sát hiện trường, thiết kế kỹ thuật, đánh giá tác động môi trường hoặc thẩm định của cơ quan có thẩm quyền.

## 2. Quy trình thao tác

### Bước 1. Tổng quan công cụ

Mở app và kiểm tra phần trạng thái hồ sơ ở sidebar. Nếu chưa có dữ liệu, bắt đầu tại trang **Khai báo bãi chôn lấp**.

### Bước 2. Khai báo bãi chôn lấp

Nhập các thông tin chính:

- Tên bãi chôn lấp.
- Tỉnh/thành phố, xã/phường.
- Tọa độ nếu có.
- Loại hình bãi chôn lấp: BCL-KHVS hoặc BCL-HVS.
- Diện tích, thể tích, chiều cao ước tính.
- Năm bắt đầu và năm ngừng tiếp nhận.

Nếu dữ liệu bắt buộc chưa hợp lệ, hệ thống sẽ không tự lưu hồ sơ.

### Bước 3. Đánh giá CRI

Với BCL-KHVS, nhập 14 thông số thuộc ba nhóm:

- H — Nguồn nguy hại.
- P — Đường lan truyền.
- R — Đối tượng tiếp nhận.

Nếu chưa có dữ liệu cho thông số nào, chọn **Chưa có dữ liệu** và ghi rõ lý do. Hệ thống sẽ gán điểm 1,00 cho thông số thiếu theo nguyên tắc thận trọng.

### Bước 4. Lựa chọn giải pháp can thiệp, đóng bãi

Xem kết quả:

- Chỉ số H, P, R và CRI.
- Cấp rủi ro.
- Nhóm giải pháp khuyến nghị.
- Phân tích chuyên môn theo H/P/R.
- Thông số chi phối rủi ro.
- Khuyến nghị kỹ thuật tiếp theo.

### Bước 5. So sánh bãi chôn lấp

Khi có nhiều BCL, dùng trang so sánh để:

- Xếp hạng theo CRI.
- Lọc theo tỉnh, cấp rủi ro, giải pháp.
- Xuất bảng tổng hợp Excel.

### Bước 6. Xuất hồ sơ và báo cáo

Chọn BCL cần xuất, nhập thông tin trang bìa:

- Đơn vị thực hiện.
- Người lập báo cáo.
- Người kiểm tra.
- Ngày lập báo cáo.

Sau đó xuất:

- Excel để tổng hợp dữ liệu.
- Word để làm hồ sơ kỹ thuật.
- HTML để in PDF bằng Chrome/Edge.
- JSON để lưu và tải lại phiên làm việc.

## 3. Kiểm tra nhanh trước khi gửi báo cáo

Trước khi dùng báo cáo cho trao đổi chính thức, cần kiểm tra:

- Tên BCL, địa phương và loại hình BCL.
- 14 thông số CRI và lý do thiếu dữ liệu.
- Cấp rủi ro và nhóm giải pháp.
- Phần phân tích chuyên môn.
- Thông tin người lập, người kiểm tra và ngày báo cáo.
- Font tiếng Việt trong Word/HTML/Excel.

## 4. Lưu ý vận hành

- Dữ liệu trong phiên Streamlit có thể mất khi đóng hoặc tải lại trình duyệt nếu chưa xuất JSON.
- Nên xuất JSON sau mỗi đợt nhập dữ liệu để có thể phục hồi phiên làm việc.
- Nếu cần báo cáo PDF, tải HTML và dùng Chrome/Edge để in thành PDF.
- Với hồ sơ chính thức, cần kiểm chứng dữ liệu bằng khảo sát thực địa và hồ sơ kỹ thuật.
