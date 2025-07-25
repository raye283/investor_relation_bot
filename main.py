import time
import json
import requests
from utils import check_updates
import telebot

# Загрузка конфигурации
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["telegram_token"]
bot = telebot.TeleBot(TOKEN)
chat_id = config["telegram_chat_id"]

def main():
    sent_news = set()
    while True:
        updates = check_updates(config["urls"], sent_news)
        for update in updates:
            text = f"🆕 Новость с {update['source']}
📌 {update['title']}
📅 {update['date']}
🔗 {update['link']}"
            bot.send_message(chat_id, text)
            sent_news.add(update["link"])
        time.sleep(60 * 60 * 4)  # Проверка каждые 4 часа

if __name__ == "__main__":
    main()