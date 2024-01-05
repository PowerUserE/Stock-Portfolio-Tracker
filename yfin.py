import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
# plt.style.use('seaborn')

# Get the data for the stock AAPL
apple = yf.Ticker('AAPL')
# print(apple.info)

stockinfo = apple.info

# for key, value in stockinfo.items():
#     print(key, ":", value)

print(apple.major_holders)
print(apple.institutional_holders)
print(apple.splits)
print(apple.dividends)
