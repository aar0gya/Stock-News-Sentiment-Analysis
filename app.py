import nltk
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
import time

# ------------------------------------------------
# SCRAPER + SENTIMENT LOGIC (same as your main.py)
# ------------------------------------------------

FINVIZ_URL = "https://finviz.com/quote.ashx?t="
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) "
        "Gecko/20100101 Firefox/120.0"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def parse_date(date_str):
    if date_str is None:
        return None

    formats = ["%b-%d-%y", "%b %d", "%m/%d/%y"]

    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            pass

    return pd.to_datetime(date_str, errors="coerce")


def fetch_news(ticker):
    url = FINVIZ_URL + ticker.upper()
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", id="news-table")
        return table
    except:
        return None


def run_sentiment_analysis(ticker_list):
    all_rows = []

    for ticker in ticker_list:
        table = fetch_news(ticker)
        time.sleep(1)

        if not table:
            continue

        for row in table.find_all("tr"):
            link = row.find("a")
            if not link:
                continue

            title = link.text.strip()
            timestamp = row.td.text.strip().split()

            if len(timestamp) == 2:
                date, time_ = timestamp
            else:
                date, time_ = None, timestamp[0]

            all_rows.append([ticker, date, time_, title])

    df = pd.DataFrame(all_rows, columns=["ticker", "date", "time", "title"])

    if df.empty:
        return None, None

    df["date"] = df["date"].apply(parse_date)
    df = df.dropna(subset=["date"])
    df["date"] = df["date"].dt.date

    vader = SentimentIntensityAnalyzer()
    df["compound"] = df["title"].apply(lambda x: vader.polarity_scores(x)["compound"])

    mean_df = (
        df.groupby(["ticker", "date"], as_index=False)["compound"]
        .mean()
        .pivot(index="date", columns="ticker", values="compound")
    )

    return df, mean_df


# ------------------------------------------------
# STREAMLIT UI
# ------------------------------------------------

st.set_page_config(page_title="Stock News Sentiment Analysis", layout="wide")

st.title("📈 Stock Market News Sentiment Analysis")
st.write("Analyze real-time sentiment for major tickers using FinViz news scraping & VADER sentiment analysis.")

tickers_input = st.text_input(
    "Enter Stock Tickers (comma-separated)",
    "NVDA, META, GOOG"
)

if st.button("Run Analysis"):
    tickers = [t.strip().upper() for t in tickers_input.split(",")]

    st.info("Fetching latest news & computing sentiment... Please wait.")

    df, mean_df = run_sentiment_analysis(tickers)

    if df is None:
        st.error("No data found — FinViz may have blocked requests.")
    else:
        st.subheader("📄 Scraped News Table")
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Daily Average Sentiment Chart")

        fig, ax = plt.subplots(figsize=(12, 5))
        mean_df.plot(kind="bar", ax=ax)
        ax.set_title("Daily Average Sentiment per Ticker")
        ax.set_ylabel("Compound Sentiment")
        ax.set_xlabel("Date")
        st.pyplot(fig)

        st.success("Analysis Completed Successfully!")

