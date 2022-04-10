import random
import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'}


# get official byn rates from nbrb.by API
def get_rates():
    try:
        r = requests.get('https://www.nbrb.by/API/ExRates/Rates?Periodicity=0', headers=headers, timeout=(3, 25)).json()

        for i in r:
            if i['Cur_ID'] == 431:
                usd_dict = dict(i)
            elif i['Cur_ID'] == 451:
                eur_dict = dict(i)
            elif i['Cur_ID'] == 455:
                nok_dict = dict(i)
            elif i['Cur_ID'] == 456:
                rur_dict = dict(i)

        usd = usd_dict["Cur_Name"] + ': ' + str(usd_dict['Cur_OfficialRate']) + ' BYN'
        eur = eur_dict["Cur_Name"] + ': ' + str(eur_dict['Cur_OfficialRate']) + ' BYN'
        rur = str(rur_dict["Cur_Scale"]) + ' ' + rur_dict["Cur_Name"] + ': ' + str(
            rur_dict['Cur_OfficialRate']) + ' BYN'
        nok = str(nok_dict["Cur_Scale"]) + ' ' + nok_dict["Cur_Name"] + ': ' + str(
            nok_dict['Cur_OfficialRate']) + ' BYN'

        rates = (usd, eur, rur, nok)

    except requests.exceptions.ConnectionError as err:
        rates = ('# Connection error #',)
        print(err)
    except requests.exceptions.HTTPError as err:
        rates = ('# HTTP error #',)
        print(err)
    except requests.exceptions.Timeout as err:
        rates = ('# Timeout error #',)
        print(err)

    return rates


# get byn cost in usd, eur, rur from nbrb.by API
def get_byn_cost():
    try:
        r = requests.get('https://www.nbrb.by/API/ExRates/Rates?Periodicity=0', headers=headers, timeout=(3, 25)).json()

        for i in r:
            if i['Cur_ID'] == 431:
                usd_dict = dict(i)
            elif i['Cur_ID'] == 451:
                eur_dict = dict(i)
            elif i['Cur_ID'] == 456:
                rur_dict = dict(i)

        usd = float("{:.6f}".format(1 / (usd_dict['Cur_OfficialRate'])))
        eur = float("{:.6f}".format(1 / (eur_dict['Cur_OfficialRate'])))
        rur = float("{:.6f}".format(100 / (rur_dict['Cur_OfficialRate'])))

        byn_cost = (str(usd) + ' USD', str(eur) + ' EUR', str(rur) + ' RUR')

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
        page = requests.get('https://banki24.by/exchange/currencymarket', headers=headers, timeout=(3, 25))
        soup = BeautifulSoup(page.text, "html.parser")
        # currency_value = soup.find_all('p', class_='text-center h1 mt-0')
        currency_value = soup.select('p.text-center.h1.mt-0')
        # currency_change = soup.find_all('span', class_='pull-left label label-danger')
        currency_change = soup.select('span.pull-left.label')

        currency = []
        change = []

        for i in range(len(currency_value)):
            currency.append(currency_value[i].text.replace('\n', '').replace('\t', ''))

        for i in range(len(currency_change)):
            change.append(currency_change[i].text.replace('\n', '').replace('\t', '').replace('&plus', '+'))

        usd = f'1 USD: {currency[0]} ({change[0]})'
        eur = f'1 EUR: {currency[1]} ({change[1]})'
        rur = f'100 RUR: {currency[2]} ({change[2]})'
        cny = f'10 CNY: {currency[3]} ({change[3]})'

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
