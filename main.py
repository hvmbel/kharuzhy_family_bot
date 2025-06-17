import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ==== Конфигурация ====
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ==== Telegram логика ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print("Chat ID:", chat_id)
    await update.message.reply_text("Бот активен!")

def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Starting bot polling loop")
    application.run_polling()

# ==== Flask приложение ====
app = Flask(__name__)

@app.route("/")
def index():
    return "Бот работает!"

# ==== Запуск ====
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    print("Flask app started")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
