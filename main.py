# -*- coding: utf-8 -*-
import os
import requests
import time
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

URLS = {
    "Relmada": "https://www.relmada.com/for-investors",
    # Добавляй другие компании по аналогии
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_latest_news(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    heading = soup.find("h3") or soup.find("h2") or soup.find("h1")
    date = soup.find("time")

    if heading and date:
        return {
            "title": heading.get_text(strip=True),
            "date": date.get_text(strip=True),
            "source": url
        }
    return None

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print("Ошибка отправки:", response.text)

def main():
    seen = {}
    while True:
        for name, url in URLS.items():
            update = get_latest_news(url)
            if update:
                key = (name, update["title"], update["date"])
                if key not in seen:
                    seen[key] = True
                    text = (
                        f"📌 Новость с {name}:\n"
                        f"<b>{update['title']}</b>\n"
                        f"Дата: {update['date']}\n"
                        f"{update['source']}"
                    )
                    send_telegram_message(text)
        time.sleep(4 * 60 * 60)  # каждые 4 часа

if __name__ == "__main__":
    main()
