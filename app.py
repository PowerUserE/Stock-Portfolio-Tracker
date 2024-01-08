

import streamlit as st1
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import time
import yfinance as yf
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

total_investment = 0
st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.header("Stock Portfolio Tracker")


def fetch_realtime_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')
    current_price = data['Close'].iloc[-1]
    return current_price


@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    return df


df = pd.DataFrame()
df = pd.read_csv('portfolio_sample.csv')


ticker = st.sidebar.multiselect(
    "SELECT TICKER", options=df["Ticker"].unique(), default=df["Ticker"].unique())

df_selection = df.query("Ticker==@ticker")
# show df_selection
# st.dataframe(df["Ticker"].unique())
total_investment = df_selection['Purchase Price'].sum()


with st.sidebar:
    st.header("Configuration")
    upload_option = st.radio("Choose data source:",
                             ("Use Sample Portfolio", "Upload File"))
    if upload_option == "Use Sample Portfolio":
        st.info("Using Sample Portfolio.")
        df = pd.read_csv('portfolio_sample.csv')
    elif upload_option == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload CSV", type=["csv"], accept_multiple_files=False)
        if uploaded_file is not None:
            st.info("Using uploaded Portfolio.")
            df = load_data(uploaded_file)
        else:
            st.info("Using Sample Portfolio.")
            df = load_data("portfolio_sample.csv")


def Home():
    current_prices = []
    for ticker in df["Ticker"].unique():
        current_prices.append(fetch_realtime_price(ticker))

    # total_investment = df_selection['Purchase Price'].sum()
    networth_increase = sum(current_prices) - \
        df_selection['Purchase Price'].sum()

    gains_losses = sum(current_prices) - df_selection['Purchase Price'].sum()
    percentage_returns = (gains_losses / total_investment) * \
        100 if total_investment != 0 else 0

    # Add current prices to df_selection
    df_selection['Current Price'] = current_prices

    st.info('Portfolio Summary')
    total1, total2, total4 = st.columns(3, gap='small')
    with total1:
        st.info('Total Investment', icon="💰")
        st.metric(label="Total Investment",
                  value=f"{total_investment:,.2f}", help="Total investment made", delta=f'in $')
    with total2:
        st.info('Net Worth', icon="💰")
        st.metric(label="Net Worth",
                  value=f"${sum(current_prices):,.2f}", delta=f'{percentage_returns:,.2f}%', help="Total net worth of portfolio")
    with total4:
        st.info('Gains/Losses', icon="💰")
        st.metric(label="Profit/Loss",
                  value=f"${gains_losses:,.2f}", delta=f'{percentage_returns:,.2f}%', help="Total profit/loss since purchase")

    style_metric_cards(
        # set the background color to black
        background_color="#000000",
        border_left_color="#686664",
        border_color="#000000",
        box_shadow="#F71938"
    )


def realtime():
    ##############################
    # Real-time Updates for 10
    with st.expander("Click here to see Real-Time Updates"):
        st1.info('Real-Time Updates')
        columns = st1.columns(4, gap='small')

        for index, row in df_selection.iterrows():
            stock_ticker = row['Ticker']
            current_price = fetch_realtime_price(stock_ticker)
            price_change = (current_price - row['Purchase Price'])
            percent_change = (price_change / row['Purchase Price']) * 100

            with columns[index % 4]:  # Use modulo to distribute items across columns
                st1.metric(label=stock_ticker,
                           value=f"${current_price:,.2f}", delta=f"{percent_change:,.2f}%")
    ##############################


def showData():
    with st.expander("VIEW PORTFOLIO DATA"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=[
                                  "Ticker", "Quantity", "Purchase Date", "Purchase Price"])
        st.dataframe(df_selection[showData], use_container_width=True)


def create_empty_dataframe():
    columns = ['Symbol / Ticker', 'Last Price', 'Change + Change %', 'Shares', 'Market Value', 'Unrealized Gain/Loss',
               'Investment Cost', 'Weight % in Portfolio', 'Trailing P/E', 'EPS (TTM)', 'Book Value', '52-week Range']
    return pd.DataFrame(columns=columns)


def get_stock_details(ticker, shares, purchase_price):
    # Create a Ticker object for the specified stock symbol
    stock = yf.Ticker(ticker)

    # Fetch data using various attributes
    info = stock.info
    for key, value in info.items():
        print(key, ":", value)

    # history = stock.history(period="1d")
    # stats = stock.info['quoteType']
    # div_info = stock.dividends
    # splits = stock.splits

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
    weight_percent = market_value / total_investment * 100
    # try catch for pe_ratio
    try:
        pe_ratio = info['trailingPE']
    except KeyError:
        pe_ratio = info['forwardPE']
    eps_ttm = info['trailingEps']
    book_value = info['bookValue']
    wk_range = info['fiftyTwoWeekLow'] - info['fiftyTwoWeekHigh']

    return [symbol, last_price, change_info, shares, market_value, unrealized_gain_loss, investment_cost, weight_percent, pe_ratio, eps_ttm, book_value, wk_range]
    # return details_df


