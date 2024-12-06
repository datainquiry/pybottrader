"""Data Streamers"""

from typing import Union
from attrs import define
import pandas as pd
from .strategies import Position


@define
class StreamIteration:
    """Used to report results from a stream iteration"""

    time: pd.Timestamp
    position: Position
    data: dict
    roi: Union[float, None]
    portfolio_value: float
    accumulated_roi: Union[float, None]


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
