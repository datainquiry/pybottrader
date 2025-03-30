"""
Example of a simple strategy based the RSI indicator.  When RSI is less than a
given number (usually 30), a sell position is deliverated. On the other hand,
when RSI is greater than a given number (usually 70), a buy position is
deliverated. Otherwise, the position deliverated is stay.
"""

from pybottrader.indicators import RSI
from pybottrader.datastreamers.yfinance import YFHistory
from pybottrader.portfolios import DummyPortfolio
from pybottrader.strategies import CrossOver
from pybottrader.traders import Trader

# Apple, daily data from 2021 to 2023
datastream = YFHistory("AAPL", start="2021-01-01", end="2023-12-31")
# Start with USD 1,000
portfolio = DummyPortfolio(1000.0)
# My strategy
strategy = CrossOver(short_period=10, long_period=30, threshold=0.05)
# Putting everything eogether
trader = Trader(strategy, portfolio, datastream)
# A default runner, but you can implement your own loop
trader.run()
