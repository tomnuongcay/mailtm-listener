# 📧 MAIL.TM AUTO LISTENER (VIP PROMAX EDITION)

Một công cụ mã nguồn mở mạnh mẽ giúp tự động hóa việc tạo và lắng nghe mã xác minh (OTP) từ các hộp thư tạm thời của **Mail.tm**. Công cụ này được thiết kế để hoạt động hoàn toàn tự động, nhanh chóng và dễ sử dụng.

---

## ✨ Tính năng nổi bật

* **Tự động hoàn toàn:** Không cần đăng ký thủ công, tự động lấy tên miền và tạo tài khoản ngẫu nhiên.
* **Đăng nhập không mật khẩu:** Tự động xử lý Token API mà không cần người dùng nhập mật khẩu.
* **Vòng lặp vô tận:** Sau khi nhận mã hoặc bỏ qua, hệ thống tự động làm mới và tạo mail mới ngay lập tức.
* **Tính năng Skip thông minh:** Nhấn phím `[ENTER]` bất cứ lúc nào để bỏ qua email hiện tại và đổi sang email khác (hỗ trợ tốt trên cả Windows và Linux).
* **Lọc mã OTP:** Tự động tìm và trích xuất mã xác minh 6 số từ nội dung email.
* **Giao diện trực quan:** Sử dụng Colorama để hiển thị trạng thái bằng màu sắc, dễ dàng theo dõi.

## 🛠️ Yêu cầu hệ thống

* Python 3.10 trở lên.
* Các thư viện bổ trợ: `requests`, `colorama`.

## 🚀 Hướng dẫn cài đặt

1. **Tải mã nguồn về máy:**
   ```bash
   git clone https://github.com/tomnuongcay/mailtm-listener.git
   cd mailtm-listener
