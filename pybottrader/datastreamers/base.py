"""
Base classes for data streamers.
All datastreamer should inherit from DataStreamer.
"""

from typing import Optional
import pandas as pd


class DataStreamer:
    """A data streamer abstract class"""

    index = 0
    data = pd.DataFrame()
    symbol = ""
    label = ""

    def __init__(self):
        """Init method"""

    def next(self) -> Optional[dict]:
        """Returns the next observation"""
        if self.index >= len(self.data):
            return None
        result = self.data.iloc[self.index].to_dict()
        self.index += 1
        return result

    def result(self) -> Optional[dict]:
        """Returns the current observation"""
        if self.index >= len(self.data):
            return None
        return self.data.iloc[self.index].to_dict()

    def reset(self):
        """Resets the counter to 0"""
        self.index = 0

    @staticmethod
    def labels() -> dict:
        """Labeling helper"""
        return {
            "symbol": {"label": "Symbol", "help": "Ticker symbol"},
            "start": {"label": "Start", "help": "Starting datetime stamp"},
            "end": {"label": "End", "help": "Ending datetime stamp"},
            "invertal": {"label": "Interval", "help": "Aggregation period"},
        }


class CSVFileStreamer(DataStreamer):
    """
    An dataframe file streamer
    """

    data: pd.DataFrame
    index: int

    def __init__(self, filename: str):
        self.index = 0
        self.data = pd.read_csv(filename)
