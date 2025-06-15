from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID", "0"))

KIDS = [
    {"name": "Петя", "username": "@petya"},
    {"name": "Маша", "username": "@masha"}
]

current_index = 0
photos_received = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Chat ID:", update.effective_chat.id)
    await update.message.reply_text("Бот активен!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global photos_received
    if update.message.from_user.username == KIDS[current_index]["username"].replace("@", ""):
        photos_received.append(update.message.photo)
        if len(photos_received) == 3:
            await update.message.reply_text("✅ Получено 3 фото. Молодец!")
            await notify_next(update, context)

async def notify_kid(context: ContextTypes.DEFAULT_TYPE):
    global photos_received
    photos_received = []
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"{KIDS[current_index]['username']}, напоминание! Сегодня твое дежурство. Жду 3 фото до 22:15!"
    )

async def check_photos(context: ContextTypes.DEFAULT_TYPE):
    if len(photos_received) < 3:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f"{KIDS[current_index]['username']}, ты не прислал(а) 3 фото. Дежуришь снова завтра. Убери посуду сегодня или завтра утром!"
        )

async def notify_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_index
    current_index = (current_index + 1) % len(KIDS)
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"🔔 Завтра дежурит {KIDS[current_index]['username']}"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.job_queue.run_daily(notify_kid, time(hour=21, minute=45))
    app.job_queue.run_daily(check_photos, time(hour=22, minute=15))

    app.run_polling()

if __name__ == "__main__":
    main()
