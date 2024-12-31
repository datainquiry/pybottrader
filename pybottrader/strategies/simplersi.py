from ..indicators import RSI
from . import Strategy, StrategySignal, Position

class SimpleRSIStrategy(Strategy):
    """A simple strategy based on the RSI indicator"""

    rsi: RSI
    last_flip = Position.SELL
    lower_band: float
    upper_band: float

    def __init__(self, lower_band=30.0, upper_band=70.0):
        self.rsi = RSI()
        self.lower_band = lower_band
        self.upper_band = upper_band

    @staticmethod
    def labels() -> dict:
        return {
            'lower_band': {'label': 'Lower Band', 'help': 'Band below which price is considered underbought'},
            'upper_band': {'label': 'Upper Band', 'help': 'Band above which price is considered overbought'},
        }

    def evaluate(self, data) -> StrategySignal:
        # default positio STAY
        position = Position.STAY
        # Update the RSI indicator
        self.rsi.update(open_price=data["open"], close_price=data["close"])
        # Make the decision what position to advice
        if self.last_flip == Position.SELL and self.rsi[0] < self.lower_band:
            position = Position.BUY
            self.last_flip = Position.BUY
        elif self.last_flip == Position.BUY and self.rsi[0] > self.upper_band:
            position = Position.SELL
            self.last_flip = Position.SELL
        return StrategySignal(time=data["time"], price=data["close"], position=position)


