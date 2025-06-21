import numpy as np
import matplotlib.pyplot as plt

def run_macd_strategy_improved(data):
    """
    Run the MACD strategy on the provided data.
    """
    data = calculate_macd(data, short_window=12, long_window=26, signal_window=9)
    data = crossover_logic(data)
    plot_strategy(data)
    return data

# Calculate Moving average lines
def calculate_macd(data, short_window, long_window, signal_window):
    data['EMA_SHORT'] = data['Close'].ewm(span=short_window, adjust=False).mean() # The fast moving EMA
    data['EMA_LONG'] = data['Close'].ewm(span=long_window, adjust=False).mean() # The slow moving EMA
    data['MACD'] = data['EMA_SHORT'] - data['EMA_LONG'] # The MACD Line
    # The Signal Line is the EMA of the MACD line - this is used to generate buy/sell signals
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data

"""
What makes this strategy improved is our handling of the signal detection surrounding the centerline (0).
We can include the parameters of the original MACD strategy but with this added component.
When there is high momentum, those above the centerline are more likely to be short term gains.
The strategy will buy when the MACD crosses above the signal line and is below the centerline,
and sell when the MACD crosses below the signal line and is above the centerline.
"""

# Crossover Detection Logic
def crossover_logic(data):
    # Set default position to 0
    data['Position'] = 0

    # Buy: When MACD cross above Signal AND MACD is below 0 (Early momentum)
    buy_signal = (data['MACD'] > data['Signal']) & (data['MACD'].shift(1) < data['Signal'].shift(1)) & (data['MACD'] < 0)
    data.loc[buy_signal, 'Position'] = 1  # Buy signal

    # Sell: When MACD crosses below the Signal
    sell_signal = ((data['MACD'] < data['Signal']) & (data['MACD'].shift(1) > data['Signal'].shift(1)))
    data.loc[sell_signal, 'Position'] = -1  # Sell signal

    # Fill position forward to simulate holding
    data['Position'] = data['Position'].ffill().fillna(0)

    # Detect actual position changes
    data['Position_Change'] = data['Position'].diff()

    return data

def plot_strategy(data):
    """
    Plot the results of the MACD strategy.
    Use two windows, one to show the stock price, the other shows the strategy.
    Both windows display the buy and sell signals to help visualize the strategy.
    """
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # Plot Stock Price
    ax1.set_title('Stock Price')
    ax1.set_ylabel('Price')
    ax1.plot(data['Close'], label='Close Price')
    ax1.legend()

    # Plot MACD and Signal Line
    ax2.plot(data['MACD'], label='MACD', color='blue')
    ax2.plot(data['Signal'], label='Signal Line', color='orange')
    ax2.set_title('MACD Strategy')
    ax2.set_ylabel('MACD Value')
    ax2.legend()
    
    # Plot buy signals
    buy_signals = data[data['Position_Change'] == 1]
    for idx in buy_signals.index:
        ax1.axvline(x=idx, color='green', label='', alpha=0.4)
        ax2.axvline(x=idx, color='green', label='', alpha=0.4)

    # Plot sell signals
    sell_signals = data[data['Position_Change'] == -1]
    for idx in sell_signals.index:
        ax1.axvline(x=idx, color='red', label='', alpha=0.4)
        ax2.axvline(x=idx, color='red', label='', alpha=0.4)

    plt.show()