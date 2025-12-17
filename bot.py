import requests
import time
import re
import random
import string
import threading
from colorama import Fore, Style, init

init(autoreset=True)

BOT_VERSION = "MAIL.TM LISTENER (VIP PROMAX ULTRA EDITION)"
AUTHOR_INFO = "Developer: t.me/tomnuongcay"

class MailTMListener:
    def __init__(self):
        self.api_url = "https://api.mail.tm"
        self.email = ""
        self.token = ""
        self.domain = self.get_domain()
        self.skip_requested = False

    def get_domain(self):
        try:
            r = requests.get(f"{self.api_url}/domains", timeout=5)
            return random.choice([d['domain'] for d in r.json()['hydra:member']])
        except:
            return None

    def create_account(self):
        if not self.domain: return None
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        self.email = f"{username}@{self.domain}"
        try:
            payload = {"address": self.email, "password": password}
            r = requests.post(f"{self.api_url}/accounts", json=payload, timeout=5)
            if r.status_code == 201:
                t_r = requests.post(f"{self.api_url}/token", json=payload, timeout=5)
                self.token = t_r.json()['token']
                return self.email
        except:
            pass
        return None

    def listen_for_skip(self):
        input()
        self.skip_requested = True

    def get_latest_code(self):
        print(f"{Fore.MAGENTA}⏳ Đang chờ Code về hộp thư {Fore.CYAN}{self.email}")
        print(f"{Fore.YELLOW}👉 Nhấn [ENTER] để bỏ qua và đổi mail khác")

        headers = {"Authorization": f"Bearer {self.token}"}

        skip_thread = threading.Thread(target=self.listen_for_skip, daemon=True)
        skip_thread.start()

        while True:
            if self.skip_requested:
                print(f"{Fore.RED}⏩ Đã bỏ qua! Đang đổi mail mới")
                return "skip"

            try:
                r = requests.get(f"{self.api_url}/messages", headers=headers, timeout=5)
                messages = r.json().get('hydra:member')
                if messages:
                    msg_id = messages[0]['id']
                    r_msg = requests.get(f"{self.api_url}/messages/{msg_id}", headers=headers, timeout=5)
                    text_body = r_msg.json().get('text') or r_msg.json().get('intro') or ""
                    match = re.search(r'\b\d{6}\b', text_body)
                    if match:
                        code = match.group(0)
                        print(Fore.BLUE + "\n" + "="*50)
                        print(f"{Style.BRIGHT}{Fore.YELLOW}✨ CODE ĐÃ VỀ! ✨")
                        print(f"{Fore.GREEN} Mã xác minh của bạn là: {Fore.RED}{Style.BRIGHT}{code}")
                        print(Fore.BLUE + "="*50)
                        return code
            except:
                pass
            time.sleep(2)

def print_header():
    title_width = 50
    print(f"\n{Fore.WHITE}{Style.BRIGHT}{'=' * title_width}")
    print(f"{Fore.CYAN}{BOT_VERSION.center(title_width)}")
    print(f"{Fore.CYAN}{AUTHOR_INFO.center(title_width)}")
    print(f"{Fore.WHITE}{Style.BRIGHT}{'=' * title_width}\n")

def main():
    while True:
        print_header()
        listener = MailTMListener()
        email = listener.create_account()

        if email:
            print(f"{Fore.GREEN}✅ Đã tạo thành công: {Fore.CYAN}{email}")
            result = listener.get_latest_code()

        print(f"\n{Fore.BLUE}🔄 Đang chuẩn bị Mail tiếp theo")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}👋 Đã dừng chương trình.")
        
