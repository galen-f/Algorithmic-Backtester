import matplotlib.pyplot as plt

"""
This is an aggressive macd strategy which is powerful in bull markets, but fails miserably in bear markets.
"""

def run_macd_agro(data):
    """
    Run the MACD strategy on the provided data.
    """
    data = calculate_macd(data, short_window=12, long_window=26, signal_window=9, trend_window=50)
    data = crossover_logic(data)
    plot_strategy(data)
    return data

# Calculate Moving average lines
def calculate_macd(data, short_window, long_window, signal_window, trend_window):
    data['EMA_SHORT'] = data['Close'].ewm(span=short_window, adjust=False).mean() # The fast moving EMA
    data['EMA_LONG'] = data['Close'].ewm(span=long_window, adjust=False).mean() # The slow moving EMA
    data['MACD'] = data['EMA_SHORT'] - data['EMA_LONG'] # The MACD Line
    # The Signal Line is the EMA of the MACD line - this is used to generate buy/sell signals
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()

    # Add a 200 day moving average to determine the trend of the stock.
    data['200_MA'] = data['Close'].ewm(span=trend_window, adjust=False).mean()

    # We are going to calculate the histogram value now too, we will use this to determine the strength of the signal. and when to buy and sell
    data['Histogram'] = data['MACD'] - data['Signal']
    return data

"""
What makes this strategy improved is our handling of the signal detection surrounding the centerline (0).
We can include the parameters of the original MACD strategy but with this added component.
When there is high momentum, those above the centerline are more likely to be short term gains.
The strategy will buy when the MACD crosses above the signal line and is below the centerline,
and sell when the MACD crosses below the signal line.
"""

# Crossover Detection Logic
def crossover_logic(data):
    position = 'neutral' # No position by default
    data['Position_Change'] = 0  # Initialize Position_Change column

    previous_buy_price = 0  # Track the price at which we bought

    for i in range(1, len(data)-1):
        macd_below_zero = data['MACD'].iloc[i] < 0                                                          # If the MACD is below the centerline (Undervalued)
        price_above_200ma = data['Close'].iloc[i] > data["200_MA"].iloc[i]                                  # If in an up-trend
        not_already_bought = position != 'buy'                                                              # If we are not already in a trade
                                                                     
        histogram_is_negative = data['Histogram'].iloc[i] < 0
        histogram_downwards_momentum_is_significant = data['Histogram'].iloc[i] < -1  # If the histogram is below a certain threshold
        we_are_in_a_trade = position == 'buy'
        price_below_200ma = data['Close'].iloc[i] < data["200_MA"].iloc[i]

        if macd_below_zero and price_above_200ma and not_already_bought:   # Buy
            buy_operation(data, data.index[i])
            position = 'buy'
            change_since_last_buy = data['Close'].iloc[i] - previous_buy_price if previous_buy_price != 0 else 0
            print(f"Buy with Histogram value: {data['Histogram'].iloc[i]:.4f}       Change since last buy: {change_since_last_buy:.2f}")
            previous_buy_price = data['Close'].iloc[i]  # Update the previous buy price

        elif histogram_is_negative and price_below_200ma and histogram_downwards_momentum_is_significant and we_are_in_a_trade:     # If in a downtrend and we are in a trade, sell
            sell_operation(data, data.index[i])
            position = 'sell'
            profit = data['Close'].iloc[i] - previous_buy_price  # Calculate profit from the buy price
            print(f"Sell with Histogram value: {data['Histogram'].iloc[i]:.4f}      Profit: {profit:.2f}")

    return data

def buy_operation(data, index):
    """Marks a buy signal and sets Position and Position_Change appropriately."""
    data.at[index, 'Position'] = 1
    data.at[index, 'Position_Change'] = 1
    
def sell_operation(data, index):
    """Marks a sell signal and sets Position and Position_Change appropriately."""
    data.at[index, 'Position'] = 0
    data.at[index, 'Position_Change'] = -1

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
    ax1.plot(data['200_MA'], label='200 Day MA', color='red')  # Plot the 200 day moving average
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