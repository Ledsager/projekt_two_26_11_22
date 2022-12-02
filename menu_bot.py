from telegram import Update
from telegram.ext import ContextTypes

async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Я бот, привет.")

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