import json
import asyncio
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
logging.basicConfig(level=logging.INFO)

TOKEN = "7922676476:AAEApJ7cZdcHR9LoOlO6TaeVymIRcGOfyFg"
SUBSCRIBERS_FILE = "subscribers.json"

def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return []
    with open(SUBSCRIBERS_FILE, "r") as f:
        return json.load(f)

def save_subscribers(users):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(users, f)

# 🔧 Заглушки, заменишь на реальные функции
def get_telegram_news():
    return {
        "title": "🔥 Telegram-новость",
        "summary": "Это последняя новость из канала.",
        "link": "https://t.me/MLBBNews_sng"
    }

def get_official_mlbb_news():
    return {
        "title": "🌐 Официальная новость",
        "summary": "Это последняя новость с официальных источников.",
        "link": "https://m.mobilelegends.com/ru/news"
    }

# 👤 Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я буду присылать тебе новости MLBB. Напиши /subscribe для подписки.")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    users = load_subscribers()
    if user_id not in users:
        users.append(user_id)
        save_subscribers(users)
        await update.message.reply_text("✅ Ты подписан на новости MLBB.")
    else:
        await update.message.reply_text("ℹ️ Ты уже подписан.")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    users = load_subscribers()
    if user_id in users:
        users.remove(user_id)
        save_subscribers(users)
        await update.message.reply_text("🔕 Ты отписался от новостей.")
    else:
        await update.message.reply_text("Ты и так не подписан.")

# 📰 Команда news — кнопки выбора источника
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Telegram", callback_data="news_telegram")],
        [InlineKeyboardButton("🌐 Офиц. источник", callback_data="news_official")]
    ])
    await update.message.reply_text("Выберите источник новостей:", reply_markup=keyboard)

# 🔘 Обработка нажатия кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "news_telegram":
        news = get_telegram_news()
    elif query.data == "news_official":
        news = get_official_mlbb_news()
    else:
        await query.edit_message_text("❌ Неизвестная команда.")
        return

    text = f"📰 <b>{news['title']}</b>\n\n{news['summary']}\n\n🔗 <a href=\"{news['link']}\">Читать полностью</a>"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Открыть", url=news['link'])]])

    await query.edit_message_text(text=text, parse_mode="HTML", reply_markup=keyboard)

# 🔄 Фоновая рассылка (оставим без изменений)
async def send_news_periodically(app: Application):
    while True:
        await asyncio.sleep(3600)

# ▶ Запуск
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CallbackQueryHandler(button_handler))

    async def run():
        app.create_task(send_news_periodically(app))
        print("✅ Бот запущен и готов.")
        await app.run_polling()

    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(run())