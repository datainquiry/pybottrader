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
