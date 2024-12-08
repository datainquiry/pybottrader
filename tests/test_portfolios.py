from pybottrader.portfolios import *
from pybottrader.strategies import Position


class TestBasePortfolio:
    def setup_method(self):
        self.portfolio = Portfolio(cash=1000.0)

    def test_constructor(self):
        assert abs(self.portfolio.initial_cash - 1000.0) < 1e-6
        assert self.portfolio.last_position == Position.STAY
        assert self.portfolio.last_price < 1e-6
        assert self.portfolio.last_ticker == ""

    def test_process(self):
        self.portfolio.process(ticker="AAPL", position=Position.BUY, price=100.0)
        assert self.portfolio.last_ticker == "AAPL"
        assert self.portfolio.last_position == Position.BUY
        assert abs(self.portfolio.last_price - 100.0) < 1e-6

    def test_valuation(self):
        assert abs(self.portfolio.valuation() - 1000.0) < 1e-6
        self.portfolio.process(ticker="AAPL", position=Position.BUY, price=100.0)
        assert abs(self.portfolio.valuation() - 1000.0) < 1e-6

    def test_accumulated_return(self):
        assert self.portfolio.accumulated_return() < 1e-6
        self.portfolio.process(ticker="AAPL", position=Position.BUY, price=100.0)
        assert self.portfolio.accumulated_return() < 1e-6


class TestDummyPortafolio:
    def setup_method(self):
        self.portfolio = DummyPortfolio(cash=1000.0)

    def test_constructor(self):
        assert abs(self.portfolio.cash - 1000.0) < 1e-6
        assert self.portfolio.share_units < 1e-6
        assert abs(self.portfolio.initial_cash - 1000.0) < 1e-6
        assert self.portfolio.last_position == Position.STAY
        assert abs(self.portfolio.last_price) < 1e-6
        assert self.portfolio.last_ticker == ""

    def test_buy(self):
        self.portfolio.process(position=Position.BUY, price=10.0)
        assert self.portfolio.last_position == Position.BUY
        assert abs(self.portfolio.last_price - 10.0) < 1e-6
        assert self.portfolio.cash < 1e-6
        assert abs(self.portfolio.share_units - 100.0) < 1e-6
        # Trying to buy without cash
        self.portfolio.process(position=Position.BUY, price=10.0)
        assert self.portfolio.cash < 1e-6
        assert abs(self.portfolio.share_units - 100.0) < 1e-6

    def test_sell(self):
        # Trying to sell without having any share
        self.portfolio.process(position=Position.SELL, price=10.0)
        assert abs(self.portfolio.cash - 1000.0) < 1e-6
        assert self.portfolio.share_units < 1e-6
        # Buying and selling at the same price
        self.portfolio.process(position=Position.BUY, price=10.0)
        self.portfolio.process(position=Position.SELL, price=10.0)
        assert abs(self.portfolio.cash - 1000.0) < 1e-6
        assert self.portfolio.share_units < 1e-6
        # Buying and selling at different price
        self.portfolio.process(position=Position.BUY, price=10.0)
        self.portfolio.process(position=Position.SELL, price=12.0)
        assert abs(self.portfolio.cash - 1200.0) < 1e-6
        assert self.portfolio.share_units < 1e-6

    def test_valuation(self):
        assert abs(self.portfolio.valuation() - 1000.0) < 1e-6
        self.portfolio.process(position=Position.BUY, price=10.0)
        assert abs(self.portfolio.valuation() - 1000.0) < 1e-6
        self.portfolio.process(position=Position.SELL, price=12.0)
        assert abs(self.portfolio.valuation() - 1200.0) < 1e-6

    def test_accumulated_return(self):
        assert self.portfolio.accumulated_return() < 1e-6
        self.portfolio.process(position=Position.BUY, price=10.0)
        assert self.portfolio.accumulated_return() < 1e-6
        self.portfolio.process(position=Position.SELL, price=12.0)
        assert abs(self.portfolio.accumulated_return() - 0.2) < 1e-6
