from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

finviz_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'GOOG', 'META']

news_tables = {}
for ticker in tickers:
    url = finviz_url + ticker
    req = Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )

    try:
        response = urlopen(req)
        html = BeautifulSoup(response, 'html.parser')
        news_table = html.find('table', id='news-table')
        if news_table:
            news_tables[ticker] = news_table
        else:
            print(f"No news found for {ticker}")
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")

parsed_data = []

for ticker, news_table in news_tables.items():
    for row in news_table.find_all('tr'):
        link = row.find('a')
        if not link:
            continue
        title = link.text.strip()
        date_text = row.td.text.strip().split(' ')
        if len(date_text) == 1:
            time = date_text[0]
            date = None
        else:
            date, time = date_text[0], date_text[1]
        parsed_data.append([ticker, date, time, title])

df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

if df.empty:
    print("No data scraped. Finviz may have blocked requests or changed HTML layout.")
else:
    vader = SentimentIntensityAnalyzer()
    df['compound'] = df['title'].apply(lambda t: vader.polarity_scores(t)['compound'])
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    df = df.dropna(subset=['date'])

    mean_df = (
        df.groupby(['ticker', 'date'], as_index=False)['compound']
        .mean()
        .pivot(index='date', columns='ticker', values='compound')
    )

    if mean_df.empty:
        print("No sentiment data to plot.")
    else:
        plt.figure(figsize=(10, 8))
        mean_df.plot(kind='bar')
        plt.title("Average Sentiment per Ticker Over Time")
        plt.ylabel("Compound Sentiment")
        plt.xlabel("Date")
        plt.tight_layout()
        plt.show(block=True)
        input("Press Enter to close the plot window...")
