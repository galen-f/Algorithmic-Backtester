# from ../dataloader import get_price_data
import numpy as np
import matplotlib.pyplot as plt

def run_macd_strategy(data):
    """
    Run the MACD strategy on the provided data.
    """
    data = calculate_macd(data, short_window=12, long_window=26, signal_window=9)
    data = crossover_logic(data)
    data = assign_positions(data)
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

# Assign Positions based on MACD crossover
def assign_positions(data):
    """
    Assign positions based on the MACD crossover signals.
    """
    data['Position'] = 0
    data.loc[data['MACD'] > data['Signal'], 'Position'] = 1  # Buy signal
    data.loc[data['MACD'] < data['Signal'], 'Position'] = -1  # Sell signal
    data['Position'] = data['Position'].ffill().fillna(0)  # Forward fill positions
    return data

# Crossover Detection Logic
def crossover_logic(data):
    data['Position'] = np.where(data['MACD'] > data['Signal'], 1, 0)  # 1 for buy, 0 for sell
    data['Position_Change'] = data['Position'].diff()  # Detect changes in position
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