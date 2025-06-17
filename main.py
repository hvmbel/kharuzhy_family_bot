import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")  # ОБЯЗАТЕЛЬНО: передай эту переменную в Cloud Run

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print("✅ Chat ID:", chat_id)
    await update.message.reply_text("Бот активен!")

def run_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    print("✅ Bot started")
    app_bot.run_polling()

@app.route("/")
def index():
    return "Flask: OK"

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
