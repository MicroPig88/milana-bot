from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8569063130:AAG8-QflWqLWmPeDgop0ltodQ_x2HhQkuSQ"  # токен бота от BotFather
TARGET_CHAT_ID = -1003467562734# ID чата, куда пересылать сообщения


async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылка сообщений в нужный чат"""

    msg = update.message or update.channel_post

    if msg is None:
        return

    # --- ТЕКСТ ---
    await context.bot.forward_message(
        chat_id=TARGET_CHAT_ID,
        from_chat_id=update.effective_chat.id,
        message_id=update.message.message_id
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # перехватываем ВСЁ, что может содержать сообщение
    app.add_handler(MessageHandler(filters.ALL, forward))
    app.run_polling()

if __name__ == "__main__":
    main()