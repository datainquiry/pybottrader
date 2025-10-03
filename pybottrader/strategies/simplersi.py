"""
A basic RSI strategy
"""

from ..indicators import RSI
from .base import Strategy, StrategySignal, Position


class SimpleRSI(Strategy):
    """
    Simple RSI is an strategy based on the direct application of
    the RSI indicator. The user can define the lower and upper bands
    to detect overbought and underbought conditions. When the RSI
    crosses below the lower band, a BUY signal is generated. When it
    crosses above the upper band, a SELL signal is generated.
    The strategy maintains the last position to avoid repeated signals.
    """

    rsi: RSI
    last_flip = Position.SELL
    lower_band: float
    upper_band: float

    def __init__(self, lower_band=30.0, upper_band=70.0):
        """
        Initialize the SimpleRSI strategy with specified lower and upper
        bands.
        """
        self.rsi = RSI()
        self.lower_band = lower_band
        self.upper_band = upper_band

    @staticmethod
    def labels() -> dict:
        """Labels for GUI builder"""
        return {
            "lower_band": {
                "label": "Lower Band",
                "help": "Band below which price is considered underbought",
            },
            "upper_band": {
                "label": "Upper Band",
                "help": "Band above which price is considered overbought",
            },
        }

    def evaluate(self, data) -> StrategySignal:
        """
        This function is call every time a new data point is available.
        It updates the RSI indicator and checks if the RSI crosses
        the defined bands to generate BUY or SELL signals.
        """
        if "time" not in data or "open" not in data or "close" not in data:
            return StrategySignal()
        position = Position.STAY
        # Update the RSI indicator
        self.rsi.update(open_price=data["open"], close_price=data["close"])
        # Make the decision what position to advice
        if self.last_flip == Position.SELL and self.rsi[0] < self.lower_band:
            position = Position.BUY
        elif self.last_flip == Position.BUY and self.rsi[0] > self.upper_band:
            position = Position.SELL
        if position != Position.STAY:
            self.last_flip = position
        return StrategySignal(
            time=data["time"],
            price=data["close"],
            position=position,
        )
