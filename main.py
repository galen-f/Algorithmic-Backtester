from dataloader import get_price_data
from backtest import run_backtest
from strategies.ma_crossover import run_ma_crossover_strategy
from strategies.macd_strategy import run_macd_strategy

def main():
    print("Welcome to Galen's trading strategy testing grounds!\n" \
    "This program will run a trading strategy on a stock of your choice.\n" \
    "Please enter a stock ticker: ")
    print("Enter a strategy: \n" \
    "\tMA Crossover\n" \
    "\tMACD")
    strategy =input("Select a trading strategy:")
    data = get_price_data('NVDA', '2024-06-20', '2025-06-20') # Assign stock and testing period.
    # strategy_name = "MACD" # Assign strategy to run.

    if strategy == "MA Crossover":
        print("Running Moving Average Crossover Strategy...")
        data = run_ma_crossover_strategy(data)
        run_backtest(data)
    elif strategy == "MACD":
        print("Running MACD Strategy...")
        data = run_macd_strategy(data) 
        run_backtest(data)
    else:
        print(f"Strategy '{strategy_name}' is not a valid strategy")

if __name__ == "__main__":
    main()