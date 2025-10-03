"""
A basic strategy based on crossover moving averages
"""

from ..indicators import MA
from .base import Strategy, StrategySignal, Position

class CrossOver(Strategy):
    """
    A basic strategy based on crossover moving averages. Buys when the
    short moving average crosses above the long moving average,
    and sells when it crosses below. A threshold can be set to avoid
    whipsaws. The last_flip variable is used to track the last position
    change to prevent multiple buy/sell signals in a row.
    The threshold is a proportion above/below the long moving average
    to trigger a buy/sell signal.
    """

    short_ma: MA
    long_ma: MA
    threshold: float
    last_flip = Position.SELL

    def __init__(self, short_period: int, long_period: int, threshold=0.0):
        """
        :param short_period: Number of periods for the short moving average
        :param long_period: Number of periods for the long moving average
        :param threshold: Proportion above/below to flip position
        """
        self.short_ma = MA(short_period)
        self.long_ma = MA(long_period)
        self.threshold = threshold

    @staticmethod
    def labels() -> dict:
        """Labels for GUI builder"""
        return {
            "short_period": {
                "label": "Short duration",
                "help": "Number of periods for the short moving average",
            },
            "long": {
                "label": "Long duration",
                "help": "Number of periods for the long moving average",
            },
            "threshold": {
                "label": "Threshold",
                "help": "Proportion above/below to flip position",
            },
        }

    def evaluate(self, data) -> StrategySignal:
        position = Position.STAY
        if "time" not in data or "close" not in data:
            return StrategySignal()
        self.short_ma.update(data["close"])
        self.long_ma.update(data["close"])
        upper_band = self.long_ma[0] * (1 + self.threshold)
        lower_band = self.long_ma[0] * (1 - self.threshold)
        if self.last_flip == Position.SELL and self.short_ma[0] < lower_band:
            position = Position.BUY
        elif self.last_flip == Position.BUY and self.short_ma[0] > upper_band:
            position = Position.SELL
        if position != Position.STAY:
            self.last_flip = position
        return StrategySignal(
            time=data["time"],
            price=data["close"],
            position=position,
        )
