.. PyBotTrader documentation master file, created by
   sphinx-quickstart on Fri Dec 13 21:45:50 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyBotTrader documentation
=========================

PyBotTrader is an experimental Python library designed to help on creating
trading bots, intended for retail traders. It offers tools for real-time
financial analysis, including indicators like moving averages (like MA, EMA,
RSI, MACD, and ROI), which update dynamically with new data. The library
includes data streamers to handle sequential data from sources like CSV files or
the YFinance API, and basic portfolio managers for back-testing simple buy/sell
strategies. Users can define custom strategies that integrate data streams,
indicators, and decision-making rules to generate trading signals. A basic
trader module is included for testing strategies, making the library a versatile
framework for algorithmic trading experimentation.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   indicators
