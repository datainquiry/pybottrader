"""
TRADING PORTFOLIO MODELS

This module has beed adapted from:
https://github.com/jailop/trading/tree/main/indicators-c%2B%2B
"""

from .strategies import Position
from .indicators import roi


class Portfolio:
    """Base Portfolio Class"""

    initial_cash: float
    last_position: Position
    last_price: float
    last_ticker: str

    def __init__(self, cash: float = 1000.0):
        """Init method"""
        self.initial_cash = cash
        self.last_position = Position.STAY
        self.last_price = 0.0
        self.last_ticker = ""

    def process(
        self, ticker: str = "", position: Position = Position.STAY, price: float = 0.0
    ):
        """Process signal"""
        self.last_ticker = ticker
        self.last_price = price
        self.last_position = position

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

    def process(
        self, ticker: str = "", position: Position = Position.STAY, price: float = 0.0
    ):
        super().process(ticker=ticker, position=position, price=price)
        if position == Position.BUY:
            if self.cash == 0.0:
                return
            self.share_units = self.cash / price
            self.share_price = price
            self.cash = 0.0
        elif position == Position.SELL:
            if self.share_units == 0.0:
                return
            self.cash = self.share_units * price
            self.share_price = price
            self.share_units = 0.0

    def valuation(self) -> float:
        return self.cash if self.cash > 0.0 else (self.share_price * self.share_units)
