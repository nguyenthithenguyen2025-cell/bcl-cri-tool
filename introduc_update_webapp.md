# Đề xuất nâng cấp web app BCL-CRI theo hướng chuyên nghiệp hóa

## 1. Bối cảnh và mục tiêu nâng cấp

Web app BCL-CRI hiện đã có các chức năng cốt lõi để khai báo thông tin bãi chôn lấp, nhập thông số CRI, tính toán chỉ số rủi ro, phân loại mức độ rủi ro, khuyến nghị giải pháp đóng bãi và xuất báo cáo. Tuy nhiên, để có thể giới thiệu rộng rãi cho cơ quan quản lý nhà nước, các sở, ngành và địa phương, ứng dụng cần được nâng cấp theo hướng chuyên nghiệp hơn về giao diện, quy trình nghiệp vụ, nội dung chuyên môn, chất lượng báo cáo và khả năng vận hành.

Mục tiêu của đợt nâng cấp là chuyển web app từ mức công cụ thử nghiệm kỹ thuật sang mức công cụ hỗ trợ ra quyết định có hình thức trang trọng, logic sử dụng rõ ràng, đầu ra phù hợp hồ sơ quản lý môi trường và có thể trình diễn trong các cuộc họp chuyên môn với cơ quan nhà nước.

## 2. Định vị người dùng mục tiêu

Ứng dụng cần được thiết kế cho các nhóm người dùng chính sau:

- Cơ quan quản lý nhà nước về môi trường ở cấp trung ương và địa phương.
- Sở Nông nghiệp và Môi trường, các chi cục/bộ phận quản lý chất thải rắn.
- Ủy ban nhân dân cấp tỉnh, huyện, xã có nhu cầu rà soát hiện trạng bãi chôn lấp.
- Ban quản lý dự án, đơn vị tư vấn môi trường, đơn vị vận hành bãi chôn lấp.
- Nhóm nghiên cứu và đào tạo trong lĩnh vực quản lý chất thải rắn và kỹ thuật môi trường.

Do đó, giao diện và nội dung cần tránh phong cách thử nghiệm, hạn chế biểu tượng cảm xúc không cần thiết, ưu tiên ngôn ngữ kỹ thuật trang trọng, bố cục rõ ràng, minh bạch về cơ sở pháp lý và phương pháp tính toán.

## 3. Định hướng nâng cấp tổng thể

### 3.1. Nâng cấp nhận diện và thông điệp

Ứng dụng cần có nhận diện chính thức hơn, bao gồm tên công cụ, logo đơn vị chủ trì, thông tin đề tài, phiên bản, ngày cập nhật và phạm vi áp dụng. Trang giới thiệu cần nêu rõ đây là công cụ hỗ trợ quyết định, không thay thế khảo sát kỹ thuật chi tiết, thiết kế kỹ thuật hoặc thẩm định của cơ quan có thẩm quyền.

Nội dung giới thiệu nên thể hiện rõ:

- Mục tiêu đánh giá rủi ro bãi chôn lấp chất thải rắn sinh hoạt.
- Phạm vi áp dụng cho bãi chôn lấp hợp vệ sinh và không hợp vệ sinh.
- Nguyên tắc sử dụng chỉ số rủi ro tổng hợp CRI.
- Mối liên hệ giữa kết quả CRI và nhóm giải pháp đóng bãi.
- Giới hạn của công cụ và yêu cầu kiểm chứng dữ liệu đầu vào.

### 3.2. Nâng cấp giao diện theo hướng dashboard hành chính - kỹ thuật

Giao diện nên được thiết kế lại theo phong cách dashboard phục vụ công tác quản lý nhà nước: sáng, rõ, ít trang trí, ưu tiên khả năng đọc nhanh, so sánh nhanh và truy xuất báo cáo. Các trang cần thống nhất hệ màu, font chữ, khoảng cách, kích thước thẻ kết quả, bảng dữ liệu và biểu đồ.

Sidebar nên được tổ chức lại theo nhóm chức năng:

- Tổng quan.
- Khai báo bãi chôn lấp.
- Đánh giá CRI.
- Kết quả và giải pháp.
- So sánh nhiều bãi chôn lấp.
- Xuất hồ sơ và lưu phiên làm việc.
- Hướng dẫn và căn cứ kỹ thuật.

Các biểu tượng cảm xúc nên được thay thế bằng biểu tượng chuyên nghiệp hoặc nhãn chữ rõ ràng. Màu rủi ro vẫn có thể dùng xanh, vàng, cam, đỏ, nhưng cần áp dụng nhất quán và có chú giải.

### 3.3. Nâng cấp quy trình nghiệp vụ

Ứng dụng nên được cấu trúc thành quy trình 5 bước:

1. Khai báo thông tin bãi chôn lấp.
2. Phân loại bãi chôn lấp hợp vệ sinh hoặc không hợp vệ sinh.
3. Nhập và kiểm tra 14 thông số CRI.
4. Xem kết quả, phân tích rủi ro và giải pháp khuyến nghị.
5. Xuất báo cáo, bảng tổng hợp và lưu hồ sơ đánh giá.

