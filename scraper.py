import requests
import time

# بياناتك الخاصة
TOKEN = "8380499471:AAEjcV3pOVaIuQOOxdL-wCDgOjvFpivzI1s"
CHAT_ID = "8034521813"
API_URL = "https://api.allorigins.win/get?url=https://www.trackcasinos.com/api/sicbo/history"

def run_scraper():
    last_num = None
    start_time = time.time()
    while time.time() - start_time < 280: 
        try:
            response = requests.get(API_URL).json()
            raw_data = response['contents']
            current_num = raw_data.split('"result":')[1].split(',')[0].strip()
            if current_num != last_num:
                requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={current_num}")
                last_num = current_num
        except: pass
        time.sleep(25)

if __name__ == "__main__":
    run_scraper()
