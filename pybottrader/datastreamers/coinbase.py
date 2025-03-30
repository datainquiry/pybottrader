"""
Data Streamer for Coinbase
"""

import os
from typing import Optional
import logging
from datetime import datetime
import pandas as pd
from requests.exceptions import HTTPError
from coinbase.rest import RESTClient
from . import DataStreamer
from ..types import DateStamp, TickerSymbol, TimeFrame

LIMIT = 350  # Limit set by Coinbase


class CBHistory(DataStreamer):
    """Using Coinbase as a data streamer"""

    start: int
    end: int
    period: str
    client: Optional[RESTClient] = None

    def __init__(
        self,
        symbol: TickerSymbol,
        start: DateStamp,
        end: Optional[DateStamp],
        interval: TimeFrame = "1d",
    ):
        super().__init__()
        self.symbol = symbol

        # Setting the intervalo of time
        if interval == "1m":
            self.period = "ONE_MINUTE"
        elif interval == "5m":
            self.period = "FIVE_MINUTE"
        elif interval == "15m":
            self.period = "FIFTEEN_MINUTE"
        elif interval == "30m":
            self.period = "THIRTY_MINUTE"
        else:
            self.period = "ONE_DAY"

        # Setting start en end time
        if end:
            self.end = int(datetime.fromisoformat(end).timestamp())
        else:
            self.end = int(datetime.now().timestamp())
        factor = LIMIT * 60
        if self.period == "ONE_DAY":
            factor *= 60 * 24
        limit = self.end - factor
        self.start = int(datetime.fromisoformat(start).timestamp())
        self.start = self.start if self.start >= limit else limit

        # Credentials
        if not "COINBASE_API_KEY" in os.environ:
            logging.warning("COINBASE_API_KEY environment variable not defined")
            return
        if not "COINBASE_SECRET_KEY" in os.environ:
            logging.warning("COINBASE_SECRET_KEY environment variable not defined")
            return
        try:
            self.client = RESTClient(
                api_key=os.environ["COINBASE_API_KEY"],
                api_secret=os.environ["COINBASE_SECRET_KEY"],
            )
        except HTTPError:
            logging.warning("Connection to Coinbase failed")
            return
        self._retrieve_data()

    def _retrieve_data(self):
        if not self.client:
            return
        try:
            response = self.client.get_candles(
                self.symbol, self.start, self.end, self.period
            )
            self.data = (
                pd.DataFrame(
                    [candle.to_dict() for candle in response["candles"]]
                ).rename(columns={"start": "time"})
                # .set_index("time")
            )
            for col in ["open", "close", "low", "high", "volume"]:
                self.data[col] = self.data[col].astype(float)
        except HTTPError:
            logging.warning("Network error retrieving candles")
