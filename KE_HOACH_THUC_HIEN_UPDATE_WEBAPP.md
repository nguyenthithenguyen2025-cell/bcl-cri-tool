# Kế hoạch thực hiện nâng cấp web app BCL-CRI

## 1. Mục tiêu kế hoạch

Kế hoạch này nhằm triển khai các nâng cấp cần thiết để web app BCL-CRI trở thành công cụ có thể giới thiệu rộng rãi cho cơ quan nhà nước và các địa phương trong công tác rà soát, đánh giá rủi ro và lựa chọn giải pháp đóng bãi chôn lấp chất thải rắn sinh hoạt.

## 2. Nguyên tắc ưu tiên

Các hạng mục được ưu tiên theo bốn tiêu chí:

- Tác động trực tiếp đến trải nghiệm và niềm tin của người dùng.
- Tác động đến tính đúng đắn, minh bạch và khả năng truy xuất của kết quả CRI.
- Mức độ cần thiết khi trình diễn cho cơ quan quản lý nhà nước.
- Khả năng hoàn thành nhanh trong kiến trúc Streamlit hiện có.

## 3. Lộ trình thực hiện đề xuất

### Giai đoạn 1. Chuẩn hóa giao diện và quy trình sử dụng

**Mục tiêu:** Làm cho app có hình thức trang trọng, dễ dùng và phù hợp trình diễn chính thức.

**Hạng mục công việc:**

- Thiết kế lại sidebar theo nhóm chức năng rõ ràng.
- Giảm biểu tượng cảm xúc trong tiêu đề, nút bấm và thông báo chính.
- Chuẩn hóa hệ màu, font chữ, khoảng cách, thẻ kết quả, bảng dữ liệu và biểu đồ.
- Thêm trạng thái quy trình 5 bước: khai báo, phân loại, nhập CRI, xem kết quả, xuất báo cáo.
- Làm rõ trạng thái từng BCL: chưa đủ thông tin, chưa tính CRI, đã tính CRI, BCL-HVS.
- Bổ sung khả năng chọn và chỉnh sửa lại BCL đã nhập.

**Đầu ra:**

- Giao diện 6 trang thống nhất hơn.
- Sidebar và điều hướng rõ ràng hơn.
- Người dùng có thể chỉnh sửa nhiều BCL mà không nhầm dữ liệu.

**Tiêu chí nghiệm thu:**

- Tất cả trang hiển thị ổn định trên màn hình desktop.
- BCL-KHVS chưa tính CRI không bị hiển thị nhầm là BCL-HVS.
- Người dùng có thể nhập 2-3 BCL, quay lại sửa từng BCL và kết quả cập nhật đúng.

### Giai đoạn 2. Nâng cấp kiểm tra dữ liệu đầu vào

**Mục tiêu:** Tăng độ tin cậy của dữ liệu và tính minh bạch khi xử lý thiếu dữ liệu.

**Hạng mục công việc:**

- Bổ sung kiểm tra năm ngừng tiếp nhận so với năm bắt đầu hoạt động.
- Bổ sung cảnh báo tọa độ ngoài phạm vi hợp lý của Việt Nam.
- Cảnh báo diện tích, thể tích hoặc chiều cao bất thường.
- Bắt buộc nhập lý do khi chọn "chưa có dữ liệu" cho thông số CRI.
- Hiển thị danh sách thông số thiếu và lý do thiếu trong báo cáo.
- Thêm thông báo về nguyên tắc thận trọng khi gán điểm 1,00.

**Đầu ra:**

- Module validator hoàn chỉnh hơn.
- Form nhập CRI có kiểm soát dữ liệu thiếu.
- Báo cáo thể hiện rõ dữ liệu nào được giả định ở mức rủi ro tối đa.

**Tiêu chí nghiệm thu:**

