import os, logging
import uvicorn
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters
from contextlib import asynccontextmanager
from bot.main import forward, BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(MessageHandler(filters.ALL, forward))

@asynccontextmanager
async def lifespan(app: FastAPI):
    await application.initialize()
    logging.info("Telegram Application initialized")
    yield
    await application.shutdown()
    logging.info("Telegram Application shutdown")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Бот работает!"}

@app.post(f"/webhook/{BOT_TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    logging.info(f"Incoming update: {data}")
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))