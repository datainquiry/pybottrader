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


def test_RSI():
    rsi = RSI(period=3)
    rsi.update(open_price=1.0, close_price=2.0)
    assert np.isnan(rsi[0])
    rsi.update(open_price=2.0, close_price=4.0)
    assert np.isnan(rsi[0])
    rsi.update(open_price=4.0, close_price=3.0)
    assert abs(rsi[0] - 75.0) < 1e-6


def test_MACD():
    """
    Data for this test was taken from:
    <https://investexcel.net/how-to-calculate-macd-in-excel/>
    """
    macd = MACD(
        short_period=12,
        long_period=26,
        diff_period=9,
        mem_size=2,
    )
    ts = np.array(
        [
            459.99,
            448.85,
            446.06,
            450.81,
            442.8,
            448.97,
            444.57,
            441.4,
            430.47,
            420.05,
            431.14,
            425.66,
            430.58,
            431.72,
            437.87,
            428.43,
            428.35,
            432.5,
            443.66,
            455.72,
            454.49,
            452.08,
            452.73,
            461.91,
            463.58,
            461.14,
            452.08,
            442.66,
            428.91,
            429.79,
            431.99,
            427.72,
            423.2,
            426.21,
            426.98,
            435.69,
            434.33,
            429.8,
            419.85,
            426.24,
            402.8,
            392.05,
            390.53,
            398.67,
            406.13,
            405.46,
            408.38,
            417.2,
            430.12,
            442.78,
            439.29,
            445.52,
            449.98,
            460.71,
            458.66,
            463.84,
            456.77,
            452.97,
            454.74,
            443.86,
            428.85,
            434.58,
            433.26,
            442.93,
            439.66,
            441.3,
        ]
    )
    res = np.array(
        [
            3.03752586873395,
            1.90565222933578,
            1.05870843537763,
            0.410640325343509,
            -0.152012994298479,
            -0.790034731709356,
            -1.33810041258299,
            -2.17197457979186,
            -3.30783450954566,
            -4.59014109868629,
            -5.75668618055047,
            -6.65738137622787,
            -7.33974702300915,
            -7.78618154079804,
            -7.90287193112745,
            -7.58262468963905,
            -6.78603605354027,
            -5.77285851501159,
            -4.5644861655494,
            -3.21555428301682,
            -1.67071586469137,
            -0.112968660984149,
            1.45411118991556,
            2.82877971367526,
            3.94371200786538,
            4.85665087093101,
            5.41047306555065,
            5.45836826902626,
            5.26562556819742,
            4.89909832689482,
            4.58597343224244,
            4.26011131701701,
            3.96060129677866,
        ]
    )
    for i, value in enumerate(ts):
        macd.update(value)
        if i < 33:
            assert np.isnan(macd[0].signal)
        elif i == 33:
            assert abs(macd[0].signal - res[i - 33]) < 1e-3
        else:
            assert abs(macd[0].signal - res[i - 33]) < 1e-3
            assert abs(macd[-1].signal - res[i - 34]) < 1e-3
