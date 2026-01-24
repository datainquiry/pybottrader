import sys

# Check if UI components are available before importing
try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    from pybottrader.ui.candlestick import CandlestickChart, CandleStickSeries

    UI_AVAILABLE = True
except ImportError as e:
    print("UI components not available. Install with: pip install pybottrader[ui]")
    print(f"Import error: {e}")
    UI_AVAILABLE = False
    sys.exit(1)

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
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
