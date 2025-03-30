"""

# PyBotTrader - A library to build trader bots

PyBotTrader is an experimental Python library designed to help create trading
bots, particularly for retail traders. It offers tools for real-time financial
analysis, including indicators like moving averages (like MA, EMA, RSI, MACD, and
ROI), which update dynamically with new data. The library includes data streamers
to handle sequential data from sources like CSV files or the YFinance API, and
basic portfolio managers for back-testing simple buy/sell strategies. Users can
define custom strategies that integrate data streams, indicators, and
decision-making rules to generate trading signals. A basic trader module is
included for testing strategies, making the library a versatile framework for
algorithmic trading experimentation.

Installation:

```
pip install pybottrader
```
"""

from __future__ import annotations
from pybottrader.indicators._indicators import ATR
from pybottrader.indicators._indicators import EMA
from pybottrader.indicators._indicators import FloatIndicator
from pybottrader.indicators._indicators import MA
from pybottrader.indicators._indicators import MACD
from pybottrader.indicators._indicators import MACDIndicator
from pybottrader.indicators._indicators import MACDResult
from pybottrader.indicators._indicators import MV
from pybottrader.indicators._indicators import ROI
from pybottrader.indicators._indicators import RSI
from pybottrader.indicators._indicators import roi
from . import indicators

__all__ = [
    "ATR",
    "EMA",
    "FloatIndicator",
    "MA",
    "MACD",
    "MACDIndicator",
    "MACDResult",
    "MV",
    "ROI",
    "RSI",
    "indicators",
    "roi",
]
