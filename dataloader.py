import yfinance as yf
import pandas as pd

def get_price_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data = pd.DataFrame(data)
    return data