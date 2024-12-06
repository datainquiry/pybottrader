"""
Moving Average
Implementation adopted from:
https://github.com/jailop/trading/tree/main/indicators-c++
"""

import numpy as np


class MA:
    """Moving Average"""

    period: int
    prevs: np.ndarray
    length: int = 0
    pos: int = 0
    accum: float = 0.0

    def __init__(self, period: int):
        """
        The number of period or window size is required to initialize a MA
        object.
        """
        self.period = period
        self.prevs = np.zeros(period, dtype=float)

    def update(self, value: float) -> float:
        """Aggregate a new value into the moving average"""
        if self.length < self.period:
            self.length += 1
        else:
            self.accum -= self.prevs[self.pos]
        self.prevs[self.pos] = value
        self.accum += value
        self.pos = (self.pos + 1) % self.period
        return self.get()

    def get(self) -> float:
        """Current output of the moving average"""
        if self.length < self.period:
            return np.nan
        return self.accum / self.period

class EMA:
    """Exponential Moving Average"""
    periods: float
    alpha: float
    smooth_factor: float
    length: int = 0
    prev: float = 0.0
    def __init__(self, periods: int, alpha = 2.0):
        self.periods = periods
        self.alpha = alpha
        self.smooth_factor = alpha / (1.0 + periods)
    def update(self, value: float) -> float:
        """Aggregate a new value into the moving average"""
        self.length += 1
        if self.length < self.periods:
            self.prev += value
        elif self.length == self.periods:
            self.prev += value
            self.prev /= self.periods
        else:
            self.prev = (value * self.smooth_factor) + self.prev * (1.0 - self.smooth_factor)
        return self.get()


    def get(self) -> float:
        """Current output of the moving average"""
        if self.length < self.periods:
            return np.nan
        return self.prev

def roi(initial_value, final_value):
    """Return on investment"""
    if initial_value == 0:
        return np.nan
    return final_value / initial_value - 1.0
