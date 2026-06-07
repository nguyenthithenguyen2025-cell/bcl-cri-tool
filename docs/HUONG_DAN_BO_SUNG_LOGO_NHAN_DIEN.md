# Hướng dẫn bổ sung logo nhận diện chính thức

## 1. Các logo cần cung cấp

Để hoàn thiện nhận diện chính thức của app, cần cung cấp tối thiểu các file sau:

| Nhóm nhận diện | Tên file cần đặt | Ghi chú |
|----------------|------------------|---------|
| Đơn vị chủ trì | `logo_don_vi_chu_tri.png` | Ví dụ: Trường Đại học Thủy Lợi hoặc đơn vị chủ trì đề tài |
| Đề tài/chương trình | `logo_de_tai.png` | Nếu đề tài có logo/biểu trưng riêng |
| Cơ quan phối hợp | `logo_co_quan_phoi_hop.png` | Nếu có cơ quan phối hợp chính thức |

Các file đặt tại:

```text
assets/branding/
```

## 2. Yêu cầu định dạng

- Ưu tiên định dạng `.png` nền trong suốt.
- Chiều ngang khuyến nghị: 300-600 px.
- Chiều cao khuyến nghị: 120-300 px.
- Dung lượng mỗi logo nên dưới 500 KB.
- Logo cần sắc nét, không bị mờ, không bị méo tỷ lệ, không bị cắt viền.

## 3. Cách app sử dụng logo

Khi các file logo tồn tại trong `assets/branding/`, app sẽ tự hiển thị logo ở sidebar theo thứ tự:

1. Đơn vị chủ trì.
2. Đề tài/chương trình.
3. Cơ quan phối hợp.

Nếu chưa có file logo, app vẫn hoạt động bình thường và không hiển thị khối logo.

## 4. Lưu ý khi triển khai lên Streamlit Cloud

Logo cần được commit và push lên GitHub để Streamlit Cloud hiển thị được. Sau khi bổ sung logo, cần chạy:

```bash
git add assets/branding/
git commit -m "Branding: bổ sung logo nhận diện chính thức"
git push origin master
```

Sau khi push, Streamlit Cloud sẽ tự rebuild và cập nhật giao diện.
