import requests
import time
from bs4 import BeautifulSoup
import os

PUSHOVER_USER = os.environ["PUSHOVER_USER"]
PUSHOVER_TOKEN = os.environ["PUSHOVER_TOKEN"]

URL = "https://www.xtb.com/pl/recommendations"
last_trade = ""

def send_push(title, message):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "title": title,
            "message": message,
            "priority": 1
        }
    )

def get_trade():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text("\n")

    capture = False
    block = []

    for line in text.split("\n"):
        line = line.strip()

        if "Zagranie dnia" in line:
            capture = True

        if capture and line:
            block.append(line)

        if capture and "TP" in line:
            break

    return "\n".join(block) if block else None

while True:
    try:
        trade = get_trade()

        if trade and trade != last_trade:
            last_trade = trade
            send_push("XTB – Zagranie dnia", trade)

    except Exception as e:
        print("Error:", e)

    time.sleep(900)
