from config import keys, header
import json
import requests


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote, base, amount):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        if amount < 0:
            raise APIException('Сумма должна быть больше 0')

        response = requests.get(f'https://api.apilayer.com/fixer/convert?'
                                f'to={base_ticker}&from={quote_ticker}&amount={amount}', headers=header)
        total_base = json.loads(response.content)['result']

        return total_base
