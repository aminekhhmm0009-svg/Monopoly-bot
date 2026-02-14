import telebot
import requests
from bs4 import BeautifulSoup
import time

# --- البيانات التي قدمتها ---
TOKEN = '8520192110:AAH5N9k16MwijB06v0iiV6mB-iSCI6blq0Q'
CHAT_ID = '8034521813'
bot = telebot.TeleBot(TOKEN)

# استراتيجية Black Diamond 💎
STRATEGY = {
    '2 Rolls': {'threshold': 12, 'active': False},
    '4 Rolls': {'threshold': 45, 'active': False}
}

def get_data():
    url = "https://tracksino.com/monopoly"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        stats = {}
        rows = soup.find_all('tr')
        for row in rows:
            t = row.get_text()
            if '2 Rolls' in t and 'Since' in t:
                stats['2 Rolls'] = int(''.join(filter(str.isdigit, t.split('Since')[-1])))
            if '4 Rolls' in t and 'Since' in t:
                stats['4 Rolls'] = int(''.join(filter(str.isdigit, t.split('Since')[-1])))
        return stats
    except:
        return None

def main():
    print("البوت بدأ العمل ومراقبة استراتيجية Black Diamond...")
    last_gaps = {'2 Rolls': -1, '4 Rolls': -1}
    
    while True:
        data = get_data()
        if data:
            for game in STRATEGY:
                gap = data.get(game, 0)
                
                # إشارة النجاح (الفوز)
                if STRATEGY[game]['active'] and gap == 0:
                    bot.send_message(CHAT_ID, f"✅ **تم قنص فرصة بنجاح!**\n🎯 النتيجة: {game}\n\nBOOM 🔥💎")
                    STRATEGY[game]['active'] = False
                
                # إشارة القنص (التنبيه)
                elif gap >= STRATEGY[game]['threshold'] and not STRATEGY[game]['active']:
                    if gap != last_gaps[game]:
                        msg = f"⚠️ **تم قنص فرصة**\n🎯 الهدف: {game}\n📊 الفجوة الحالية: {gap}\n💎 استراتيجية: Black Diamond\n\n💡 ابدأ الرهان الآن!"
                        bot.send_message(CHAT_ID, msg)
                        STRATEGY[game]['active'] = True
                        last_gaps[game] = gap
                
                elif gap == 0:
                    STRATEGY[game]['active'] = False
        
        time.sleep(25) # فحص كل 25 ثانية لضمان الدقة

if __name__ == "__main__":
    main()
