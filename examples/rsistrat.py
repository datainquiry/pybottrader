"""
Example of a simple strategy based the RSI indicator. When RSI is less than a
given number (usually 30), a sell position is deliverated. On the other hand,
when RSI is greater than a given number (usually 70), a buy position is
deliverated. Otherwise, the position deliverated is stay.
"""

import argparse
from datetime import date, timedelta
from pybottrader.datastreamers import YFHistory
from pybottrader.portfolios import DummyPortfolio
from pybottrader.strategies import SimpleRSI
from pybottrader.traders import Trader

# Default dates
start_date = "2021-01-01"
end_date = "2023-12-31"

# Parsing command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--symbol", type=str, default="AAPL", help="Ticker symbol")
parser.add_argument("--start", type=str, default=start_date, help="Start date")
parser.add_argument("--end", type=str, default=end_date, help="End date")
parser.add_argument("--initial_cash", type=float, default=1000.0, help="Initial cash")
parser.add_argument("--lower", type=float, default=30.0, help="Lower RSI band")
parser.add_argument("--upper", type=float, default=70.0, help="Upper RSI band")
args = parser.parse_args()

# Apple, daily data
datastream = YFHistory(args.symbol, start=args.start, end=args.end)
# Start with USD 1,000
portfolio = DummyPortfolio(args.initial_cash)
# My strategy
strategy = SimpleRSI(lower_band=args.lower, upper_band=args.upper)
# Putting everything together
trader = Trader(strategy, portfolio, datastream)
# A default runner, but you can implement your own loop
trader.run()
