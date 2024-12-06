import numpy as np
import pytest
from pybottrader.indicators import *


def test_ma():
    """
    This test has been adapted from:
    https://github.com/jailop/trading/tree/main/indicators-c%2B%2B
    """
    period = 3
    ma = MA(period)
    ts = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    for i, value in enumerate(ts):
        y = ma.update(value)
        if i < period - 1:
            assert np.isnan(y)
        else:
            assert y == pytest.approx(ts[i] - 1.0)


def test_ema():
    """
    This test has been adapted from:
    https://github.com/jailop/trading/tree/main/indicators-c%2B%2B
    """
    periods = 5
    ema = EMA(periods)
    ts = np.array([10.0, 12.0, 14.0, 13.0, 15.0, 16.0, 18.0])
    res = np.array([12.8, 13.866666, 15.244444])
    for i, value in enumerate(ts):
        y = ema.update(value)
        if i < periods - 1:
            assert np.isnan(y)
        else:
            assert abs(y - res[i - periods + 1]) < 1e-6


def test_roi():
    assert np.isnan(roi(0, 100))
    assert abs(roi(100, 120) - 0.2) < 1e-6
    assert abs(roi(100, 80) + 0.2) < 1e-6
