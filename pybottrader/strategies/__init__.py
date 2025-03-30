"""
# Strategies

A strategy model, so the user of this library can implement it owns strategies
(this is the purpose of this library).  A strategy is built to consume a data
stream, compute indicators, and produce BUY/SELL signals.

"""

from .base import Position, StrategySignal, Strategy
from .simplersi import SimpleRSI
from .crossover import CrossOver
