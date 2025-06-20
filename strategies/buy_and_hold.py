import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_buy_and_hold_strategy(data, startDate, endDate):
    """
    A simple, buy the stock and hold 
    it for however long the window is set to.
    """
    data['Position'] = 0 # Set the trading position to default

    buy_price = data.loc [startDate]['Close'].squeeze()

    sell_price = data.iloc[-1]['Close'].squeeze()

    data = (buy_price - sell_price) / buy_price * 100

    return data