"""Scanner Example"""

import attrs
from pybottrader.strategies import (
    SimpleRSI,
    CrossOver,
)
from pybottrader.strategies import Position
from pybottrader.datastreamers.yfinance import YFHistory
from pybottrader.scanners import Scanner

streamer = YFHistory("AAPL", start="2021-01-01", end="2024-12-31")
strat1 = SimpleRSI()
strat2 = CrossOver(short_period=30, long_period=120, threshold=0.1)
scanner = Scanner([strat1, strat2], streamer)
scanner.run()
