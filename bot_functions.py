import random
import requests
from bs4 import BeautifulSoup


# get official byn rates from nbrb.by API
def get_rates(is_web_or_bot):
    try:
        r = requests.get('https://www.nbrb.by/API/ExRates/Rates?Periodicity=0').json()

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
        rur = str(rur_dict["Cur_Scale"]) + ' ' + rur_dict["Cur_Name"] + ': ' + str(rur_dict['Cur_OfficialRate']) + ' BYN'
        nok = str(nok_dict["Cur_Scale"]) + ' ' + nok_dict["Cur_Name"] + ': ' + str(nok_dict['Cur_OfficialRate']) + ' BYN'

        if is_web_or_bot == 'bot':
            rates = usd + '\n' + eur + '\n' + rur + '\n' + nok
        else:
            rates = (usd, eur, rur, nok)

    except requests.exceptions.ConnectionError as err:
        rates = '# Connection error #'
        print(err)
    except requests.exceptions.HTTPError as err:
        rates = '# HTTP error #'
        print(err)
    except requests.exceptions.Timeout as err:
        rates = '# Timeout error #'
        print(err)

    return rates


# get byn cost in usd, eur, rur from nbrb.by API
def get_byn_cost(is_web_or_bot):
    try:
        r = requests.get('https://www.nbrb.by/API/ExRates/Rates?Periodicity=0').json()

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

        if is_web_or_bot == 'bot':
            byn_cost = '1 BYN стоит:\n' + str(usd) + ' USD\n' + str(eur) + ' EUR\n' + str(rur) + ' RUR'
        else:
            byn_cost = (str(usd), str(eur), str(rur))

    except requests.exceptions.ConnectionError as err:
        byn_cost = '# Connection error #'
        print(err)
    except requests.exceptions.HTTPError as err:
        byn_cost = '# HTTP error #'
        print(err)
    except requests.exceptions.Timeout as err:
        byn_cost = '# Timeout error #'
        print(err)

    return byn_cost


# get stock exchange rates with BeautifulSoup
def get_exchange_rates(is_web_or_bot):
    try:
        page = requests.get('https://bankibel.by/torgi-na-bvfb')
        soup = BeautifulSoup(page.text, "html.parser")
        currency_value = soup.find_all('div', class_='curr_val')
        curr_value_change = soup.find_all('div', class_='change')

        currency = []
        change = []

        for i in range(len(currency_value)):
            currency.append(currency_value[i].text)

        for i in range(len(curr_value_change)):
            change.append(curr_value_change[i].text)

        usd = '1 USD: ' + str(currency[0]).lstrip() + ' (' + str(change[0]) + ')'
        eur = '1 EUR: ' + str(currency[1]).lstrip() + ' (' + str(change[2]) + ')'
        rur = '100 RUR: ' + str(currency[2]).lstrip() + ' (' + str(change[4]) + ')'

        if is_web_or_bot == 'bot':
            exchange_rates = 'Результаты торгов:\n' + usd + '\n' + eur + '\n' + rur
        else:
            exchange_rates = (usd, eur, rur)

    except requests.exceptions.ConnectionError as err:
        exchange_rates = '# Connection error #'
        print(err)
    except requests.exceptions.HTTPError as err:
        exchange_rates = '# HTTP error #'
        print(err)
    except requests.exceptions.Timeout as err:
        exchange_rates = '# Timeout error #'
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
