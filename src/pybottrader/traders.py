"""A collection of bottraders"""

from typing import Union
from .datastreamers import DataStreamer, StreamIteration
from .portfolios import Portfolio
from .strategies import Strategy, Position
from .indicators import roi


class Trader:
    """Base class"""

    portfolio: Portfolio
    datastream: DataStreamer
    strategy: Strategy
    last_result: Union[StreamIteration, None] = None
    last_valuation: float = 0.0

    def __init__(
        self,
        strategy: Strategy,
        portfolio: Portfolio,
        datastream: DataStreamer,
    ):
        """Init method"""
        self.datastream = datastream
        self.portfolio = portfolio
        self.strategy = strategy

    def next(self) -> bool:
        obs = self.datastream.next()
        if obs is None:
            return False
        pos = self.strategy.evaluate(**obs)
        self.portfolio.process(position=pos, price=obs["close"])
        self.last_result = StreamIteration(
            time=obs["time"],
            position=pos,
            data=obs,
            roi=roi(self.last_valuation, self.portfolio.valuation()),
            portfolio_value=self.portfolio.valuation(),
            accumulated_roi=self.portfolio.accumulated_return(),
        )
        self.last_valuation = self.portfolio.valuation()
        return True

    def status(self) -> StreamIteration:
        """Trader last result"""
        return self.last_result

    def run(self):
        while self.next():
            status = self.status()
            # Printing status after BUY or SELL
            if status.position != Position.STAY:
                print(
                    f"{status.time}  "
                    + f"{status.position.name:5}  "
                    + f"{status.data['close']:10.2f} USD  "
                    + f"ROI {status.roi * 100.0:5.1f} %  "
                    f"Accum. ROI {status.accumulated_roi * 100.0:5.1f} %"
                )
