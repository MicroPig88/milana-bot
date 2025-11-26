from flask import Flask, request
import asyncio
import os
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler
from bot.main import forward, BOT_TOKEN

flask_app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

@flask_app.route("/")
def home():
    return "Бот работает!", 200

@flask_app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    # перехватываем ВСЁ, что может содержать сообщение
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, forward))
    update = Update.de_json(request.get_json(force=True), bot)
    # обрабатываем апдейт через приложение
    asyncio.create_task(application.process_update(update))
    return "ok", 200


if __name__ == "__main__":
    # запускаем Flask
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))