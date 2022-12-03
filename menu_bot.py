
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

async def start(update, context):
    keyboard = [
            [
                InlineKeyboardButton("Option 1", callback_data="1"),
                InlineKeyboardButton("Option 2", callback_data="2"),
            ],
            [InlineKeyboardButton("Option 3", callback_data="3")],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")

async def echo(update, context):
    output_input = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text=output_input)

async def unknown(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Извините , такой команды нет.\n Введите команду.")

async def command_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'/exch - перевод валют\n/rate - курс валют\n/help\n')

# async def inline_caps(update, context):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = []
#     results.append(
#         InlineQueryResultArticle(
#             id=query.upper(),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     await context.bot.answer_inline_query(update.inline_query.id, results)

# async def process_help_command(message: types.Message):
#     msg = TextDoc(BOLD('Я могу ответить на следующие команды:'),
#                '/voice', '/photo', '/group', '/note', '/file, /testpre', sep='\n')
#     await message.reply(msg, parse_mode=ParseMode.MARKDOWN)