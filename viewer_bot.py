from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime as dt


async def command_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(f'rate ready')
    data=[['USD', 60.3866], ['EUR', 62.7814], ['KZT', 13.0523], ['TRY', 3.2426], ['UZS', 53.808], ['AZN', 35.5215]]
    # data_exchange = copy.deepcopy(data)
    date_now = dt.now().strftime('%Y-%m-%d %H:%M')
    # root = tkinter.Tk()
    await update.message.reply_text(f'Курс валют на сегодня - {date_now}')
    frame_color = '#4ca8ff'  # палитра или рал цвета
    # btn2 = Button(root, width=40, text="Перевод валют", command=exchange_convert_t)
    # btn2.pack(side=TOP, padx=10, pady=10)
    for list_element in data:
        list_element.insert(0, '')

    if len(data[0]) > 3:
        header_file_csv = ['Код', 'Курс', 'Единиц']
        header_file_csv.insert(0, date_now)
    else:  # len(data_exchange[0]) > 2:
        header_file_csv = ['Код валюты', 'Курс']
        header_file_csv.insert(0, date_now)

    res = [*[header_file_csv], *data]
    print(res, end='')
    await update.message.reply_text(res)
    # r и c указывают нам место расположения меток
    # r = 0
    # for col in res:
    #     for row in col:
    #         # добавил стиль в меню и цвет
    #         # await update.message.reply_text(f'{row} ')
    #         print()
