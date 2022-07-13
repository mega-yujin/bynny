import random
import requests
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}
ALL_DAILY_RATES = 'https://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
CURRENCY_RATE = 'https://www.nbrb.by/api/exrates/rates/'
CURRENCY_MARKET = 'https://banki24.by/exchange/currencymarket'

CURRENCY_CODES = {'AUD': 440, 'AMD': 510, 'BGN': 441, 'UAH': 449, 'DKK': 450, 'USD': 431, 'EUR': 451, 'PLN': 452,
                  'JPY': 508, 'IRR': 461, 'ISK': 453, 'CAD': 371, 'CNY': 462, 'KWD': 394, 'MDL': 454, 'NZD': 448,
                  'NOK': 455, 'RUB': 456, 'XDR': 457, 'SGD': 421, 'KGS': 458, 'KZT': 459, 'TRY': 460, 'GBP': 429,
                  'CZK': 463, 'SEK': 464, 'CHF': 426}


def get_data(url: str, headers=None) -> requests.Response:
    if headers is None:
        headers = HEADERS
    try:
        response = requests.get(url, headers=headers, timeout=(3, 25))
    except requests.exceptions.ConnectionError as e:
        response = ('# Connection error #',)
        print(e)
    except requests.exceptions.HTTPError as e:
        response = ('# HTTP error #',)
        print(e)
    except requests.exceptions.Timeout as e:
        response = ('# Timeout error #',)
        print(e)
    return response


def get_currency(currency_id: int) -> dict:
    response = get_data(CURRENCY_RATE + str(currency_id))
    return response.json()


def get_all_currencies() -> list[dict]:
    return get_data(ALL_DAILY_RATES).json()


def format_currency_rates(*currency: dict) -> list:
    return [f'{item.get("Cur_Name")}: {item.get("Cur_OfficialRate")} BYN' for item in currency]


def format_byn_cost(*currency: dict) -> list:
    return [f'{(item.get("Cur_Scale") / item.get("Cur_OfficialRate")):.6f} {item.get("Cur_Name")}' for item in currency]


def get_rates() -> list:
    """
    returns official byn rates from nbrb.by API
    """
    rates = None
    try:
        usd = get_currency(CURRENCY_CODES.get('USD'))
        eur = get_currency(CURRENCY_CODES.get('EUR'))
        rur = get_currency(CURRENCY_CODES.get('RUB'))
        nok = get_currency(CURRENCY_CODES.get('NOK'))

        rates = format_currency_rates(usd, eur, rur, nok)

    except requests.exceptions.ConnectionError as e:
        rates = ('# Connection error #',)
        print(e)
    except requests.exceptions.HTTPError as e:
        rates = ('# HTTP error #',)
        print(e)
    except requests.exceptions.Timeout as e:
        rates = ('# Timeout error #',)
        print(e)

    return rates


# get byn cost in usd, eur, rur from nbrb.by API
def get_byn_cost() -> list:
    try:
        r = get_data(ALL_DAILY_RATES, HEADERS).json()

        usd = get_currency(CURRENCY_CODES.get('USD'))
        eur = get_currency(CURRENCY_CODES.get('EUR'))
        rur = get_currency(CURRENCY_CODES.get('RUB'))

        byn_cost = format_byn_cost(usd, eur, rur)

    except requests.exceptions.ConnectionError as err:
        byn_cost = ('# Connection error #',)
        print(err)
    except requests.exceptions.HTTPError as err:
        byn_cost = ('# HTTP error #',)
        print(err)
    except requests.exceptions.Timeout as err:
        byn_cost = ('# Timeout error #',)
        print(err)

    return byn_cost


# get stock exchange rates with BeautifulSoup
def get_exchange_rates():
    try:
        page = get_data(CURRENCY_MARKET, HEADERS)
        soup = BeautifulSoup(page.text, "html.parser")
        raw_currency_value = soup.select('p.text-center.h1.mt-0')
        raw_currency_change = soup.select('span.pull-left.label')

        currency_value = [
            item.text.replace('\n', '').replace('\t', '') for item in raw_currency_value
        ]
        currency_change = [
            item.text.replace('\n', '').replace('\t', '').replace('&plus', '+') for item in raw_currency_change
        ]

        usd = f'1 USD: {currency_value[0]} ({currency_change[0]})'
        eur = f'1 EUR: {currency_value[1]} ({currency_change[1]})'
        rur = f'100 RUR: {currency_value[2]} ({currency_change[2]})'
        cny = f'10 CNY: {currency_value[3]} ({currency_change[3]})'

        exchange_rates = (usd, eur, rur, cny)

    except requests.exceptions.ConnectionError as err:
        exchange_rates = ('# Connection error #',)
        print(err)
    except requests.exceptions.HTTPError as err:
        exchange_rates = ('# HTTP error #',)
        print(err)
    except requests.exceptions.Timeout as err:
        exchange_rates = ('# Timeout error #',)
        print(err)

    return exchange_rates


# random bot answer
def random_answer():
    ans = ('Прошу прощения, создатель научил меня только искать курсы валют :(',
           'Извини, я тебя не понимаю, я только учусь!',
           'Хвала создателю!!',
           'Извини, попробуй спросить позже.',
           'Человек, я тебя не понимаю.')

    return random.choice(ans)
