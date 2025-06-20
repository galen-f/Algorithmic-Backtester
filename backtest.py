from dataloader import get_price_data

def run_backtest(data):
    # fill forwards the position to maintain the last position until a new signal.
    data['Position'] = data['Position'].ffill().fillna(0)

    #calculate daily returns.
    data['Daily_Return'] = data['Close'].pct_change()
    # Calculate strategy returns based on position.
    data['Strategy_Return'] = data['Position'].shift(1) * data['Daily_Return']

    # Simulate Capital
    initial_capital = 10000
    data['Capital'] = initial_capital * (1 + data['Strategy_Return']).cumprod()

    # Calculate total returns.
    total_capital = data['Capital'].iloc[-1]

    print(f"Total Capital after trading: ${total_capital:.2f}")
    print(f"Total Returns: {((total_capital - initial_capital) / initial_capital) * 100:.2f}%")
