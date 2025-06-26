from dataloader import get_price_data

import pandas as pd

def run_backtest(data):

    data = data.copy()  # Create a copy of the data to avoid modifying the original DataFrame

    # Initialize Position and Position_Change columns
    if 'Position' not in data.columns:
        data['Position'] = 0
    if 'Position_Change' not in data.columns:
        data['Position_Change'] = 0

    # fill forwards the position to maintain the last position until a new signal.
    data['Position'] = data['Position'].ffill().fillna(0)
    
    # Simulate initial Capital
    initial_capital = 10000

    # Calculate daily returns
    data['Daily_Return'] = data['Close'].pct_change()

    # Calculate the strategy returns: Position from previous day determines today's returns
    data['Strategy_Return'] = data['Position'].shift(1) * data['Daily_Return']

    #Simulate the capital over time.
    data['Capital'] = initial_capital * (1 + data['Strategy_Return']).cumprod()

    # print the daily information.
    print(f"{'Date':<10} {'Position':<10} {'Daily Return':<15} {'Strategy Return':<15} {'Capital':<10}")
    print("=" * 50)

    # Print the daily returns every day.
    for i in range(1, len(data)):
      date = data.index[i].date()
      position = data['Position'].iloc[i]
      daily_return = data['Daily_Return'].iloc[i] if not pd.isna(data['Daily_Return'].iloc[i]) else 0.0
      strategy_return = data['Strategy_Return'].iloc[i] if not pd.isna(data['Strategy_Return'].iloc[i]) else 0.0
      capital = data['Capital'].iloc[i]

      print(f"{date}    {position:<10}  {daily_return:<15.4f}   {strategy_return:<15.4f}    ${capital:<10.2f}")

    # Calculate total returns.
    total_capital = data['Capital'].iloc[-1]
    total_return_percentage = ((total_capital - initial_capital) / initial_capital) * 100
    position_changes = data['Position'].diff().fillna(0)
    num_trades = position_changes[position_changes != 0].count()
    days_in_position = (data['Position'] > 0).sum()
    total_days = len(data)
    percentage_of_days_in_position = (days_in_position / total_days) * 100
    buy_hold_return = buy_and_hold_returns(data)

    print(f"\n{'==' * 20}")
    print("BACKTEST RESULTS")
    print(f"Initial Capital:                 ${initial_capital:.2f}")
    print(f"Final Capital:                   ${total_capital:.2f}")
    print(f"Total Returns:                   {total_return_percentage:.2f}%")
    print(f"Number of Trades:                {num_trades}")
    print(f"Days in Position:                {days_in_position}")
    print(f"Total Days in Backtest:          {total_days}")
    print(f"Percentage of Days in Position:  {percentage_of_days_in_position:.2f}%")
    print(f"Buy & Hold Return:               {buy_hold_return:.2f}%")

    return data

def buy_and_hold_returns(data):
    initial_price = data['Close'].iloc[0]
    final_price = data['Close'].iloc[-1]
    return ((final_price - initial_price) / initial_price) * 100