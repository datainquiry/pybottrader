"""Experimental Trading Terminal"""

import sys
from typing import Type
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
)
from pybottrader.strategies.simplersi import SimpleRSIStrategy
from pybottrader.datastreamers.yfinance import YFHistory
from pybottrader.ui.line import LineSeries, LineChart
from pybottrader.ui.formfactory import TraderFormFactory
from pybottrader.portfolios import DummyPortfolio
from pybottrader.traders import Trader

class BaseWindow(QMainWindow):
    """Trader Terminal Window"""
    strategy_class: Type
    data_class: Type
    def __init__(self, strategy_class: Type, data_class: Type):
        super().__init__()
        self.strategy_class = strategy_class
        self.data_class = data_class
        self.setWindowTitle("PyBotTrader")
        self.setMinimumWidth(800)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.trader_form = TraderFormFactory(strategy_class, data_class)
        self.trader_form.values_changed.connect(self.update)
        self.main_layout.addWidget(self.trader_form)
        self.chart = LineChart()
        self.main_layout.addWidget(self.chart)

    def update(self, data: dict):
        """Updates the chart"""
        print("Derived class", data)
        params = self.trader_form.get_values()
        streamer = self.data_class(**params["data"])
        strat = self.strategy_class(**params["strategy"])
        portfolio = DummyPortfolio()
        trader = Trader(strat, portfolio, streamer)
        series = LineSeries(name="Simple RSI")
        while trader.next():
            status = trader.status()
            series.update({"time": status.signal.time, "value": strat.rsi[0]})
        self.chart.add_series(series)
        # self.chart.add_horizontal_line(strat_params["lower_band"], "Lower Band")
        # self.chart.add_horizontal_line(strat_params["upper_band"], "Upper Band")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BaseWindow(strategy_class = SimpleRSIStrategy, data_class = YFHistory)
    window.show()
    sys.exit(app.exec_())
