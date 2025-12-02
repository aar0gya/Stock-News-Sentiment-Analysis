# 📈 Stock News Sentiment Analysis

Analyze the **real-time sentiment of stock market news** using Python, FinViz scraping, and VADER sentiment analysis. This project provides both **tabular data** and **visual sentiment charts** for multiple tickers in a **live web app** built with **Streamlit**.

---

## 🔗 Live Demo

[Click here to access the live app](https://stock-news-sentiment-analysis-fzx7qmxy27r8jt7immruik.streamlit.app/)

---

## 🚀 Features

- Scrapes **real-time news headlines** from FinViz for multiple stock tickers.
- Performs **sentiment analysis** using the **VADER** lexicon.
- Computes **daily average sentiment** per ticker.
- Displays **interactive tables** and **bar charts** in a web browser.
- Built with **Python**, **Streamlit**, **Pandas**, and **Matplotlib**.
- Ready for **live deployment** on Streamlit Cloud.

---

## 🛠 Tech Stack

- **Python 3.11+**
- **Streamlit** — web interface
- **Pandas** — data processing
- **Matplotlib** — visualization
- **BeautifulSoup4 & Requests** — web scraping
- **NLTK & VADER** — sentiment analysis

---

## 💡 How to Use Locally

**Clone the repo**

```bash
git clone https://github.com/your-username/stock-news-sentiment-analysis.git
cd stock-news-sentiment-analysis

pip install -r requirements.txt

streamlit run app.py

Stock-News-Sentiment-Analysis/
│
├── app.py                 # Streamlit web app
├── main.py                # Original CLI script
├── vader_lexicon.txt      # VADER lexicon for sentiment analysis
├── requirements.txt       # Python dependencies
├── README.md              # Project overview
└── LICENSE                # Open source license

```

⚡ Notes

Streamlit Cloud automatically updates the app whenever you push to GitHub.

FinViz may occasionally block requests — in that case, wait a few minutes and try again.

The VADER lexicon is included to avoid runtime download issues in cloud deployment.

---

📈 Future Enhancements

Add historical trend analysis for multiple tickers.

Include sentiment heatmaps and ticker comparisons.

Implement user authentication for personalized watchlists.

Add export to CSV/Excel functionality.


