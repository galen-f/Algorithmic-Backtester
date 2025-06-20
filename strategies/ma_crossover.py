from dataloader import get_price_data
import numpy as np
import matplotlib.pyplot as plt


def run_ma_crossover_strategy(data):
    """
    Run the moving average crossover strategy on the provided data.
    """
    data = calculate_moving_average(data, 8, 'SHORT_MA')
    data = calculate_moving_average(data, 50, 'LONG_MA')
    data = crossover_logic(data)
    data = assign_positions(data)
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
    df['Signal'] = np.where(df['SHORT_MA'] > df['LONG_MA'], 1, -1) 
    df['Position_Change'] = df["Signal"].diff()
    return df

def assign_positions(df):
    """
    Assign positions based on the crossover signals.
    """
    df['Position'] = 0
    df.loc[df['Position_Change'] == 2, 'Position'] = 1  # Buy signal
    df.loc[df['Position_Change'] == -2, 'Position'] = 0  # Sell signal
    df['Position'] = df['Position'].ffill().fillna(0)
    return df

def plot_strategy(data):
    """
    Plot the moving averages and the closing price.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['SHORT_MA'], label='Short Moving Average', alpha=0.5)
    plt.plot(data['LONG_MA'], label='Long Moving Average', alpha=0.5)
    
    # Plot buy signals (buy signals are mapped when position changes to 1)
    buy_signals = data[data['Position_Change'] == 2]
    plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='g', label='Buy Signal', s=100)
    
    # Plot sell signals (sell signals are mapped when position changes to 0)
    sell_signals = data[data['Position_Change'] == -2]
    plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='r', label='Sell Signal', s=100)
    
    plt.title('Moving Average Crossover Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()