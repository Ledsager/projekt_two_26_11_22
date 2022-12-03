from datetime import datetime as dt

def get_save_data_log(data):
   now = dt.now()
   with open('save_data_log.csv', 'a', encoding='utf-8') as my_file:
      my_file.write('{} запрос информации {} Пользователь {} ид {} - {}\n'
                     .format(now.strftime("%Y-%m-%d"), now.strftime('%H:%M'), data[0],data[1],data[2]))