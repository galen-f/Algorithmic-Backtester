# 📈 Trading Strategy Backtester
This is a python-based backtesting engine for evaluating stock trading strategies, using historical price data from Yahoo Finance and displaying it in user-friendly graphs. Additionally presents metrics like the % of days in a trade, the Buy and Hold returns of the period, how many trades were made, etc. 

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
<img src="https://github.com/user-attachments/assets/223e0874-bc11-4266-b24e-7568a4e57218" width="325">

### Moving Average Crossover
This strategy combines a short-term moving average with a long-term moving average. If the short-term moving average is greater than the long-term moving average, this indicates a bullish market, so we buy. If the short-term average is less, we sell.<br>
<img src="https://github.com/user-attachments/assets/d9bd0c3a-4cb9-4df7-84cb-2f6b4cde0c5c" width="685">
<img src="https://github.com/user-attachments/assets/cd2fb10a-30e7-48a1-ae7e-739423e37677" width="322">

### Moving Average Convergence Divergence (MACD)
This is a widley used trading strategy. We once again take two moving averages, a long and a short, and take the moving average of those two moving averages, this gives us the MACD line. Then we take a moving average of the MACD line, this is the signal line. <br>

We can measure if the MACD line is above the Signal line, we want to be in a buy position, if the opposite is true, we want to be in a sell position.<br>
<img src="https://github.com/user-attachments/assets/a4711e43-efb4-4110-bbb1-ccdf186e6886" width="685">
<img src="https://github.com/user-attachments/assets/8eff9e65-7c98-419e-8b3e-21accfb17544" width="322">

### MACD+
An adjustment of the MACD strategy which includes more trend indicators, such as only buying if the MACD line is negative (undervalued) and the stock is above a 200 day EMA (Uptrend). Often too cautious to be profitable, but good at reducing losses in downtrending markets. <br>
<img src="https://github.com/user-attachments/assets/202e5d52-9c8b-411e-8453-c826d4d44b92" width="685">
<img src="https://github.com/user-attachments/assets/494d1b5a-adb4-4491-a180-9a35fae55caf" width="322">

### Agressive MACD
A further adjustment of the cautious MACD which attempts in increase the agressivness of the algorithm. Very profitable in bull markets but very vulnerable in bear markets. Increases the aggression by only selling when the downwards momentum is significant and below the 200 day EMA. <br>
<img src="https://github.com/user-attachments/assets/00b5aec5-5824-4cdb-91d3-c9cabcc9c117" width="685">
<img src="https://github.com/user-attachments/assets/95588f80-0060-42b8-aeae-0194d6a508ed" width="322">


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





