from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtCharts import QChart, QChartView, QCandlestickSeries, QCandlestickSet
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt


class CandleStickSeries(QCandlestickSeries):
    def __init__(self):
        super().__init__()
        self.setName("Price")
        self.setIncreasingColor(Qt.GlobalColor.green)
        self.setDecreasingColor(Qt.GlobalColor.red)

    def update(self, data):
        candlestick_set = QCandlestickSet(
            data["open"],
            data["high"],
            data["low"],
            data["close"],
            data["time"] * 1000,
        )
        self.append(candlestick_set)


class CandlestickChart(QWidget):
    def __init__(self, parent=None, title: str = ""):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.chart = QChart()
        self.chart.setTitle(title)
        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        chart_view.setRubberBand(QChartView.RubberBand.RectangleRubberBand)
        chart_view.setDragMode(QChartView.DragMode.ScrollHandDrag)
        layout.addWidget(chart_view)
        self.setLayout(layout)

    def add_series(self, series):
        self.chart.addSeries(series)
        self.chart.createDefaultAxes()
        self.chart.legend().setVisible(True)
        axis = series.attachedAxes()
        axis[0].setLabelsAngle(-90)
