
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


import yfinance as yf
import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime
# # plt.style.use('seaborn')


def get_stock_details(ticker, Total_Portfolio_Value=10000, shares=15, purchase_price=83.33):
    # Create a Ticker object for the specified stock symbol
    stock = yf.Ticker(ticker)

    # Fetch data using various attributes
    info = stock.info
    for key, value in info.items():
        print(key, ":", value)

    history = stock.history(period="1d")
    stats = stock.info['quoteType']
    div_info = stock.dividends
    splits = stock.splits

    # Extract relevant details
    '''
    Symbol / Ticker
    Last Price
    Change + Change %
    Shares
    Market Value
    Unrealized Gain/Loss
    Investment Cost
    Weight % in Portfolio
    Trailing P/E
    EPS (TTM)
    Book Value
    52-week Range
    '''
    symbol = info['symbol']
    last_price = info['currentPrice']
    change_and_change_percent = (info['currentPrice'] - info['previousClose'])
    change_percent = info['currentPrice'] / info['previousClose']

    # Join the two variables into a single string
    change_info = "{} ({}%)".format(
        round(change_and_change_percent, 2), round(change_percent, 2))

    market_value = info['currentPrice'] * shares
    investment_cost = shares * purchase_price
    unrealized_gain_loss = info['currentPrice'] - investment_cost * shares
    weight_percent = market_value / Total_Portfolio_Value * 100
    pe_ratio = info['trailingPE']
    eps_ttm = info['trailingEps']
    book_value = info['bookValue']
    wk_range = info['fiftyTwoWeekLow'] - info['fiftyTwoWeekHigh']

    # facny print
    # print("Symbol: ", symbol)
    # print("Last Price: ", last_price)
    # print("Change info ", change_info)
    # print("Shares: ", shares)
    # print("Market Value: ", market_value)
    # print("Unrealized Gain/Loss: ", unrealized_gain_loss)
    # print("Investment Cost: ", investment_cost)
    # print("Weight % in Portfolio: ", weight_percent)
    # print("Trailing P/E: ", pe_ratio)
    # print("EPS (TTM): ", eps_ttm)
    # print("Book Value: ", book_value)
    # print("52-week Range: ", wk_range)

    # Create a DataFrame with the extracted details
    details_df = pd.DataFrame({
        'Symbol': [symbol],
        'Last Price': [last_price],
        'Change': [change_info],
        'Shares': [shares],
        'Market Value': [market_value],
        'Unrealized Gain/Loss': [unrealized_gain_loss],
        'Investment Cost': [investment_cost],
        'Weight % in Portfolio': [weight_percent],
        'Trailing P/E': [pe_ratio],
        'EPS (TTM)': [eps_ttm],
        'Book Value': [book_value],
        '52-week Range': [wk_range]
    })

    for data in details_df.iterrows():
        print(data[1])

    return details_df


# Example usage
ticker_symbol = "META"  # Replace with your desired stock symbol
details_df = get_stock_details(ticker_symbol)
# print(details_df)
