# PyBotTrader

Version 0.0.4

API Documentation <https://jailop.github.io/pybottrader/pybottrader.html>

An experimental Python library to implement trading bots. I'm building this
library based on patterns I've observed implementing trading algorithms for my
clients. It is intended, when it becomes stable, to be used by retail traders.

Features:

- Financial indicators for streaming data. They don´t make calculations from
  scratch but instead by keeping memory of previous results (intended to be use
  with real time data). An `update` method is used to push new data and update
  their results. They use a bracket notation to bring access to results, like
  `ind[0]` for the most recent result and `ind[-1]` for the previous one.
  Current implemented indicators are `MA` (simple moving average), `EMA`
  (exponential moving average), RSI (Relative Strength Index), MACD (Moving
  average convergence/divergence), and `ROI` (return of investment). Check some
  examples in [this test
  file](https://github.com/jailop/pybottrader/blob/main/test/test_indicators.py).
- Data streamers to read or retrieve sequential data. They provide a `next`
  method to bring access to the next data item. Current data streamers
  implemented: `CSVFileStreamer` and `YFinanceStreamer` (based on the `yfinace`
  library.)
- Portfolio managers, to implement buy/sell policies and deliver orders.
  Currently only a `DummyPortfolio` is implemented, one that when receives a
  `buy` signal buys everything that it can with its available cash, and sells
  all its assets when receives a `sell` signal. This portfolio can be used for
  back-testing.
- A strategy model, so the user of this library can implement it owns strategies
  (this is the purpose of this library).  A strategy is built to consume a data
  stream, compute indicators, and produce BUY/SELL signals.
- Traders, these are bots that based on a data stream, a strategy, and a
  portfolio, run the trading operations. Currently only a basic Trader is
  offered, useful for back-testing.

Using this library looks like:

``` python
from pybottrader.indicators import RSI
from pybottrader.datastreamers import YFinanceStreamer
from pybottrader.portfolios import DummyPortfolio
from pybottrader.traders import Trader
from pybottrader.strategies import Strategy, Position

class SimpleRSIStrategy(Strategy):
    rsi: RSI
    last_flip = Position.SELL

    def __init__(self):
        self.rsi = RSI()

    def evaluate(self, *args, **kwargs) -> Position:
        # default positio STAY
        position = Position.STAY
        # It is expected that open and close values
        # are provided by the data streamer. Otherwise,
        # just return the default position (STAY)
        if "open" not in kwargs or "close" not in kwargs:
            return position
        # Update the RSI indicator
        self.rsi.update(open_price=kwargs["open"], close_price=kwargs["close"])
        # If RSI is less than 30, buy
        if self.last_flip == Position.SELL and self.rsi[0] < 30:
            position = Position.BUY
            self.last_flip = Position.BUY
        # If RSI is greater than 70, sell
        elif self.last_flip == Position.BUY and self.rsi[0] > 70:
            position = Position.SELL
            self.last_flip = Position.SELL
        return position

# Apple, daily data from 2021 to 2023
datastream = YFinanceStreamer("AAPL", start="2021-01-01", end="2023-12-31")
# Start with USD 1,000
portfolio = DummyPortfolio(1000)
# My strategy
strategy = SimpleRSIStrategy()
# Putting everything together
trader = Trader(strategy, portfolio, datastream)

# A nice header
print(
    "{:10} {:4} {:>10} {:>10}  {:>10} {:>10}".format(
        "Date", "Pos.", "Price", "ROI", "Valuation", "Accum.ROI"
    )
)

# Run the back-testing
while trader.next():
    status = trader.status()
    if status.position != Position.STAY:
        date = status.time.strftime("%Y-%m-%d")
        # A nice output
        print(
            f"{date} {status.position.name:4} {status.data['close']:10.2f} "
            + f"{status.roi * 100.0:10.2f}% {status.portfolio_value:10.2f} "
            + f"{status.accumulated_roi * 100.0:10.2f}%"
        )
```

Output is shown below. Using this strategy ended in a loss.

```
Date       Pos.      Price        ROI   Valuation  Accum.ROI
2021-02-10 BUY      132.59       0.00%    1000.00       0.00%
2021-04-09 SELL     130.25      -1.77%     982.35      -1.77%
2021-05-05 BUY      125.45       0.00%     982.35      -1.77%
2021-06-21 SELL     129.78       3.45%    1016.28       1.63%
2021-09-20 BUY      140.43      -0.00%    1016.28       1.63%
2021-10-20 SELL     146.64       4.42%    1061.21       6.12%
2022-01-24 BUY      159.02       0.00%    1061.21       6.12%
2022-03-25 SELL     172.12       8.24%    1148.69      14.87%
2022-04-25 BUY      160.46       0.00%    1148.69      14.87%
2022-06-08 SELL     145.98      -9.03%    1045.00       4.50%
2022-09-02 BUY      153.93       0.00%    1045.00       4.50%
2023-01-24 SELL     141.05      -8.37%     957.52      -4.25%
2023-08-04 BUY      180.62       0.00%     957.52      -4.25%
2023-10-10 SELL     177.29      -1.85%     939.85      -6.02%
```

Shortly, I'm going to release more documentation and more examples.
