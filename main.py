from dataloader import get_price_data
from backtest import run_backtest
from strategies.ma_crossover import run_ma_crossover_strategy

def main():
    print("Welcome to Galen's trading strategy testing grounds!")
    data = get_price_data('QQQ', '2020-01-01', '2020-12-31') # Assign stock and testing period.
    strategy_name = "MA Crossover" # Assign strategy to run.

    if strategy_name == "MA Crossover":
        print("Running Moving Average Crossover Strategy...")
        run_backtest(data)
        data = run_ma_crossover_strategy(data)
        
    else:
        print(f"Strategy '{strategy_name}' is not implemented yet.")

if __name__ == "__main__":
    main()