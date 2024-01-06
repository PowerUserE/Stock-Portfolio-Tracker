# Web srapping script to get real time stock price from yahoo finance

import pandas as pd
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import datetime


def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    # if web_content is None:
    #     return []
    try:
        spans = web_content_div[0].find_all('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    return texts


def real_time_price(stock_code):
    url = 'https://finance.yahoo.com/quote/' + \
        stock_code + '?p=' + stock_code + '&.tsrc=fin-srch'
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')

        # price, change
        texts = web_content_div(
            web_content, 'My(6px) Pos(r) smartphone_Mt(6px) W(100%)')
        if texts != []:
            price = texts[0]
            change = texts[1]
        else:
            price, change = [], []

        # volume
        # texts = web_content_div(web_content, 'Pos(r) Pos(s)!--lgv2')
        texts = web_content_div(
            web_content, 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)')
        if texts != []:
            for count, vol in enumerate(texts):
                if vol == 'Volume':
                    volume = texts[count+1]
        else:
            volume = []

        # latest pattern
        pattern = web_content_div(
            web_content, 'Bxz(bb) D(ib) Va(t) Mih(250px)--lgv2 W(100%) Mt(-6px) Mt(0px)--mobp Mt(0px)--mobl W(50%)--lgv2 Mend(20px)--lgv2 Pend(10px)--lgv2')
        try:
            latest_pattern = pattern[0]
        except IndexError:
            latest_pattern = []

        # 1 year target
        texts = web_content_div(
            web_content, 'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)')
        if texts != []:
            for count, target in enumerate(texts):
                if target == '1y Target Est':
                    one_year_target = texts[count]
        else:
            one_year_target = []

    except ConnectionError:
        price, change, volume, latest_pattern, one_year_target = [], [], [], [], []
    return price, change, volume, latest_pattern, one_year_target


Stock = ['AAPL', 'TSLA', 'META', 'GOOG', 'MSFT', 'AMZN']
# print(real_time_price('AAPL'))
for stock in Stock:
    price, change, volume, latest_pattern, one_year_target = real_time_price(
        stock)
    # pretty print
    print(stock)
    print('Price: ', price)
    print('Change: ', change)
    print('Volume: ', volume)
    print('Latest Pattern: ', latest_pattern)
    print('1 Year Target: ', one_year_target)
    print('-----------------------------')

# # Function to show progress bar against s&p 500
