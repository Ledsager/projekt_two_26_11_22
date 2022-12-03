from telegram import Update
from telegram.ext import ContextTypes

async def command_exch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    # await update.message.reply_text(f'перевод валют')
    