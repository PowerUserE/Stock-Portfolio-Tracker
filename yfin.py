# import yfinance as yf
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime
# # plt.style.use('seaborn')

# # Get the data for the stock AAPL
# # apple = yf.Ticker('AAPL')
# # print(apple.info)

# # stockinfo = apple.info

# # for key, value in stockinfo.items():
# #     print(key, ":", value)

# # print(apple.major_holders)
# # print(apple.institutional_holders)
# # print(apple.splits)
# # print(apple.dividends)


# def fetch_realtime_price(ticker):
#     stock = yf.Ticker(ticker)
#     data = stock.history(period='1d')
#     current_price = data['Close'].iloc[-1]
#     return current_price


# current_prices = []
# for ticker in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NFLX', 'BABA', 'NVDA', 'JPM', 'V', 'MA', 'WMT', 'MCD', 'KO', 'PEP', 'PG', 'JNJ', 'UNH', 'DIS', 'NKE', 'SBUX', 'COST', 'HD', 'BA']:
#     current_prices.append(fetch_realtime_price(ticker))
#     print(fetch_realtime_price(ticker))
