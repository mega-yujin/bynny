# Bot handlers

import bot_functions
import telebot
from main import CONFIG
from utils import log_to_db

bot = telebot.TeleBot(CONFIG.TOKEN)


@bot.message_handler(commands=['rates'])  # nbrb official rates
def send_rates(message):
    answer = bot_functions.get_rates('bot')
    bot.send_message(message.chat.id, answer)
    log_to_db(message, answer)


@bot.message_handler(commands=['exchange'])  # stock exchange rates
def send_ex_rates(message):
    answer = bot_functions.get_exchange_rates('bot')
    bot.send_message(message.chat.id, answer)
    log_to_db(message, answer)


@bot.message_handler(commands=['price'])  # 1 byn cost in usd, eur and rur
def send_price(message):
    answer = bot_functions.get_byn_cost('bot')
    bot.send_message(message.chat.id, answer)
    log_to_db(message, answer)


@bot.message_handler(commands=['start'])  # start command
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.add('/rates')
    keyboard.add('/price')
    keyboard.add('/exchange')
    answer = 'Привет, ' + message.from_user.first_name + '\nВведи /rates и я скажу тебе актуальный курс белорусского ' \
                                                         'рубля. '
    bot.send_message(message.chat.id, answer, reply_markup=keyboard)
    log_to_db(message, answer)


@bot.message_handler(func=lambda message: True, content_types=['text'])  # random answer on any text message
def echo_message(message):
    answer = bot_functions.random_answer()
    bot.send_message(message.chat.id, answer)
    log_to_db(message, answer)
