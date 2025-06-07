# bot_utils.py
from telegram import Bot
import json

BOT_TOKEN = '7922676476:AAEApJ7cZdcHR9LoOlO6TaeVymIRcGOfyFg'
bot = Bot(token=BOT_TOKEN)

def load_subscribers():
    try:
        with open("subscribers.json", "r") as f:
            return json.load(f)
    except:
        return []

def send_post_to_subscribers(text):
    subscribers = load_subscribers()
    for user_id in subscribers:
        try:
            bot.send_message(chat_id=user_id, text=text)
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user_id}: {e}")
