import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# ----------------------------------------
# CONFIG
# ----------------------------------------
FINVIZ_URL = "https://finviz.com/quote.ashx?t="
TICKERS = ["AMZN", "META", "GOOG"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) "
        "Gecko/20100101 Firefox/120.0"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# ----------------------------------------
# SCRAPE NEWS TABLES
# ----------------------------------------
def fetch_news_table(ticker):
    url = FINVIZ_URL + ticker
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", id="news-table")
        return table
    except Exception as e:
        print(f"[ERROR] Could not fetch {ticker}: {e}")
        return None


news_tables = {}
for t in TICKERS:
    print(f"Fetching news for {t} ...")
    news_table = fetch_news_table(t)
    if news_table:
        news_tables[t] = news_table
    else:
        print(f"[WARNING] No news found for {t}")
    time.sleep(1.2)  # Prevent IP ban

# ----------------------------------------
# PARSE NEWS
# ----------------------------------------
parsed_rows = []

for ticker, table in news_tables.items():
    for row in table.find_all("tr"):
        link = row.find("a")
        if not link:
            continue

        title = link.text.strip()
        timestamp = row.td.text.strip().split()

        # Handle different date formats FinViz uses
        if len(timestamp) == 2:
            date, time_ = timestamp
        else:
            date, time_ = None, timestamp[0]

        parsed_rows.append([ticker, date, time_, title])

df = pd.DataFrame(parsed_rows, columns=["ticker", "date", "time", "title"])

if df.empty:
    print("\n[ERROR] No news data collected. FinViz likely blocked the scraping.")
    exit()

# ----------------------------------------
# DATE PARSING (NO MORE WARNINGS 🚀)
# ----------------------------------------
def parse_date(date_str):
    if date_str is None:
        return None

    formats = ["%b-%d-%y", "%b %d", "%m/%d/%y"]

    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            pass

    # Final fallback (slow but safe)
    try:
        return pd.to_datetime(date_str, errors="coerce")
    except:
        return None


df["date"] = df["date"].apply(parse_date)
df = df.dropna(subset=["date"])
df["date"] = df["date"].dt.date  # drop time component

# ----------------------------------------
# SENTIMENT ANALYSIS
# ----------------------------------------
vader = SentimentIntensityAnalyzer()
df["compound"] = df["title"].apply(lambda x: vader.polarity_scores(x)["compound"])

# ----------------------------------------
# GROUP & AVERAGE SENTIMENT
# ----------------------------------------
mean_df = (
    df.groupby(["ticker", "date"], as_index=False)["compound"]
    .mean()
    .pivot(index="date", columns="ticker", values="compound")
)

# ----------------------------------------
# DISPLAY RESULTS
# ----------------------------------------
print("\n==================== RAW NEWS TABLE ====================\n")
print(df)

print("\n==================== DAILY AVERAGE SENTIMENT ====================\n")
print(mean_df)

# ----------------------------------------
# PLOT
# ----------------------------------------
if not mean_df.empty:
    plt.figure(figsize=(12, 6))
    mean_df.plot(kind="bar")
    plt.title("Daily Average Sentiment per Ticker")
    plt.xlabel("Date")
    plt.ylabel("Compound Sentiment")
    plt.tight_layout()
    plt.show()
else:
    print("[INFO] No sentiment data to plot.")