def realtime_table():
    details_df = create_empty_dataframe()
    for data in df.iterrows():
        ticker = data[1]['Ticker']
        shares = data[1]['Quantity']
        purchase_price = data[1]['Purchase Price']
        details = get_stock_details(
            ticker, shares, purchase_price)
        details_df.loc[len(details_df)] = details

        # details = get_stock_details(
        #     ticker, total_investment, shares, purchase_price)

    st.write("Portfolio Tracker")

    gd = GridOptionsBuilder.from_dataframe(details_df)
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum',
                                editable=True, resizable=True, sortable=True, filter=True)
    sel_model = st.radio("Select Model", ["Multi", "Single"])
    gd.configure_selection(selection_mode=sel_model, use_checkbox=True)
    gridOptions = gd.build()

    grid_table = AgGrid(details_df, gridOptions=gridOptions,
                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                        width='100%', theme='balham', fit_columns_on_grid_load=True,
                        allow_unsafe_jscode=True, enable_enterprise_modules=True)
    sel_rows = grid_table['selected_rows']
    st.write(sel_rows)

# Function for portfolio graphs


def graphs():
    # Bar graph: Investment by Ticker
    investment_by_ticker = df_selection.groupby(by=["Ticker"]).sum()[
        "Purchase Price"].sort_values()
    fig_investment = px.bar(
        investment_by_ticker,
        x=investment_by_ticker.index,
        y="Purchase Price",
        orientation="v",
        title="<b> INVESTMENT BY TICKER </b>",
        color_discrete_sequence=["#0083B8"] * len(investment_by_ticker),
        template="plotly_white",
    )
    fig_investment.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", font=dict(color="black"))

    # Pie chart: Quantity by Ticker
    fig_pie = px.pie(df_selection, values='Quantity',
                     names='Ticker', title='QUANTITY BY TICKER')
    fig_pie.update_layout(legend_title="Ticker", legend_y=0.9)
    fig_pie.update_traces(textinfo='percent+label', textposition='inside')

    left, right = st.columns(2)
    left.plotly_chart(fig_investment, use_container_width=True)
    right.plotly_chart(fig_pie, use_container_width=True)


# Function to show progress bar against s&p 500

def Progressbar():
    # Assuming the S&P 500 value is 200000 trillion (just an example, replace with the actual value)
    sp500_value = 20000

    st.markdown(
        """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""", unsafe_allow_html=True)

    current_portfolio_value = df_selection["Purchase Price"].sum()
    percent_portfolio_vs_sp500 = round(
        (current_portfolio_value / sp500_value * 100))

    mybar = st.progress(0)

    if percent_portfolio_vs_sp500 > 100:
        st.subheader("Your Portfolio Outperformed the S&P 500!")
    else:
        st.write("Your portfolio is ",
                 percent_portfolio_vs_sp500, "% of the S&P 500")
        for percent_complete in range(percent_portfolio_vs_sp500):
            time.sleep(0.1)
            mybar.progress(percent_complete + 1,
                           text="Portfolio vs. S&P 500 Percentage")


# Menu bar

def sideBar():
    with st.sidebar:
        selected = st.radio("Main Menu", ["Home Page", "Add Investment"])
    return selected


# Main content
selected_menu = sideBar()

if selected_menu == "Home Page":
    showData()
    Home()
    realtime()
    Progressbar()
    graphs()

    realtime_table()

if selected_menu == "Add Investment":
    st.subheader("Add Investment")
    st.write("Add your investment details here")

# Theme
hide_st_style = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
# Apply dark theme using custom CSS styles
dark_theme_styles = """
<style>
body {
    color: white;
    background-color: #1E1E1E;  /* Dark background color */
}

/* Sidebar styling */
.sidebar .sidebar-content {
    background-color: #333333;  /* Dark sidebar background color */
}

/* Metrics cards styling */
.stMetricText {
    color: white;
}

.stMetricDelta {
    color: white;
}

/* Progress bar styling */
.stProgressBar div div div div {
    background-image: linear-gradient(to right, #99ff99, #FFFF00);
}

</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(dark_theme_styles, unsafe_allow_html=True)
