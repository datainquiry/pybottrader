"""
# Data Streamers

Data streamers to read or retrieve sequential data. They provide a `next` method
to bring access to the next data item. Current data streamers implemented:
`CSVFileStreamer` and `YFinanceStreamer` (based on the `yfinace` library.)

"""

from typing import Union
import pandas as pd
import yfinance


class DataStreamer:
    """A data streamer abstract class"""

    def __init__(self):
        """Init method"""

    def next(self) -> Union[dict, None]:
        """Next method"""


class CSVFileStreamer(DataStreamer):
    """
    An dataframe file streamer
    """

    data: pd.DataFrame
    index: int

    def __init__(self, filename: str):
        self.index = 0
        self.data = pd.read_csv(filename, parse_dates=True)

    def next(self) -> Union[dict, None]:
        if self.index >= len(self.data):
            return None
        result = self.data.iloc[self.index].to_dict()
        self.index += 1
        return result
