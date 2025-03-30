"""
A basic strategy based on crossover moving averages
"""

from ..indicators import MA
from .base import Strategy, StrategySignal, Position


class CrossOver(Strategy):
    """Moving Average Crossover Strategy"""

    short_ma: MA
    long_ma: MA
    threshold: float
    last_flip = Position.SELL

    def __init__(self, short_period: int, long_period: int, threshold=0.0):
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
        if self.last_flip == Position.SELL and self.short_ma[0] > upper_band:
            position = Position.BUY
            self.last_flip = Position.BUY
        elif self.last_flip == Position.BUY and self.short_ma[0] < lower_band:
            position = Position.SELL
            self.last_flip = Position.SELL
        return StrategySignal(
            time=data["time"],
            price=data["close"],
            position=position,
        )
