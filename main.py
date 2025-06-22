from dataloader import get_price_data
from backtest import run_backtest
from strategies.ma_crossover import run_ma_crossover_strategy
from strategies.macd_strategy import run_macd_strategy
from strategies.macd_improved import run_macd_strategy_improved
from strategies.buy_and_hold import run_buy_and_hold_strategy

def main():
    # Display a welcome message.
    print("Welcome to Galen's trading strategy testing grounds!\n" \
    "This program will run a trading strategy on a stock of your choice.\n" \
    "Please enter a stock ticker: ") 
    # Removed stock ticker selection for testing.
    # Display list of strats to choose from.
    print("Enter a strategy: \n" \
          "\t1. MA Crossover\n" \
          "\t2. MACD\n" \
          "\t3. MACD Improved\n" \
            "\t4. Buy and Hold") 

    # Get the strategy from the user.
    strategy = input("Select a trading strategy:") 

    # Declaring these variables here allows us to use it for buy and hold.
    startDate = '2024-06-20' 
    endDate = '2025-06-20'
    stockTicker = 'PMT'

    data = get_price_data(stockTicker, startDate, endDate) # Assign stock and testing period. - Get the price data for that.

    if strategy == "MA Crossover" or strategy == "1":
        print("Running Moving Average Crossover Strategy...")
        data = run_ma_crossover_strategy(data)
        run_backtest(data)

    elif strategy == "MACD" or strategy == "2":
        print("Running MACD Strategy...")
        data = run_macd_strategy(data) 
        run_backtest(data)

    elif strategy == "MACD Improved" or strategy == "3":
        print("Running Improved MACD Strategy...")
        data = run_macd_strategy_improved(data)
        run_backtest(data)

    elif strategy == "Buy and Hold" or strategy == "4":
        print("Running buy and hold strategy...")
        # Super simple strat used to measure other strategies.
        data = run_buy_and_hold_strategy(data, startDate, endDate)
        print(f"Returns: {data:.2f}%")
        
    else:
        print(f"Strategy '{strategy}' is not a valid strategy")

if __name__ == "__main__":
    main()