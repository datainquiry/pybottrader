"""
Example of a simple strategy based the RSI indicator.  When RSI is less than a
given number (usually 30), a sell position is deliverated. On the other hand,
when RSI is greater than a given number (usually 70), a buy position is
deliverated. Otherwise, the position deliverated is stay.
"""

from pybottrader.indicators import RSI
from pybottrader.datastreamers.yfinance import YFHistory
from pybottrader.portfolios import DummyPortfolio
from pybottrader.strategies import Strategy, Position, StrategySignal
from pybottrader.traders import Trader


class SimpleRSIStrategy(Strategy):
    """A simple strategy based on the RSI indicator"""

    rsi: RSI
    last_flip = Position.SELL
    lower_band: float
    upper_band: float

    def __init__(self, lower_band=30.0, upper_band=70.0):
        self.rsi = RSI()
        self.lower_band = lower_band
        self.upper_band = upper_band

    def evaluate(self, data) -> StrategySignal:
        # default positio STAY
        position = Position.STAY
        # Update the RSI indicator
        self.rsi.update(open_price=data["open"], close_price=data["close"])
        # Make the decision what position to advice
        if self.last_flip == Position.SELL and self.rsi[0] < self.lower_band:
            position = Position.BUY
            self.last_flip = Position.BUY
        elif self.last_flip == Position.BUY and self.rsi[0] > self.upper_band:
            position = Position.SELL
            self.last_flip = Position.SELL
        return StrategySignal(time=data["time"], price=data["close"], position=position)


# Apple, daily data from 2021 to 2023
datastream = YFHistory("AAPL", start="2021-01-01", end="2023-12-31")
# Start with USD 1,000
portfolio = DummyPortfolio(1000.0)
# My strategy
strategy = SimpleRSIStrategy(lower_band=25.0, upper_band=75.0)

# Putting everything together
trader = Trader(strategy, portfolio, datastream)
# A default runner, but you can implement your own loop
trader.run()
