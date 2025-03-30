"""Data types"""

from typing import NewType, Literal

TickerSymbol = NewType("TickerSymbol", str)
DateStamp = NewType("DateStamp", str)
TimeFrame = NewType("TimeFrame", Literal["1m", "5m", "15m", "30m", "1h", "1d"])
