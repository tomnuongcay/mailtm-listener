import requests
import time
import re
import random
import string
import sys
import select
import termios
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

    def get_domain(self):
        try:
            r = requests.get(f"{self.api_url}/domains", timeout=5)
            return random.choice([d['domain'] for d in r.json()['hydra:member']])
        except:
            return None

    def create_account(self):
        if not self.domain: return None
        user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        pas = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        self.email = f"{user}@{self.domain}"
        try:
            payload = {"address": self.email, "password": pas}
            r = requests.post(f"{self.api_url}/accounts", json=payload, timeout=5)
            if r.status_code == 201:
                t_r = requests.post(f"{self.api_url}/token", json=payload, timeout=5)
                self.token = t_r.json()['token']
                return self.email
        except:
            pass
        return None

    def flush_input(self):
        try:
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except:
            pass

    def is_skip_pressed(self):
        if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
            sys.stdin.readline()
            return True
        return False

    def get_latest_code(self):
        print(f"{Fore.MAGENTA}⏳ Đang chờ Code về hộp thư {Fore.CYAN}{self.email}")
        print(f"{Fore.YELLOW}👉 Nhấn [ENTER] để đổi mail khác")
        
        self.flush_input()
        headers = {"Authorization": f"Bearer {self.token}"}
        
        while True:
            if self.is_skip_pressed():
                print(f"{Fore.RED}⏩ Đã nhận lệnh Skip! Đang đổi mail mới")
                return "skip"
                
            try:
                r = requests.get(f"{self.api_url}/messages", headers=headers, timeout=2)
                if r.status_code == 200:
                    messages = r.json().get('hydra:member')
                    if messages:
                        m_id = messages[0]['id']
                        r_msg = requests.get(f"{self.api_url}/messages/{m_id}", headers=headers, timeout=2)
                        body = r_msg.json().get('text') or r_msg.json().get('intro') or ""
                        match = re.search(r'\b\d{6}\b', body)
                        if match:
                            code = match.group(0)
                            print(Fore.BLUE + "\n" + "="*50)
                            print(f"{Style.BRIGHT}{Fore.YELLOW}✨ CODE ĐÃ VỀ! ✨")
                            print(f"{Fore.GREEN} Mã xác minh là: {Fore.RED}{Style.BRIGHT}{code}")
                            print(Fore.BLUE + "="*50)
                            return code
            except:
                pass
            
            time.sleep(1.5)

def print_header():
    tw = 50
    print(f"\n{Fore.WHITE}{Style.BRIGHT}{'=' * tw}")
    print(f"{Fore.CYAN}{BOT_VERSION.center(tw)}")
    print(f"{Fore.CYAN}{AUTHOR_INFO.center(tw)}")
    print(f"{Fore.WHITE}{Style.BRIGHT}{'=' * tw}\n")

def main():
    while True:
        print_header()
        bot = MailTMListener()
        email = bot.create_account()

        if email:
            print(f"{Fore.GREEN}✅ Đã tạo: {Fore.CYAN}{email}")
            res = bot.get_latest_code()
            
            if res != "skip":
                print(f"\n{Fore.YELLOW}🔄 Hoàn thành! Tự động chuyển mail mới sau 3 giây...")
                time.sleep(3)
        else:
            print(f"{Fore.RED}❌ Lỗi kết nối API, đang thử lại...")
            time.sleep(2)
        
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}👋 Đã dừng chương trình.")
