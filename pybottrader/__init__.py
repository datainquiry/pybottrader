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

from .indicators import *  # Import the C++ module directly
