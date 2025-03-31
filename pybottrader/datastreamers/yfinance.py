"""
Data streamear for yfinance
"""

from typing import Union
from datetime import datetime
import numpy as np
import yfinance
from . import DataStreamer
from ..types import DateStamp, TickerSymbol, TimeFrame


class YFHistory(DataStreamer):
    """Using Yahoo Finance to retrieve data"""

    def __init__(
        self,
        symbol: TickerSymbol,
        start: DateStamp,
        end: Union[DateStamp, None] = None,
        interval: TimeFrame = "1d",
    ):
        super().__init__()
        self.symbol = symbol
        ticker = yfinance.Ticker(symbol)
        if end is None:
            end = datetime.now().isoformat()
        self.data = ticker.history(start=start, end=end, interval=interval)
        self.data.columns = [col.lower() for col in self.data.columns]
        self.data.index.names = ["time"]
        self.data.index = self.data.index.astype(np.int64) / 1e9
        self.data.reset_index(inplace=True)
