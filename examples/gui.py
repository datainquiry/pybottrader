import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pybottrader.ui.candlestick import CandlestickChart, CandleStickSeries
from pybottrader.datastreamers import CSVFileStreamer


class DataChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        widget = CandlestickChart(self)
        series = CandleStickSeries()
        data = CSVFileStreamer("data/IBM.csv")
        while True:
            item = data.next()
            if item is None:
                break
            series.update(item)
        widget.add_series(series)
        layout.addWidget(widget)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor")
        self.setGeometry(100, 100, 800, 600)
        widget = DataChart(self)
        self.setCentralWidget(widget)


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
