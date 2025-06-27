import matplotlib.pyplot as plt


def run_ma_crossover_strategy(data):
    """
    Run the moving average crossover strategy on the provided data.
    """
    data = calculate_moving_average(data, 8, 'SHORT_MA')
    data = calculate_moving_average(data, 50, 'LONG_MA')
    data = crossover_logic(data)
    plot_strategy(data)
    return data

# Called twice, once for the long average once for the short average.
def calculate_moving_average(df, window, column_name):
        """
        Calculate a move average of a specific stock in a specific window
        """
        df[column_name] = df['Close'].rolling(window=window, min_periods=1).mean()
        return df

# Crossover logic: Buy when SHORT_MA crosses above LONG_MA, sell when it crosses below.
def crossover_logic(df):
    """
    Apply crossover logic to the DataFrame.
    """
    position = 'neutral'  # No position by default
    df['Position'] = 0  # Initialize Position column
    df['Position_Change'] = 0  # Initialize Position_Change column

    # Long moving average crosses above short moving average - and the previous day was not the case
    long_crosses_over_short = ((df['LONG_MA'] > df['SHORT_MA']) & (df['LONG_MA'].shift(1) <= df['SHORT_MA'].shift(1)) )
    
    # Short moving average crosses above long moving average -  and the previous day was not the case
    short_crosses_over_long = ((df['SHORT_MA'] > df['LONG_MA']) & (df['SHORT_MA'].shift(1) <= df['LONG_MA'].shift(1)))

    for i in range(1, len(df)):
        if long_crosses_over_short.iloc[i] and position != 'sell':
            sell_operation(df, i)
            position = 'sell'
        elif short_crosses_over_long.iloc[i] and position == 'sell':
            buy_operation(df, i)
            position = 'buy'
        else:
            df.at[df.index[i], 'Position'] = df.at[df.index[i-1], 'Position']
            df.at[df.index[i], 'Position_Change'] = 0

    return df

def buy_operation(data, index):
    """Marks a buy signal and sets Position and Position_Change appropriately."""
    data.at[data.index[index], 'Position'] = 1
    data.at[data.index[index], 'Position_Change'] = 1

def sell_operation(data, index):
    """Marks a sell signal and sets Position and Position_Change appropriately."""
    data.at[data.index[index], 'Position'] = 0
    data.at[data.index[index], 'Position_Change'] = -1

def plot_strategy(data):
    """
    Plot the moving averages and the closing price.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', alpha = 0.3)
    plt.plot(data['SHORT_MA'], label='Short Moving Average')
    plt.plot(data['LONG_MA'], label='Long Moving Average')
    
    # Plot buy signals (buy signals are mapped when position changes to 1)
    buy_signals = data[data['Position_Change'] == 1]
    for idx in buy_signals.index:
        plt.scatter(idx, buy_signals['Close'].loc[idx], marker='^', color='g', label='', s=100)

    # Plot sell signals (sell signals are mapped when position changes to 0)
    sell_signals = data[data['Position_Change'] == -1]
    for idx in sell_signals.index:
        plt.scatter(idx, sell_signals['Close'].loc[idx], marker='v', color='r', label='', s=100)

    plt.title('Moving Average Crossover Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()