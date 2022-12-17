import pandas as pd


def convert_currency(data, source, destination, amount):

    df = pd.DataFrame(data)[0].tolist()


    source_f = [i[1] for i in data if source == i[0]]
    destination_f = [i[1] for i in data if destination == i[0]]
    # print(df)
    result = (source_f[0] / destination_f[0]) * amount
    return result


def main_test():
    # data_exchange = list(copy.deepcopy(data))
    # global data_exchange
    # data=[['USD', 60.3866], ['EUR', 62.7814], ['KZT', 13.0523], ['TRY', 3.2426], ['UZS', 53.808], ['AZN', 35.5215]]
    # data = dre.get_data_request_exchange_api()

    convert_currency()


if __name__ == '__main__':
    main_test()