- Không thể hoàn tất hồ sơ nếu thiếu lý do cho thông số chưa có dữ liệu.
- Báo cáo Word/HTML/Excel ghi nhận đầy đủ thông số thiếu và lý do.
- Các cảnh báo dữ liệu bất thường hiển thị rõ nhưng không gây mất dữ liệu người dùng.

### Giai đoạn 3. Nâng cấp nội dung chuyên môn và diễn giải kết quả

**Mục tiêu:** Làm cho kết quả không chỉ là số CRI mà trở thành nhận xét kỹ thuật có giá trị tham khảo cho địa phương.

**Hạng mục công việc:**

- Bổ sung mô tả kỹ thuật cho 14 thông số CRI.
- Thêm nguồn dữ liệu khuyến nghị cho từng thông số.
- Nâng cấp phần phân tích tự động theo nhóm H, P, R.
- Diễn giải top thông số chi phối rủi ro và hướng xử lý.
- Thêm khuyến nghị khảo sát bổ sung khi dữ liệu thiếu hoặc rủi ro cao.
- Chuẩn hóa mô tả giải pháp đóng bãi theo hạng mục kỹ thuật.

**Đầu ra:**

- Trang kết quả có phần phân tích kỹ thuật chuyên sâu hơn.
- Báo cáo có phần nhận xét rủi ro theo nhóm H, P, R.
- Giải pháp đóng bãi trình bày theo ngôn ngữ hồ sơ kỹ thuật.

**Tiêu chí nghiệm thu:**

- Mỗi kết quả CRI có nhận xét rõ về H, P, R.
- Top 3 thông số rủi ro cao được giải thích theo ý nghĩa kỹ thuật.
- Giải pháp khuyến nghị có hạng mục bắt buộc, hạng mục bổ sung và lưu ý triển khai.

### Giai đoạn 4. Nâng cấp báo cáo và hồ sơ đầu ra

**Mục tiêu:** Tạo báo cáo đủ trang trọng để gửi kèm hồ sơ làm việc, trình bày hoặc trao đổi với địa phương.

**Hạng mục công việc:**

- Thiết kế lại mẫu Word với trang bìa, mục lục, tiêu đề chương mục và bảng biểu.
- Nâng cấp HTML export để in PDF đẹp hơn, có bố cục A4 và tiêu đề chính thức.
- Bổ sung thông tin người lập, người kiểm tra, đơn vị thực hiện và ngày đánh giá.
- Bổ sung phụ lục dữ liệu đầu vào.
- Bổ sung phần căn cứ pháp lý và giới hạn sử dụng kết quả.
- Nâng cấp Excel export để phục vụ tổng hợp nhiều BCL cấp tỉnh.

**Đầu ra:**

- File Word có cấu trúc báo cáo kỹ thuật hoàn chỉnh.
- File HTML/PDF có thể dùng để trình bày nhanh.
- File Excel có dữ liệu chuẩn hóa để tổng hợp.

**Tiêu chí nghiệm thu:**

- Báo cáo không lỗi font tiếng Việt.
- Bảng điểm 14 thông số, H/P/R/CRI và giải pháp hiển thị đầy đủ.
- Khi có dữ liệu thiếu, báo cáo ghi rõ lý do và điểm giả định.

### Giai đoạn 5. Nâng cấp dashboard so sánh và hỗ trợ lập kế hoạch

**Mục tiêu:** Hỗ trợ cơ quan quản lý xem xét nhiều bãi chôn lấp và xác định ưu tiên xử lý.

**Hạng mục công việc:**

- Nâng cấp bảng xếp hạng theo CRI với bộ lọc rõ hơn.
- Thêm chỉ báo ưu tiên xử lý: thấp, trung bình, cao, rất cao.
- Bổ sung biểu đồ so sánh H/P/R giữa nhiều BCL.
- Bổ sung biểu đồ phân bố theo địa phương.
- Xem xét tích hợp bản đồ OpenStreetMap nếu dữ liệu tọa độ đủ tin cậy.
- Xuất báo cáo tổng hợp nhiều BCL.

