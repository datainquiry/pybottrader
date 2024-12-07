# PyBotTrader

Version 0.0.3

An experimental Python library to implement trading bots. I'm building this
library based on patterns I've observed implementing trading algorithms for my
clients. It is intended, when it becomes stable, to be used by retail traders.

Features:

- Financial indicators for streaming data. They don´t make calculations from
  scratch but instead by keeping memory of previous results (intended to be use
  with real time data). An `update` method is used to push new data and update
  their results. They use a bracket notation to bring access to results, like
  `ind[0]` for the most recent result and `ind[-1]` for the previous one. Current
  implemented indicators are `MA` (simple moving average), `EMA` (exponential moving
  average), and `ROI` (return of investment).
- Data streamers to read or retrieve sequential data. They provide a `next`
  method to bring access to the next data item. Current data streamers implemented:
  `CSVFileStreamer` and `YFinanceStreamer` (based on the `yfinace` library.)
- Portfolio managers, to implement buy/sell policies and deliver orders.
  Currently only a `DummyPortfolio` is implemented, one that when receives a
  `buy` signal buys everything that it can with its available cash, and sells
  all its assets when receives a `sell` signal. This portfolio can be used for
  back-testing.
- A strategy model, so the user of this library can implement it owns strategy.
  The purpose of a strategy is to consume a data stream and produce BUY/SELL
  signals.
- Traders, these are bot the based on a data stream, a strategy, and a portfolio,
  run the trading operations. Currently only a basic Trader is offered, useful
  for back-testing.

Using this library looks like:

```
from pybottrader.datastreamers import YFinanceStreamer
from pybottrader.portfolios import DummyPortfolio
from pybottrader.traders import Trader
from pybottrader.strategies import Strategy, Position

class MyStragety(Strategy):
    def __init__(self, ...):
        # Initilize your stuff
    def evaluate(self, *args, **kwargs) -> Position:
        # This method receives data sent by the data streamer
        # and computes signals
        if cond:
            return Position.BUY
        else if cond:
            return Position.SELL
        else:
            return Position.STAY

datastream = YFinanceStreamer("AAPL", period="1y")
portfolio = DummyPortfolio(1000)  # Initial cash
strategy = MyStragety()
trader = Trader(strategy, portfolio, datastream)
trader.run()
```

Shortly, I'm going to release more documentation and examples.
