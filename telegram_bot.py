from dotenv import load_dotenv
import os
import logging
from save_data_log import get_save_data_log
from exchange_bot import *
from viewer_bot import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    ApplicationBuilder,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
EXCH, RATE, SAVE_RATE, END_BOT, OVER_START = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отправьте сообщение `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("Пользователь %s запустил чат-бот.", user.first_name)
    data=[user.first_name,user.id,'запустил чат-бот']
    get_save_data_log(data)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Перевод валют", callback_data=str(EXCH)),
            InlineKeyboardButton("Курс валют", callback_data=str(RATE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Выберите действие", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Перевод валют", callback_data=str(EXCH)),
            InlineKeyboardButton("Курс валют", callback_data=str(RATE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(text="Продолжим. Выберите действие.", reply_markup=reply_markup)
    return START_ROUTES


async def exchenge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    user = query.from_user
    logger.info("Пользователь %s запросил перевод валют.", user.first_name)
    data=[user.first_name,user.id,'запросил перевод валют']
    get_save_data_log(data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Сохранить курс валют?", callback_data=str(SAVE_RATE)),
            InlineKeyboardButton("4", callback_data=str(EXCH)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="First CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    
    print(query)



    return START_ROUTES


async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    user = query.from_user
    logger.info("Пользователь %s запросил курс валют.", user.first_name)
    data=[user.first_name,user.id,'запросил курс валют']
    get_save_data_log(data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data=str(SAVE_RATE)),
            InlineKeyboardButton("Нет", callback_data=str(OVER_START)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Сохранить курс валют?", reply_markup=reply_markup
    )
    return START_ROUTES


async def save_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""
    query = update.callback_query
    user = query.from_user
    logger.info("Пользователь %s сохранил курс валют.", user.first_name)
    data=[user.first_name,user.id,'сохранил курс валют']
    get_save_data_log(data)
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Перейти в начало?", callback_data=str(OVER_START)),
            InlineKeyboardButton("Закончить?", callback_data=str(END_BOT)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Third CallbackQueryHandler. Do want to start over?", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return END_ROUTES


async def four(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Курс валют", callback_data=str(RATE)),
            InlineKeyboardButton("Сохранить курс валют", callback_data=str(SAVE_RATE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Fourth CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    user = query.from_user
    logger.info("Пользователь %s покинул чат.", user.first_name)
    data=[user.first_name,user.id,'покинул чат']
    get_save_data_log(data)   
    await query.answer()
    await query.edit_message_text(text="Всего хорошего!")
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    load_dotenv()
    secret_token = os.getenv('TOKEN')

    application = Application.builder().token(secret_token).build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(exchenge, pattern="^" + str(EXCH) + "$"),
                CallbackQueryHandler(rate, pattern="^" + str(RATE) + "$"),
                CallbackQueryHandler(save_rate, pattern="^" + str(SAVE_RATE) + "$"),
                CallbackQueryHandler(start_over, pattern="^" + str(OVER_START) + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(start_over, pattern="^" + str(OVER_START) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(END_BOT) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()