import os
from datetime import time
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CHAT_ID = int(os.environ.get("CHAT_ID", "0"))

KIDS = [
    {"username": "@svetlana_kharuzhaya"},
    {"username": "@hvmbel"},
]
current_index = 0
photos_received = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Chat ID:", update.effective_chat.id)
    await update.message.reply_text("Бот активен!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global photos_received
    if update.message:
        photos_received.append(update.message.photo[-1].file_id)
    if len(photos_received) < 3:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f"{KIDS[current_index]['username']}, ты не прислал(а) 3 фото. Дежурный!"
        )

async def notify_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_index
    current_index = (current_index + 1) % len(KIDS)
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"🔔 Завтра дежурит {KIDS[current_index]['username']}"
    )

async def notify_kid(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=f"⏰ Напоминание: сегодня дежурит {KIDS[current_index]['username']}"
    )

async def check_photos(context: ContextTypes.DEFAULT_TYPE):
    if len(photos_received) < 3:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=f"⚠️ {KIDS[current_index]['username']}, ты не прислал(а) 3 фото до 22:15!"
        )

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.job_queue.run_daily(notify_kid, time=time(hour=21, minute=45))
    app.job_queue.run_daily(check_photos, time=time(hour=22, minute=15))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
