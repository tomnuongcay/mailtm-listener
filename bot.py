import requests
import time
import json
import re
import random
import string
from colorama import Fore, Style, init

init(autoreset=True)

# --- CẤU HÌNH CỐ ĐỊNH ---
BOT_VERSION = "MAIL.TM LISTENER (VIP PROMAX ULTRA EDITION)"
AUTHOR_INFO = "Developer: t.me/tomnuongcay"
DEFAULT_PASSWORD = "123"

FIRST_NAMES = ["john", "jane", "alex", "chris", "sam", "ryan", "taylor", "jess", "mike", "dan"]
LAST_NAMES = ["smith", "jones", "brown", "davis", "wilson", "moore", "taylor", "miller", "clark", "hall"]

# ==============================================================================
# HÀM THU THẬP THÔNG TIN TỪ NGƯỜI DÙNG
# ==============================================================================

def get_user_timeout():
    """Hỏi người dùng về thời gian chờ mail tối đa (giây)."""
    while True:
        print(f"\n{Fore.YELLOW}⏱️  Bạn muốn đặt thời gian chờ code tối đa là bao nhiêu giây?")
        timeout_input = input(f"{Fore.CYAN}  > Nhập số giây (Mặc định 300s / 5 phút): {Style.RESET_ALL}")

        if not timeout_input.strip():
            return 300

        try:
            timeout = int(timeout_input)
            if timeout >= 30:
                return timeout
            else:
                print(f"{Fore.RED}❌ Lỗi: Thời gian chờ tối thiểu phải là 30 giây.")
        except ValueError:
            print(f"{Fore.RED}❌ Lỗi: Vui lòng nhập một số nguyên hợp lệ.")

def get_user_password():
    """Hỏi người dùng về mật khẩu tùy chỉnh."""
    print(f"\n{Fore.YELLOW}🔒 Bạn có muốn đặt mật khẩu tùy chỉnh cho mail tạm không? ({Fore.GREEN}y{Fore.YELLOW}/{Fore.RED}n{Fore.YELLOW})")
    choice = input(f"{Fore.CYAN}  > Nhập lựa chọn của bạn: {Style.RESET_ALL}").lower()

    if choice == 'y':
        while True:
            password = input(f"{Fore.CYAN}  > Nhập mật khẩu tùy chỉnh: {Style.RESET_ALL}").strip()
            if password:
                return password
            else:
                print(f"{Fore.RED}❌ Mật khẩu không được để trống.")

    print(f"{Fore.BLUE}  => Sử dụng mật khẩu mặc định: {DEFAULT_PASSWORD}{Style.RESET_ALL}")
    return DEFAULT_PASSWORD

# ==============================================================================
# LỚP XỬ LÝ MAIL.TM API
# ==============================================================================

