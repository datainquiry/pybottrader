from typing import Union
from enum import Enum
from datetime import datetime
from attrs import define


class Position(Enum):
    """Trading Positions"""

    STAY = 1
    BUY = 2
    SELL = 3


@define
class StrategySignal:
    """To report computations of an strategy"""

    time: datetime = datetime.now().timestamp()
    position: Position = Position.STAY
    price: float = 0.0
    symbol: str = ""
    exchange: str = ""
    name: str = ""


class Strategy:
    """Base class for strategies"""

    def __init__(self, *args, **kwargs):
        """
        Init Method. Included for future support.
        """

    def evaluate(self, data: Union[dict, None]) -> StrategySignal:
        """
        Evaluate method. Include for future support
        """
        # The default position is STAY
        return StrategySignal(name=type(self).__name__)
