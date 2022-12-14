import copy
from dotenv import load_dotenv
import os
from datetime import datetime as dt
import requests

def get_data_viewer_output(data):
    data_exchange = copy.deepcopy(data)
    date_now = dt.now().strftime('%Y-%m-%d %H:%M')
    for list_element in data_exchange:
        list_element.insert(0, '                ')

    header_file_csv = ['Код валюты', 'Курс']
    header_file_csv.insert(0, date_now)
    res = [*[header_file_csv], *data_exchange]
    # print(res)
    # len_1 = len(header_file_csv[0])
    # len_2 = len(header_file_csv[0])
    # len_3 = len(header_file_csv[0])
    text=""
    for col in res:
        for row in col:
            text = text + f"  {row}"
            print(row, end=' ')
        print()
        text += "\n"
    # print(text)
    return text

def get_data_request_exchange_api() -> list:

    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/RUB'
    # запрос api в формате json

    response = requests.get(f'{url}').json()
    # получение словаря
    currencies = dict(response['conversion_rates'])
    currencies = [list(i) for i in currencies.items()  # преобразование словаря в список
                  if ('USD' in i) or ('EUR' in i) or ('KZT' in i) or ('TRY' in i) or ('UZS' in i) or ('AZN' in i)]
    return currencies

def main():
    data = get_data_request_exchange_api()
    get_data_viewer_output(data)

if __name__ == "__main__":
    main()

# data = [['2022-12-04 01:31', 'Код валюты', 'Курс'], ['', 'AZN', 0.02747], ['', 'EUR', 0.01533],
#             ['', 'KZT', 7.5983], ['', 'TRY', 0.2996], ['', 'USD', 0.01612], ['', 'UZS', 181.9757]]
# |'2022-12-04 01:31'|, 'Код валюты'|, 'Курс'|
# |''                |,    'AZN',   |0.02747 |
# '', 'EUR', 0.01533
