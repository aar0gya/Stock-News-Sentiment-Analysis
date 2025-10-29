# 📰 Stock News Sentiment Analysis

A Python-based project that performs **sentiment analysis on financial news headlines** for selected stock tickers.  
It scrapes news from [Finviz](https://finviz.com), analyzes sentiment using NLTK’s **VADER** model, and visualizes the resulting sentiment trends.

---

## 🚀 Features
- Fetches the latest stock-related news headlines for defined tickers.  
- Uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** to compute sentiment scores.  
- Aggregates sentiment per ticker and date.  
- Visualizes sentiment trends using Matplotlib.

---

## 🧩 Requirements
Install all dependencies before running:


🧠 How It Works

Web Scraping
Retrieves news headlines for each ticker (e.g., AMZN, GOOG, META) from Finviz.

Sentiment Analysis
Uses VADER to assign a compound sentiment score to each headline.

Visualization
Averages sentiment scores per day and plots them for easy comparison.

📈 Example Output

The program generates a bar graph illustrating the positive or negative sentiment of recent news for each ticker over time.

🛠️ Troubleshooting

If no graph appears, Finviz may be blocking automated requests.
Try changing your user-agent string or using a VPN.

If the dataset is empty, confirm that Finviz’s layout hasn’t changed.

🤝 Contributing

Just to let you know, pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to modify.

👤 Author:
Aarogya Bikram Thapa
