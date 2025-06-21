# 📈 Trading Strategy Backtester
This is a python-based backtesting engine for evaluating stock trading strategies, using historical price data from Yahoo Finance and displaying it in user-friendly graphs.

---

## 🛠️ Features
- Fetches historical data from Yahoo Finance
- Implements various algorithmic trading strategies
- Simulates capital growth and calculates total returns
- Visualizes signals and price action
- CLI Interaction for selecting strategies and stocks

---

## 🧪 Strategies
### Buy-and-Hold
A simple strategy which buys a stock at a specific date (the start date) and sells it at another specified date (the end date). It's useful for testing other strategies.<br>
![BaH_Results](https://github.com/user-attachments/assets/223e0874-bc11-4266-b24e-7568a4e57218)<br>

### Moving Average Crossover
This strategy combines a short-term moving average with a long-term moving average. If the short-term moving average is greater than the long-term moving average, this indicates a bullish market, so we buy. If the short-term average is less, we sell.<br>
![MACrossover_Strat](https://github.com/user-attachments/assets/181a800f-a19b-4532-a9fe-25beea09ddf0)<br>

![MACrossover_results](https://github.com/user-attachments/assets/566deac7-d42e-429c-8eed-c48842a168e7)<br>

### Moving Average Convergence Divergence (MACD)
This is a widley used trading strategy. We once again take two moving averages, a long and a short, and take the moving average of those two moving averages, this gives us the MACD line. Then we take a moving average of the MACD line, this is the signal line. <br>

We can measure if the MACD line is above the Signal line, we want to be in a buy position, if the opposite is true, we want to be in a sell position.<br>
![MACD_Strat](https://github.com/user-attachments/assets/53868c8a-bc8d-4ca8-b2ce-443749739a14)<br>

![MACD_Results](https://github.com/user-attachments/assets/8ffc22b6-c1a2-4865-be86-1f9829dbd89f)<br>

### MACD+
This is a project of mine where I am trying to build an improved version of the MACD strategy, however, it is not yet complete.

---

## 🚀 Running
`
pip install yfinance pandas matplotlib
python main.py` <br>
Then follow the terminal prompts to input a strategy and run the backtest.

---

## Skills

### Technical Skills
- Python
- Pandas
- Matplotlib
- Algorithmic trading strategy implementation
- Backtesting Methodologies

### Financial Skills
- Technical Indicators (MA, EMA, MACD, ETC.)
- Historical Market Analysis
- Quantitative Research Methods
- Portfolio Simulation and Capital Compounding
- Signal Generation and Position Management
- Trading Strategies





