# -*- coding: utf-8 -*-

import os

def check_balance():
    import json
    import requests

    if 'CARD_ID' in os.environ:
        CARD_ID = os.environ.get("CARD_ID")
    else:
        from config import CARD_ID

    url = 'https://mygift.gift-cards.ru/api/1/cards/' + CARD_ID

    params = {'limit': '100',
              'rid': '8905a422dd328'}

    headers = {'Host': 'mygift.gift-cards.ru',
               'Connection': 'keep-alive',
               'DNT': '1',
               'X-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/79.0.3945.88 Safari/537.36',
               'X-Request-Id': '8905a422dd328',
               'Content-Type': 'application/json;charset=utf-8',
               'Accept': '*/*',
               'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-Mode': 'cors',
               'Referer': 'https://mygift.gift-cards.ru/balance',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cookie': '_ga=GA1.3.2083281106.1577032995; _gid=GA1.3.998538586.1577032995; isAvaliable=true; upc={'
                         '"interfaceSettings":{}}; sessionId=c081dfd1-7e67-49c4-9af2-9272354518a6; _gat=1'}

    r = requests.get(url, params=params, headers=headers, timeout=10)
    response = json.loads(r.text)
    respstr = f"{response['data']['balance']['availableAmount']}"

    return respstr

if __name__ == '__main__':
    print(check_balance())