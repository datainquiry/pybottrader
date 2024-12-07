import numpy as np
import pytest
from pybottrader.indicators import *


def test_indicator():
    ind = Indicator(mem_size=5)
    for i in range(5):
        ind.push(i)
    assert abs(ind[0] - 4.0) < 1e-6
    assert abs(ind[-2] - 2.0) < 1e-6
    assert ind[-4] < 1e-6
    assert np.isnan(ind[-5])
    assert np.isnan(ind[-100])
    assert np.isnan(ind[1])
    assert np.isnan(ind[100])


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


def test_ma_memory():
    period = 3
    mem_size = 3
    ma = MA(period=period, mem_size=mem_size)
    ts = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
    for value in ts:
        ma.update(value)
    assert abs(ma[0] - 9.0) < 1e-6
    assert abs(ma[-1] - 8.0) < 1e-6
    assert abs(ma[-2] - 7.0) < 1e-6
    assert np.isnan(ma[-3])


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


def test_ema_memory():
    period = 5
    mem_size = 3
    ema = EMA(period, mem_size=mem_size)
    ts = np.array([10.0, 12.0, 14.0, 13.0, 15.0, 16.0, 18.0])
    res = np.array([12.8, 13.866666, 15.244444])
    for value in ts:
        ema.update(value)
    assert abs(ema[0] - res[2]) < 1e-6
    assert abs(ema[-1] - res[1]) < 1e-6
    assert abs(ema[-2] - res[0]) < 1e-6
    assert np.isnan(ema[-3])


def test_roi():
    assert np.isnan(roi(0, 100))
    assert abs(roi(100, 120) - 0.2) < 1e-6
    assert abs(roi(100, 80) + 0.2) < 1e-6


def test_ROI():
    r = ROI(mem_size=2)
    r.update(10.0)
    assert np.isnan(r[0])
    r.update(12.0)
    assert abs(r[0] - 0.2) < 1e-6
    r.update(15.0)
    assert abs(r[0] - 0.25) < 1e-6
    assert abs(r[-1] - 0.2) < 1e-6
