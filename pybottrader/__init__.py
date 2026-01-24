"""
# PyBotTrader - A library to build trader bots

PyBotTrader is an experimental Python library designed to help create trading
bots, particularly for retail traders. It offers tools for real-time financial
analysis, including indicators like moving averages (like MA, EMA, RSI, MACD, and
ROI), which update dynamically with new data. The library includes data streamers
to handle sequential data from sources like CSV files or YFinance API, and
basic portfolio managers for back-testing simple buy/sell strategies. Users can
define custom strategies that integrate data streams, indicators, and
decision-making rules to generate trading signals. A basic trader module is
included for testing strategies, making it a library a versatile framework for
algorithmic trading experimentation.

Installation:

Basic installation (core functionality only):
```
pip install pybottrader
```

With UI components (Qt6-based charts and forms):
```
pip install pybottrader[ui]
```

The UI components are optional and only required if you need GUI functionality
for your trading applications.
"""

from .indicators import *


def has_ui_support():
    """Check if UI components are available"""
    try:
        __import__("PyQt6")
        __import__("PyQt6.QtCharts")
        return True
    except ImportError:
        return False


def import_ui():
    """Import UI components, raising a helpful error if not available"""
    if not has_ui_support():
        raise ImportError(
            "UI components are not available. Install with: pip install pybottrader[ui]"
        )
    from . import ui

    return ui
