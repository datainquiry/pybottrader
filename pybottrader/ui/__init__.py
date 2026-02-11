"""
UI Components Module

This module provides optional Qt6-based UI components for PyBotTrader.
These components are only available when the 'ui' extra dependencies are installed.

Installation with UI support:
    pip install pybottrader[ui]

Without UI support, importing this module will raise an ImportError.
"""

# Try to import Qt6 components, but make them optional
try:
    from .line import LineChart, LineSeries, HorizontalLine
    from .candlestick import CandlestickChart, CandleStickSeries
    from .formfactory import FormFactory, TraderFormFactory
    from .strategyform import StrategyWidget
    from .dataform import TradingInputForm

    __all__ = [
        "LineChart",
        "LineSeries",
        "HorizontalLine",
        "CandlestickChart",
        "CandleStickSeries",
        "FormFactory",
        "TraderFormFactory",
        "StrategyWidget",
        "TradingInputForm",
    ]

except ImportError as e:
    # Create a helpful error message when UI components are not available
    class UIImportError(ImportError):
        def __init__(self):
            message = """
UI components are not available. To use PyBotTrader UI features, install with:

    pip install pybottrader[ui]

This will install the required Qt6 dependencies (PyQt6 and PyQt6-Charts).
"""
            super().__init__(message)

    # Replace all UI classes with error-raising placeholders
    def _ui_not_available(*args, **kwargs):
        raise UIImportError()

    LineChart = _ui_not_available
    LineSeries = _ui_not_available
    HorizontalLine = _ui_not_available
    CandlestickChart = _ui_not_available
    CandleStickSeries = _ui_not_available
    FormFactory = _ui_not_available
    TraderFormFactory = _ui_not_available
    StrategyWidget = _ui_not_available
    TradingInputForm = _ui_not_available

    __all__ = [
        "LineChart",
        "LineSeries",
        "HorizontalLine",
        "CandlestickChart",
        "CandleStickSeries",
        "FormFactory",
        "TraderFormFactory",
        "StrategyWidget",
        "TradingInputForm",
    ]