**Đầu ra:**

- Dashboard so sánh nhiều BCL có giá trị quản lý cấp tỉnh.
- Bảng ưu tiên xử lý phục vụ lập kế hoạch đầu tư.
- File Excel tổng hợp có thể gửi cho địa phương.

**Tiêu chí nghiệm thu:**

- Nhập tối thiểu 5 BCL và xếp hạng đúng theo CRI.
- Lọc theo tỉnh, cấp rủi ro và giải pháp hoạt động đúng.
- Export bảng tổng hợp giữ đúng định dạng và dữ liệu.

### Giai đoạn 6. Chuẩn bị giới thiệu và vận hành thử

**Mục tiêu:** Hoàn thiện app để trình diễn, lấy ý kiến và vận hành thử với dữ liệu thực tế.

**Hạng mục công việc:**

- Chuẩn bị bộ dữ liệu mẫu minh họa.
- Viết hướng dẫn sử dụng ngắn cho cán bộ địa phương.
- Chuẩn bị kịch bản trình diễn 10-15 phút.
- Kiểm tra app trên Streamlit Community Cloud.
- Kiểm tra các file export trên máy người dùng phổ biến.
- Ghi nhận phản hồi và lập danh sách cải tiến sau vận hành thử.

**Đầu ra:**

- App demo ổn định.
- Tài liệu hướng dẫn sử dụng.
- Bộ dữ liệu mẫu.
- Danh sách phản hồi và đề xuất nâng cấp phiên bản tiếp theo.

**Tiêu chí nghiệm thu:**

- Người dùng mới có thể nhập một BCL mẫu và xuất báo cáo mà không cần hướng dẫn trực tiếp.
- App chạy ổn định trên Streamlit Cloud.
- Báo cáo xuất ra có thể mở bằng Microsoft Word, Chrome/Edge và Excel.

## 4. Thứ tự ưu tiên triển khai ngắn hạn

Trong 1-2 phiên làm việc tiếp theo, nên ưu tiên:

1. Hoàn thiện luồng chỉnh sửa BCL đã nhập và trạng thái dữ liệu.
2. Chuẩn hóa giao diện sidebar, tiêu đề trang và thông báo.
3. Bắt buộc ghi lý do khi thiếu dữ liệu CRI.
4. Nâng cấp phần diễn giải kết quả CRI.
5. Nâng cấp báo cáo Word/HTML theo mẫu hồ sơ kỹ thuật.
6. Bổ sung kiểm thử tự động cho các chức năng chính.

## 5. Rủi ro cần kiểm soát

- Không thay đổi công thức CRI, trọng số và ngưỡng phân loại khi chưa có xác nhận chuyên môn.
- Tránh làm giao diện quá phức tạp khiến cán bộ địa phương khó sử dụng.
- Tránh để dữ liệu thiếu được xử lý tự động mà không có ghi chú trong báo cáo.
- Cần kiểm tra kỹ tiếng Việt trong file Word, HTML và Excel.
- Cần kiểm tra Streamlit Cloud sau mỗi thay đổi lớn vì môi trường cloud có thể khác máy cục bộ.

## 6. Đề xuất cấu trúc phiên bản

- Phiên bản 1.0: App hiện có, đủ chức năng tính CRI và xuất báo cáo.
- Phiên bản 1.1: Chuẩn hóa giao diện, chỉnh sửa BCL đã nhập, kiểm tra dữ liệu tốt hơn.
- Phiên bản 1.2: Nâng cấp diễn giải chuyên môn và báo cáo kỹ thuật.
- Phiên bản 1.3: Dashboard so sánh và báo cáo tổng hợp cấp tỉnh.
- Phiên bản 2.0: Cơ sở dữ liệu, tài khoản người dùng, phân quyền và lịch sử chỉnh sửa.
