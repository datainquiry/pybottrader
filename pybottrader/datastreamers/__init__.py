"""
# Data Streamers

Data streamers to read or retrieve sequential data. They provide a `next` method
to bring access to the next data item. Current data streamers implemented:
`CSVFileStreamer` and `YFinanceStreamer` (based on the `yfinace` library.)

"""

from typing import Optional
import pandas as pd
from .yfinance import YFHistory
from .base import DataStreamer
from .base import CSVFileStreamer

