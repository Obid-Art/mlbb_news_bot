from telethon import TelegramClient, events
from telegram import Bot
from bot_utils import load_subscribers
import asyncio

# 🔐 Telegram API
api_id = 27880303
api_hash = "e68a3ac3d1f64e81b1ff01f6c58d2060"
session_name = "mlbb_listener"

# 🤖 Bot API
bot_token = "7922676476:AAEApJ7cZdcHR9LoOlO6TaeVymIRcGOfyFg"

# 🔄 Канал-источник (без @)
channel_username = "MLBBNews_sng"

# ▶️ Инициализация
client = TelegramClient(session_name, api_id, api_hash)
bot = Bot(token=bot_token)

@client.on(events.NewMessage(chats=channel_username))
async def handler(event):
    message = event.message
    text = event.raw_text
    subscribers = load_subscribers()

    if not subscribers:
        print("⚠️ Нет подписчиков в базе.")
        return

    for chat_id in subscribers:
        try:
            await bot.copy_message(chat_id=chat_id,
                                   from_chat_id=message.chat_id,
                                   message_id=message.id)
            print(f"📨 Переслано с медиа в {chat_id}")
        except Exception as e:
            print(f"❌ Ошибка при отправке в {chat_id}: {e}")

async def main():
    await client.start()
    print("✅ Listener запущен и следит за новыми постами...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())