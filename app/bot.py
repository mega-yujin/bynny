from config import bot
from utils import log_to_db
import bot_service


@bot.message_handler(commands=['rates'])  # nbrb official rates
def send_rates(message):
    rates = bot_service.get_rates()
    if len(rates) != 1:
        answer = str()
        for currency in rates:
            answer += currency + '\n'
    else:
        answer = rates[0]
    bot.send_message(message.chat.id, answer.rstrip('\n'))
    log_to_db(message, answer)


@bot.message_handler(commands=['exchange'])  # stock exchange rates
def send_ex_rates(message):
    # f'Результаты торгов:\n {usd} \n {eur} \n {rur} \n {cny}'
    rates = bot_service.get_exchange_rates()
    if len(rates) != 1:
        answer = "Результаты торгов:\n"
        for currency in rates:
            answer += currency + '\n'
    else:
        answer = rates[0]
    bot.send_message(message.chat.id, answer.rstrip('\n'))
    log_to_db(message, answer)


@bot.message_handler(commands=['price'])  # 1 byn cost in usd, eur and rur
def send_price(message):
    # f'1 BYN стоит:\n {str(usd)} USD\n {str(eur)} EUR\n {str(rur)} RUR'
    prices = bot_service.get_byn_cost()
    if len(prices) != 1:
        answer = "1 BYN стоит:\n"
        for currency in prices:
            answer += currency + '\n'
    else:
        answer = prices[0]
    bot.send_message(message.chat.id, answer.rstrip('\n'))
    log_to_db(message, answer)


@bot.message_handler(commands=['start'])  # start command
def start(message):
    keyboard = bot.types.ReplyKeyboardMarkup(True)
    keyboard.add('/rates')
    keyboard.add('/price')
    keyboard.add('/exchange')
    answer = f'Привет, {message.from_user.first_name}\nВведи /rates и я скажу тебе актуальный курс белорусского рубля.'
    bot.send_message(message.chat.id, answer, reply_markup=keyboard)
    log_to_db(message, answer)


@bot.message_handler(func=lambda message: True, content_types=['text'])  # random answer on any text message
def echo_message(message):
    answer = bot_service.random_answer()
    bot.send_message(message.chat.id, answer)
    log_to_db(message, answer)
