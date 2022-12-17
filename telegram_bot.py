from dotenv import load_dotenv
from typing import List, Tuple, cast
import os
import logging
from save_data_log import *
from exchange_bot import *
from viewer_bot import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    ApplicationBuilder,
    MessageHandler,
    filters,
    InvalidCallbackData,

)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

START_ROUTES, END_ROUTES = range(2)
EXCH, RATE, SAVE_RATE, END_BOT, OVER_START = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправьте сообщение `/start`."""
    await update.message.reply_text(f'/exch - перевод валют\n/rate - курс валют\n/svrate - сохранение запроса\n/help\n')
    # await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def exchenge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show new choice of buttons"""
    user = update.message.from_user
    logger.info("Пользователь %s запросил перевод валют.", user.first_name)
    data = [user.first_name, user.id, 'запросил перевод валют']
    get_save_data_log(data)
    data_request = get_data_request_exchange_api()
    data_exchange = get_data_viewer_output(data_request)
    get_save_data_exchange(data_exchange)
    # updates = update.get_updates()

    await update.message.reply_text("введите валюту которую хотете обменять")
    await update.message.reply_text("Из какой в какую количество(пример: EUR USD 1000")
    text = update.message.text
    # context.user_data["choice"] = text
    print(text)
    text_split = text.split(' ')
    source = text_split[0]
    destination = text_split[1]
    amount = float(text_split[2])
    convert_currency(data_request, source, destination, amount)
    await update.message.reply_text(convert_currency(data_request, source, destination, amount))

async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    load_dotenv()
    user = update.message.from_user
    logger.info("Пользователь %s запросил курс валют.", user.first_name)
    data = [user.first_name, user.id, 'запросил курс валют']
    get_save_data_log(data)
    data_request = get_data_request_exchange_api()
    data_exchange = get_data_viewer_output(data_request)
    get_save_data_exchange(data_exchange)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=data_exchange)


async def save_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Пользователь %s сохранил курс валют.", user.first_name)
    data = [user.first_name, user.id, 'сохранил курс валют']
    get_save_data_log(data)
    await context.bot.send_document(chat_id=update.effective_chat.id,
                                    document=open('save_data_for_api.csv', 'rb'))
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Файл загружен")


async def command_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'/exch - перевод валют\n/rate - курс валют\n/svrate - сохранение запроса\n/help\n')


async def unknown(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Извините , такой команды нет.\n Введите команду.")


async def echo(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main() -> None:

    load_dotenv()
    secret_token = os.getenv('TOKEN')

    app = Application.builder().token(secret_token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler("exch", exchenge))
    app.add_handler(CommandHandler("rate", rate))
    app.add_handler(CommandHandler("svrate", save_rate))
    app.add_handler(CommandHandler("help", command_help))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), exchenge))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    app.run_polling()


if __name__ == "__main__":
    main()