Mỗi bước cần có trạng thái rõ ràng: chưa bắt đầu, đang nhập, thiếu dữ liệu, đã đủ dữ liệu, đã tính CRI, sẵn sàng xuất báo cáo. Khi người dùng nhập thiếu dữ liệu, hệ thống cần yêu cầu ghi lý do thiếu dữ liệu để bảo đảm tính minh bạch của hồ sơ.

### 3.4. Nâng cấp nội dung chuyên môn

Mỗi thông số CRI cần có mô tả đầy đủ hơn:

- Định nghĩa kỹ thuật.
- Cách xác định ngoài hiện trường hoặc từ hồ sơ sẵn có.
- Nguồn dữ liệu khuyến nghị.
- Các mức điểm 0,25; 0,50; 0,75; 1,00.
- Lưu ý khi dữ liệu không đầy đủ hoặc có độ tin cậy thấp.

Kết quả CRI cần có phần diễn giải tự động theo cấu trúc chuyên môn:

- Nhận xét về nhóm nguồn nguy hại H.
- Nhận xét về nhóm đường lan truyền P.
- Nhận xét về nhóm đối tượng tiếp nhận R.
- Nhận diện các thông số chi phối rủi ro.
- Khuyến nghị khảo sát bổ sung nếu thiếu dữ liệu quan trọng.
- Đề xuất hướng ưu tiên đầu tư hoặc can thiệp.

### 3.5. Nâng cấp báo cáo đầu ra

Báo cáo Word và HTML cần được định dạng như hồ sơ kỹ thuật có thể gửi kèm tài liệu làm việc. Cấu trúc báo cáo nên bao gồm:

1. Trang bìa.
2. Thông tin đơn vị, người lập, người kiểm tra và ngày đánh giá.
3. Thông tin chung về bãi chôn lấp.
4. Căn cứ pháp lý và kỹ thuật.
5. Phương pháp đánh giá CRI.
6. Bảng điểm 14 thông số.
7. Kết quả H, P, R và CRI.
8. Phân tích rủi ro.
9. Giải pháp đóng bãi khuyến nghị.
10. Phụ lục dữ liệu đầu vào và ghi chú dữ liệu thiếu.

File Excel cần phục vụ mục tiêu tổng hợp cấp tỉnh hoặc cấp vùng, có sheet dữ liệu chuẩn, sheet xếp hạng, sheet thông số CRI và sheet kết quả giải pháp.

### 3.6. Nâng cấp độ tin cậy và khả năng vận hành

Ứng dụng cần bổ sung kiểm tra dữ liệu đầu vào chặt chẽ hơn, ví dụ:

- Năm ngừng tiếp nhận không được nhỏ hơn năm bắt đầu hoạt động.
- Tọa độ phải nằm trong khoảng hợp lý của Việt Nam.
- Diện tích, thể tích, chiều cao phải có cảnh báo nếu bất thường.
- BCL-KHVS chưa tính CRI không được hiển thị như BCL-HVS.
- Dữ liệu thiếu cần có lý do.

Trong giai đoạn giới thiệu rộng rãi, cơ chế lưu/tải phiên làm việc bằng JSON vẫn phù hợp. Nếu triển khai chính thức ở nhiều địa phương, nên xem xét nâng cấp sang cơ sở dữ liệu, tài khoản người dùng, phân quyền theo địa phương và lịch sử chỉnh sửa.

## 4. Kết quả mong đợi sau nâng cấp

Sau khi hoàn thành nâng cấp, web app cần đạt các yêu cầu sau:

- Giao diện trang trọng, phù hợp trình diễn với cơ quan quản lý nhà nước.
- Quy trình sử dụng rõ ràng, giảm nhầm lẫn khi nhập nhiều bãi chôn lấp.
- Nội dung chuyên môn đủ giải thích cho cán bộ địa phương và đơn vị tư vấn.
- Kết quả CRI được diễn giải thành nhận xét kỹ thuật dễ hiểu.
- Báo cáo đầu ra có thể sử dụng như phụ lục kỹ thuật trong hồ sơ rà soát, lập kế hoạch hoặc đề xuất dự án.
- Có kiểm thử tự động cho logic tính toán và xuất báo cáo để hạn chế lỗi hồi quy.

## 5. Nguyên tắc thực hiện

Quá trình nâng cấp cần tuân thủ các nguyên tắc sau:

- Không tự ý thay đổi công thức CRI, trọng số và ngưỡng phân loại nếu chưa có xác nhận chuyên môn.
- Ưu tiên tính minh bạch của dữ liệu đầu vào và cách xử lý dữ liệu thiếu.
- Ngôn ngữ giao diện và báo cáo dùng tiếng Việt đầy đủ dấu, văn phong khoa học, trang trọng.
- Thiết kế giao diện phục vụ công việc quản lý và kỹ thuật, không theo phong cách quảng bá thương mại.
- Mỗi thay đổi lớn cần có tiêu chí kiểm tra và ghi lại trong tài liệu bàn giao.
