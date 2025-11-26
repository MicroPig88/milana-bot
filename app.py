from flask import Flask
import threading
from .main import main as start_bot # импортируем твою функцию main

flask_app = Flask(__name__)


@flask_app.route("/")
def home():
    return "Бот работает!", 200


if __name__ == "__main__":
    # запускаем Telegram-бота в отдельном потоке
    threading.Thread(target=start_bot).start()

    # запускаем Flask
    import os

    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))