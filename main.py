import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Логгирование в stdout (чтобы видеть в Google Cloud)
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logging.info(f"Chat ID: {chat_id}")
    await update.message.reply_text("Бот активен!")

# Главное: никаких потоков!
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()  # <-- запускается напрямую, без asyncio, без threading

if __name__ == '__main__':
    main()
