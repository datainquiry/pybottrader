"""Strategies"""

from enum import Enum


class Position(Enum):
    """Trading Positions"""

    STAY = 1
    BUY = 2
    SELL = 3


class Strategy:
    """Base class for strategies"""

    def __init__(self, *args, **kwargs):
        """
        Init Method. Included for future support.
        """

    def evaluate(self, *args, **kwargs) -> Position:
        """
        Evaluate method. Include for future support
        """
        # The default position is STAY
        return Position.STAY
