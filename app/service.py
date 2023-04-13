import random
import requests
import logging
from bs4 import BeautifulSoup
from typing import Union, Optional
from dataclasses import dataclass

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}
ALL_DAILY_RATES = 'https://www.nbrb.by/API/ExRates/Rates?Periodicity=0'
CURRENCY_RATE = 'https://www.nbrbb.by/api/exrates/rates/'
CURRENCY_MARKET = 'https://banki24.by/exchange/currencymarket'

CURRENCY_CODES = {'AUD': 440, 'AMD': 510, 'BGN': 441, 'UAH': 449, 'DKK': 450, 'USD': 431, 'EUR': 451, 'PLN': 452,
                  'JPY': 508, 'IRR': 461, 'ISK': 453, 'CAD': 371, 'CNY': 462, 'KWD': 394, 'MDL': 454, 'NZD': 448,
                  'NOK': 455, 'RUB': 456, 'XDR': 457, 'SGD': 421, 'KGS': 458, 'KZT': 459, 'TRY': 460, 'GBP': 429,
                  'CZK': 463, 'SEK': 464, 'CHF': 426}


def get_data(url: str, headers: dict = None) -> requests.Response:
    if headers is None:
        headers = HEADERS
    return requests.get(url, headers=headers, timeout=(3, 25))


def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:  # TODO: refactor this shit!
            # logging.exception(e)
            return '# Connection error #',
        except requests.exceptions.Timeout as e:
            # logging.exception(e)
            return '# Timeout error #',
        except Exception as e:
            # logging.exception(e)
            return '# Exception occurred durin connection #',
        return func(*args, *kwargs)

    return wrapper


def get_currency(currency_id: int) -> dict:
    response = get_data(CURRENCY_RATE + str(currency_id))
    return response.json()


def get_all_currencies() -> list[dict]:
    return get_data(ALL_DAILY_RATES).json()


def format_currency_rates(currency: list[dict]) -> list:
    return [f'{item.get("Cur_Name")}: {item.get("Cur_OfficialRate")} BYN' for item in currency]


def format_byn_cost(currency: list[dict]) -> list:
    return [
        f'{(item.get("Cur_Scale") / item.get("Cur_OfficialRate")):.6f} {item.get("Cur_Name")}'
        for item in currency
    ]


@handle_exception
def get_rates(*currency_codes) -> list:
    """
    Returns official byn rates from nbrb.by API
    """
    currencies = [get_currency(CURRENCY_CODES.get(code)) for code in currency_codes]
    rates = format_currency_rates(currencies)
    return rates


@handle_exception
def get_byn_cost(*currency_codes) -> tuple:
    """
    Returns byn cost in usd, eur, rur from nbrb.by API
    """
    # data = get_data(ALL_DAILY_RATES).json(),
    currencies = [get_currency(CURRENCY_CODES.get(code)) for code in currency_codes]
    byn_cost = format_byn_cost(currencies)
    return byn_cost


@handle_exception
def get_exchange_rates():
    """
    Returns stock exchange rates with BeautifulSoup
    """
    page = get_data(CURRENCY_MARKET, HEADERS).text
    soup = BeautifulSoup(page, "html.parser")
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

    return exchange_rates


def random_answer():
    ans = ('Прошу прощения, создатель научил меня только искать курсы валют :(',
           'Извини, я тебя не понимаю, я только учусь!',
           'Хвала создателю!!',
           'Извини, попробуй спросить позже.',
           'Человек, я тебя не понимаю.')

    return random.choice(ans)
