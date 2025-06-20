from kiteconnect import KiteConnect
import requests
import yagmail
import time
import schedule

# --- CONFIG SECTION ---

API_KEY = "jmagkgcalw4m3wbu"
API_SECRET = "51k1u4j721foclugsj8fsn1kjj1cllbk"
ACCESS_TOKEN = "NvEHYfv2epybqhOWCEjhPp6vhy94DUEZ"

PNL_ALERT_LOW = -2000
PNL_ALERT_HIGH = 3000

# Telegram
TELEGRAM_BOT_TOKEN = "7873496922:AAG_9pP33CD4GA8SSYSxz5TCRV_4aVzHylY"
TELEGRAM_CHAT_ID = "972261464"

# Email
EMAIL_USER = "ksachin.devil.inside@gmail.com"
EMAIL_PASSWORD = "9892569595"
EMAIL_RECEIVER = "shkinvesting@gmail.com"

# --- FUNCTIONS ---

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

last_alert_pnl = None

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, data=data)

def send_email(subject, body):
    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)
    yag.send(to=EMAIL_RECEIVER, subject=subject, contents=body)

def check_pnl():
    global last_alert_pnl
    try:
        positions = kite.positions()
        pnl = positions['net'][0]['pnl'] if positions['net'] else 0

        print(f"Current PNL: ₹{pnl}")

        if pnl <= PNL_ALERT_LOW or pnl >= PNL_ALERT_HIGH:
            if last_alert_pnl != pnl:  # avoid repeat alerts
                message = f"🔔 PNL Alert: ₹{pnl}\nThreshold crossed."
                send_telegram(message)
                send_email("PNL Alert Triggered", message)
                last_alert_pnl = pnl
    except Exception as e:
        print("Error:", e)

# Schedule check every 15 minutes
schedule.every(15).minutes.do(check_pnl)

while True:
    schedule.run_pending()
    time.sleep(60)
