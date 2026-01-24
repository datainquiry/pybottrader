"""
Scanner Example

A scanner is intended to apply a set of strategies over a
data stream.
"""

# In this example, two strategies are applied
from pybottrader.strategies import (
    SimpleRSI,
    CrossOver,
)

# The data stream is from Yahoo Finance (c)
from pybottrader.datastreamers import YFHistory

# The default scanner
from pybottrader.scanners import Scanner

# Data between 2021 and 2024
streamer = YFHistory("AAPL", start="2021-01-01", end="2024-12-31")
# Initializing the strategies
strats = [
    SimpleRSI(lower_band=30, upper_band=70),
    CrossOver(short_period=10, long_period=60, threshold=0.0),
]
# Setting and running the scanner
scanner = Scanner(strats, streamer)
# Using the default runner
scanner.run()
