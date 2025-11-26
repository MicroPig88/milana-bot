from fastapi import FastAPI, Request
import uvicorn
from contextlib import asynccontextmanager
import asyncio
import os
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters
from bot.main import forward, BOT_TOKEN


bot = Bot(token=BOT_TOKEN)

# создаём приложение Telegram один раз
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(MessageHandler(filters.ALL, forward))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код запуска (startup)
    await application.start()
    logging.info("Telegram bot started")
    yield
    # Завершение работы Telegram приложения
    await application.stop()
    logging.info("Telegram bot stopped")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Бот работает!"}

@app.post(f"/webhook/{BOT_TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    # безопасная асинхронная обработка апдейта
    await application.process_update(update)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))