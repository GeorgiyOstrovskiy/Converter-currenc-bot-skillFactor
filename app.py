from config import Token, keys
from extensions import Converter, APIException
import telebot


start_text = '''Вас, приветствует конвертер валют. Чтобы начать работу введите команду:
<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену> <количество первой валюты>
Можете воспользоваться помощью: /help'''

help_text = '''Чтобы начать работу введите команду:
<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену> <количество первой валюты>
Чтобы узнать дсотупные валюты: /values'''

bot = telebot.TeleBot(Token)


@bot.message_handler(commands=['start', ])
def command_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, start_text)


@bot.message_handler(commands=['help', ])
def command_help(message: telebot.types.Message):
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = message.text.split(' ')
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {keys[quote]} в {keys[base]} = {total_base}'
        bot.reply_to(message, text)


bot.polling(none_stop=True)
