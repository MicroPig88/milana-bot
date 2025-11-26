import os

from telegram import Update
from telegram.ext import ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"] # токен бота от BotFather
TARGET_CHAT_ID = int(os.environ["TARGET_CHAT_ID"])# ID чата, куда пересылать сообщения


async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылка сообщений в нужный чат"""

    msg = update.message or update.channel_post

    if msg is None:
        return

    # --- ТЕКСТ ---
    await context.bot.forward_message(
        chat_id=TARGET_CHAT_ID,
        from_chat_id=msg.chat.id,
        message_id=msg.message_id
    )