class MailTMListener:
    def __init__(self, password, max_wait_time):
        self.api_url = "https://api.mail.tm"
        self.email = ""
        self.password = password
        self.max_wait_time = max_wait_time
        self.token = ""
        self.check_interval = 3

    def generate_human_username(self):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        num = str(random.randint(10, 999))

        formats = [
            f"{first}.{last}{num}",
            f"{first}{last}{num}",
            f"{last}{first}{num}"
        ]

        return random.choice(formats)

    def create_account(self):
        print(f"\n{Style.BRIGHT}{Fore.YELLOW}>>> 📧 BẮT ĐẦU TẠO TÀI KHOẢN MAIL.TM <<<")
        try:
            r = requests.get(f"{self.api_url}/domains", timeout=5)
            if r.status_code != 200 or not r.json().get('hydra:member'):
                print(f"{Fore.RED}❌ [ERROR] Lỗi lấy domain: {r.status_code}")
                return None

            # CHỌN DOMAIN NGẪU NHIÊN TỪ DANH SÁCH
            domains_list = [d['domain'] for d in r.json()['hydra:member']]
            if not domains_list:
                print(f"{Fore.RED}❌ [ERROR] Không tìm thấy domain khả dụng từ Mail.tm.")
                return None

            domain = random.choice(domains_list)

            username = self.generate_human_username()
            self.email = f"{username}@{domain}"

            payload = {"address": self.email, "password": self.password}
            headers = {"Content-Type": "application/json"}
            r = requests.post(f"{self.api_url}/accounts", json=payload, headers=headers, timeout=5)

            if r.status_code == 201:
                print(f"{Fore.GREEN}✅ [SUCCESS] Tạo email thành công!")
                print(f"   {Fore.CYAN}🔑 Email: {self.email}")
                print(f"   {Fore.CYAN}🔐 Pass:  {self.password}")

                return self.get_token()
            else:
                print(f"{Fore.RED}❌ [ERROR] Lỗi tạo tài khoản ({username}@{domain}): {r.status_code} - {r.text}")
        except Exception as e:
            print(f"{Fore.RED}❌ [ERROR] Lỗi kết nối khi tạo mail: {e}")
        return None

    def get_token(self):
        try:
            payload = {"address": self.email, "password": self.password}
            r = requests.post(f"{self.api_url}/token", json=payload, timeout=5)
            if r.status_code == 200:
                self.token = r.json()['token']
                return self.email
            else:
                 print(f"{Fore.RED}❌ [ERROR] Lỗi lấy token: {r.status_code} - {r.text}")
        except:
            pass
        return None

    def get_latest_code(self):
        print(f"\n{Fore.MAGENTA}⏳ Đang chờ Code (6 số) về hộp thư {Fore.CYAN}{self.email} {Fore.MAGENTA}(Tối đa {self.max_wait_time} giây)...")

        headers = {"Authorization": f"Bearer {self.token}"}
        start_time = time.time()

        while time.time() - start_time < self.max_wait_time:
            try:
                r = requests.get(f"{self.api_url}/messages", headers=headers, timeout=5)
                if r.status_code == 200:
                    messages = r.json().get('hydra:member')

                    if messages:
                        msg_id = messages[0]['id']

                        r_msg = requests.get(f"{self.api_url}/messages/{msg_id}", headers=headers, timeout=5)
                        data = r_msg.json()
                        text_body = data.get('text') or data.get('intro') or ""

                        match = re.search(r'\b\d{6}\b', text_body)
                        if match:
                            code = match.group(0)
                            print(Fore.BLUE + "\n" + "="*50)
                            print(f"{Style.BRIGHT}{Fore.YELLOW}✨ CODE ĐÃ VỀ! ✨")
                            print(f"{Fore.GREEN} Mã xác minh của bạn là: {Fore.RED}{code}")
                            print(Fore.BLUE + "="*50)
                            return code
            except:
                pass

            time.sleep(self.check_interval)

        print(f"\n{Fore.RED}❌ [TIMEOUT] Không tìm thấy code trong thời gian chờ ({self.max_wait_time} giây).")
        return None

# ==============================================================================
# HÀM CHẠY CHÍNH
# ==============================================================================

def print_header():
    title_width = 45
    title_line = Fore.WHITE + Style.BRIGHT + "=" * title_width

    centered_version = BOT_VERSION.center(title_width)
    centered_author = AUTHOR_INFO.center(title_width)

    print(f"\n{title_line}")
    print(f"{Fore.CYAN} {centered_version}")
    print(f"{Fore.CYAN} {centered_author}")
    print(f"{title_line}{Style.RESET_ALL}")

def main():
    print_header()

    user_password = get_user_password()
    user_timeout = get_user_timeout()

    while True:
        listener = MailTMListener(user_password, user_timeout)

        email = listener.create_account()

        if email:
            listener.get_latest_code()

        print(f"\n{Fore.YELLOW}❓ Bạn muốn tạo thêm email mới không? ({Fore.GREEN}y{Fore.YELLOW}/{Fore.RED}n{Fore.YELLOW})")
        choice = input(f"{Fore.CYAN}  > Nhập lựa chọn của bạn: {Style.RESET_ALL}").lower()

        if choice != 'y':
            print(f"\n{Fore.GREEN}👋 Cảm ơn đã sử dụng! Bot đã dừng lại.{Style.RESET_ALL}")
            break

        print(f"\n{Fore.BLUE}==================================================")
        print(f"{Fore.BLUE}            TIẾP TỤC VỚI LƯỢT CHẠY MỚI")
        print(f"{Fore.BLUE}=================================================={Style.RESET_ALL}")

if __name__ == "__main__":
    main()
