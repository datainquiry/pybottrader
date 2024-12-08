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
