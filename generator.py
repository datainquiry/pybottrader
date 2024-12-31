from typing import Dict, Any, Type, Callable
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from pybottrader.strategies.simplersi import SimpleRSIStrategy
from pybottrader.datastreamers.yfinance import YFHistory
from pybottrader.ui.line import LineSeries, LineChart
from pybottrader.ui.formfactory import FormFactory
from pybottrader.portfolios import DummyPortfolio
from pybottrader.traders import Trader

class BaseWindow(QMainWindow):
    datawidget: FormFactory
    stratwidget: FormFactory
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
        container_widget = QWidget()
        container_widget.setMaximumWidth = 250
        self.layout = QVBoxLayout()
        container_widget.setLayout(self.layout)
        self.main_layout.addWidget(container_widget)
        self.datawidget = FormFactory(data_class)
        self.layout.addWidget(self.datawidget)
        self.stratwidget = FormFactory(strategy_class)
        self.layout.addWidget(self.stratwidget)
        self.button = QPushButton("Analyze")
        self.layout.addWidget(self.button)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)
        self.chart = LineChart()
        self.main_layout.addWidget(self.chart)

class MainWindow(BaseWindow):
    def __init__(self, strategy_class: Type, data_class: Type):
        super().__init__(strategy_class=strategy_class, data_class=data_class)
        self.button.clicked.connect(self.update)

    def upadte(self, data: dict):
        print("Derived class", data)
        streamer = self.data_class(**self.datawidget.get_values())
        strat_params = self.stratwidget.get_values()
        strat = self.strategy_class(**strat_params)
        portfolio = DummyPortfolio()
        trader = Trader(strat, portfolio, streamer)
        series = LineSeries()         
        while trader.next():
            status = trader.status()
            series.update({"time": status.signal.time, "value": strat.rsi[0]})            
        self.chart.add_series(series)
        # self.chart.add_horizontal_line(strat_params["lower_band"], "Lower Band")
        # self.chart.add_horizontal_line(strat_params["upper_band"], "Upper Band")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(strategy_class = SimpleRSIStrategy, data_class = YFHistory)
    window.show()
    sys.exit(app.exec_())
