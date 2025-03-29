"""
Report signal reversions for a set of strategies
"""

from datetime import datetime
from typing import Optional
from attrs import define
from .datastreamers import DataStreamer
from .strategies import Strategy, StrategySignal


@define
class ScannerIteration:
    time: datetime = datetime.now()
    signals: dict[str, StrategySignal] = {}

class Scanner:
    datastream: DataStreamer
    strategies: list[Strategy]
    last_result: Optional[ScannerIteration] = None

    def __init__(self, strategies: list[Strategy], datastream: DataStreamer):
        self.datastream = datastream
        self.strategies = strategies

    def next(self) -> bool:
        obs = self.datastream.next()
        if obs is None:
            return False
        self.last_result = ScannerIteration()
        if "time" in obs:
            self.last_result.time = obs["time"]
        for strat in self.strategies:
            self.last_result.signals[type(strat).__name__] = strat.evaluate(data=obs)
        return True

    def status(self) -> Optional[ScannerIteration]:
        return self.last_result
