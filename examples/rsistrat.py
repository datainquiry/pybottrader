"""
Example of a simple strategy based the RSI indicator. When RSI is less than a
given number (usually 30), a sell position is deliverated. On the other hand,
when RSI is greater than a given number (usually 70), a buy position is
deliverated. Otherwise, the position deliverated is stay.
"""

from pybottrader.datastreamers import YFHistory
from pybottrader.portfolios import DummyPortfolio
from pybottrader.strategies import SimpleRSI
from pybottrader.traders import Trader

# Apple, daily data from 2021 to 2023
datastream = YFHistory("AAPL", start="2021-01-01", end="2023-12-31")
# Start with USD 1,000
portfolio = DummyPortfolio(1000.0)
# My strategy
strategy = SimpleRSI(lower_band=30.0, upper_band=70.0)
# Putting everything together
trader = Trader(strategy, portfolio, datastream)
# A default runner, but you can implement your own loop
trader.run()
