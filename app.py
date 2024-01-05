

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from streamlit_extras.metric_cards import style_metric_cards
import time

st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.header("Stock Portfolio Tracker")


@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    return df


df = pd.DataFrame()
df = pd.read_csv('portfolio_sample.csv')


ticker = st.sidebar.multiselect(
    "SELECT TICKER", options=df["Ticker"].unique(), default=df["Ticker"].unique())

df_selection = df.query("Ticker==@ticker")

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


with st.expander("Uploaded Data Preview"):
    st.dataframe(df.head(10))


def Home():

    total_investment = df_selection['Purchase Price'].sum()
    investment_mode = df_selection['Purchase Price'].mode().iloc[0]
    investment_mean = df_selection['Purchase Price'].mean()
    investment_median = df_selection['Purchase Price'].median()

    st.info('Portfolio Summary')
    total1, total2, total3, total4, total5 = st.columns(5, gap='small')
    with total1:
        st.info('Total Investment', icon="💰")
        st.metric(label="Total Investment", value=f"{total_investment:,.2f}")
    with total2:
        st.info('Most Investment', icon="💰")
        st.metric(label="Most Investment", value=f"{investment_mode:,.2f}")
    with total3:
        st.info('Average Investment', icon="💰")
        st.metric(label="Average Investment", value=f"{investment_mean:,.2f}")
    with total4:
        st.info('Median Investment', icon="💰")
        st.metric(label="Median Investment", value=f"{investment_median:,.2f}")
    with total5:
        st.info('Total Quantity', icon="💰")
        # st.metric(label="Total Quantity", value=numerize(
        #     df_selection['Quantity'].sum()))
        st.metric(label="Total Quantity", value=df_selection['Quantity'].sum())

    style_metric_cards(
        # set the background color to black
        background_color="#000000",
        border_left_color="#686664",
        border_color="#000000",
        box_shadow="#F71938"
    )


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
    sp500_value = 200000

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
    Home()
    Progressbar()
    graphs()
    showData()

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
