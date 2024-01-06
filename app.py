

import streamlit as st1
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from streamlit_extras.metric_cards import style_metric_cards
import time
import yfinance as yf

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

    total_investment = df_selection['Purchase Price'].sum()
    investment_mode = df_selection['Purchase Price'].mode().iloc[0]
    investment_mean = df_selection['Purchase Price'].mean()
    gains_losses = sum(current_prices) - df_selection['Purchase Price'].sum()
    percentage_returns = (gains_losses / total_investment) * \
        100 if total_investment != 0 else 0

    # Add current prices to df_selection
    df_selection['Current Price'] = current_prices

    st.info('Portfolio Summary')
    total1, total2, total3, total4, total5 = st.columns(5, gap='small')
    with total1:
        st.info('Total Investment', icon="💰")
        st.metric(label="Total Investment",
                  value=f"${total_investment:,.2f}", delta=f'${total_investment:,.2f}')
    with total2:
        st.info('Most Investment', icon="💰")
        st.metric(label="Most Investment",
                  value=f"${investment_mode:,.2f}", delta=f'${investment_mode:,.2f}')
    with total3:
        st.info('Average Investment', icon="💰")
        st.metric(label="Average Investment",
                  value=f"${investment_mean:,.2f}", delta=f'${investment_mean:,.2f}')
    with total4:
        st.info('Gains/Losses', icon="💰")
        st.metric(label="Gains/Losses",
                  value=f"${gains_losses:,.2f}", delta=f'${gains_losses:,.2f}')
    with total5:
        st.info('Percentage Returns', icon="💰")
        st.metric(label="Percentage Returns",
                  value=f"{percentage_returns:,.2f}%", delta=f'{percentage_returns:,.2f}%')

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
        columns = st1.columns(5, gap='small')

        for index, row in df_selection.iterrows():
            stock_ticker = row['Ticker']
            current_price = fetch_realtime_price(stock_ticker)
            price_change = (current_price - row['Purchase Price'])
            percent_change = (price_change / row['Purchase Price']) * 100

            with columns[index % 5]:  # Use modulo to distribute items across columns
                st1.metric(label=stock_ticker,
                           value=f"${current_price:,.2f}", delta=f"{percent_change:,.2f}%")
    ##############################


def showData():
    with st.expander("VIEW PORTFOLIO DATA"):
        showData = st.multiselect('Filter: ', df_selection.columns, default=[
                                  "Ticker", "Quantity", "Purchase Date", "Purchase Price"])
        st.dataframe(df_selection[showData], use_container_width=True)


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
    Progressbar()
    graphs()
    realtime()

    # Update the app every 30 seconds
    # for _ in range(300):
    #     realtime()
    #     time.sleep(1)
    #     st.experimental_rerun()


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

st.markdown(hide_st_style, unsafe_allow_html=True)
