"""
# Portfolio Managers

Portfolio managers, to implement buy/sell policies and deliver orders.
Currently only a `DummyPortfolio` is implemented, one that when receives a `buy`
signal buys everything that it can with its available cash, and sells all its
assets when receives a `sell` signal. This portfolio can be used for
back-testing.
"""

from .strategies import Position, StrategySignal
from .indicators import roi


class Portfolio:
    """Base Portfolio Class"""

    initial_cash: float
    last_position: Position
    last_exchange: str
    last_price: float
    last_ticker: str

    def __init__(self, cash: float = 1000.0):
        """Init method"""
        self.initial_cash = cash
        self.last_position = Position.STAY
        self.last_price = 0.0
        self.last_ticker = ""
        self.last_exchange = ""

    def process(self, signal: StrategySignal):
        """Process signal"""
        self.last_ticker = signal.ticker
        self.last_price = signal.price
        self.last_position = signal.position
        self.last_exchange = signal.exchange

    def valuation(self) -> float:
        """Default valuation method"""
        return self.initial_cash

    def accumulated_return(self) -> float:
        """Accumulated ROI"""
        return roi(self.initial_cash, self.valuation())


class DummyPortfolio(Portfolio):
    """
    Dummy portfolio is the most basic portfolio model.
    It works with only one asset. When it receives the buy signal,
    it uses all the available cash to buy the asset. When it receives
    the sell signal, it sells all the shares of the asset.
    """

    cash: float
    share_units: float
    share_price: float

    def __init__(self, cash: float = 1000.0):
        super().__init__(cash)
        self.cash = cash
        self.share_units = 0.0
        self.share_price = 0.0

    def process(self, signal: StrategySignal):
        super().process(signal)
        if signal.position == Position.BUY:
            if self.cash == 0.0:
                return
            self.share_units = self.cash / signal.price
            self.share_price = signal.price
            self.cash = 0.0
        elif signal.position == Position.SELL:
            if self.share_units == 0.0:
                return
            self.cash = self.share_units * signal.price
            self.share_price = signal.price
            self.share_units = 0.0

    def valuation(self) -> float:
        return self.cash if self.cash > 0.0 else (self.share_price * self.share_units)
