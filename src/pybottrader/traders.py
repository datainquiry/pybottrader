"""A collection of bottraders"""

from typing import Union
from datetime import datetime
from attrs import define, asdict
from .datastreamers import DataStreamer
from .portfolios import Portfolio
from .strategies import Strategy, Position, StrategySignal
from .indicators import roi


@define
class TradingIteration:
    """Used to report results from a trading iteration"""

    signal: StrategySignal
    data: dict
    roi: Union[float, None]
    portfolio_value: float
    accumulated_roi: Union[float, None]


class Trader:
    """Base class"""

    portfolio: Portfolio
    datastream: DataStreamer
    strategy: Strategy
    last_result: Union[TradingIteration, None] = None
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
        """Perfoms a trading iteration"""
        obs = self.datastream.next()
        if obs is None:
            return False
        signal = self.strategy.evaluate(**obs)
        self.portfolio.process(**asdict(signal))
        self.last_result = TradingIteration(
            signal=signal,
            data=obs,
            roi=roi(self.last_valuation, self.portfolio.valuation()),
            portfolio_value=self.portfolio.valuation(),
            accumulated_roi=self.portfolio.accumulated_return(),
        )
        self.last_valuation = self.portfolio.valuation()
        return True

    def status(self) -> TradingIteration:
        """Trader last result"""
        return self.last_result

    def run(self):
        """A default runner"""
        # A nice header
        print(
            "{:26} {:4} {:>10} {:>10}  {:>10} {:>10}".format(  # pylint: disable=consider-using-f-string
                "Time", "Pos.", "Price", "ROI", "Valuation", "Accum.ROI"
            )
        )
        # Run the back-testing
        while self.next():
            status = self.status()
            if status.signal.position != Position.STAY:
                # A nice output
                print(
                    f"{status.signal.time} {status.signal.position.name:4} {status.data['close']:10.2f} "
                    + f"{status.roi * 100.0:10.2f}% {status.portfolio_value:10.2f} "
                    + f"{status.accumulated_roi * 100.0:10.2f}%"
                )
