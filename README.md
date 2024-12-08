# PyBotTrader

API Documentation <https://jailop.github.io/pybottrader/pybottrader.html>

An experimental Python library to implement trading bots. I'm building this
library based on patterns I've observed implementing trading algorithms for my
clients. It is intended, when it becomes stable, to be used by retail traders.

## Features

- Financial indicators for streaming data. They don´t make calculations from
  scratch but instead by keeping memory of previous results (intended to be use
  with real time data). An `update` method is used to push new data and update
  their results. They use a bracket notation to bring access to results, like
  `ind[0]` for the most recent result and `ind[-1]` for the previous one.
  Current implemented indicators are `MA` (simple moving average), `EMA`
  (exponential moving average), `RSI` (Relative Strength Index), `MACD` (Moving
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

## Example

Using this library looks like:

``` python
from pybottrader.indicators import RSI
from pybottrader.datastreamers import YFinanceStreamer
from pybottrader.portfolios import DummyPortfolio
from pybottrader.traders import Trader
from pybottrader.strategies import Strategy, Position, StrategySignal

class SimpleRSIStrategy(Strategy):
    rsi: RSI
    last_flip = Position.SELL
    lower_band: float
    upper_band: float

    def __init__(self, lower_band=30.0, upper_band=70.0):
        self.rsi = RSI()
        self.lower_band = lower_band
        self.upper_band = upper_band

    def evaluate(self, *args, **kwargs) -> StrategySignal:
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
        if self.last_flip == Position.SELL and self.rsi[0] < self.lower_band:
            position = Position.BUY
            self.last_flip = Position.BUY
        # If RSI is greater than 70, sell
        elif self.last_flip == Position.BUY and self.rsi[0] > self.upper_band:
            position = Position.SELL
            self.last_flip = Position.SELL
        return StrategySignal(
            time=kwargs["time"], price=kwargs["close"], position=position
        )

# Apple, daily data from 2021 to 2023
datastream = YFinanceStreamer("AAPL", start="2021-01-01", end="2023-12-31")
# Start with USD 1,000
portfolio = DummyPortfolio(1000.0)
# My strategy
strategy = SimpleRSIStrategy(lower_band=25.0, upper_band=75.0)

# Putting everything together
trader = Trader(strategy, portfolio, datastream)
trader.run()
```

Output is shown below.

```
Time                       Pos.      Price        ROI   Valuation  Accum.ROI
2021-02-11 00:00:00-05:00 BUY      132.33       0.00%    1000.00       0.00%
2021-06-21 00:00:00-04:00 SELL     129.78      -1.93%     980.72      -1.93%
2021-09-20 00:00:00-04:00 BUY      140.43       0.00%     980.72      -1.93%
2021-10-22 00:00:00-04:00 SELL     146.08       4.02%    1020.17       2.02%
2022-05-24 00:00:00-04:00 BUY      138.48       0.00%    1020.17       2.02%
2022-07-08 00:00:00-04:00 SELL     145.07       4.76%    1068.72       6.87%
2022-09-02 00:00:00-04:00 BUY      153.93       0.00%    1068.72       6.87%
2023-01-24 00:00:00-05:00 SELL     141.05      -8.37%     979.26      -2.07%
2023-08-07 00:00:00-04:00 BUY      177.50       0.00%     979.26      -2.07%
2023-10-12 00:00:00-04:00 SELL     179.59       1.18%     990.78      -0.92%
```

## Installation

```sh
pip install pybottrader
```

Shortly, I'm going to release more documentation and more examples.
