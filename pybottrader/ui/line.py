from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPointF


class LineSeries(QLineSeries):
    def __init__(self, name="Price"):
        super().__init__()
        self.setName(name)

    def update(self, data):
        """Updates the line series with new data point"""
        self.append(data["time"] * 1000, data["value"])


class HorizontalLine(QLineSeries):
    def __init__(
        self, value: float, name: str = "Level", color: Qt.GlobalColor = Qt.red
    ):
        super().__init__()
        self.setName(name)
        self.value = value
        pen = QPen(color)
        pen.setStyle(Qt.DashLine)
        self.setPen(pen)

    def update_bounds(self, min_x: float, max_x: float):
        """Updates the horizontal line to span the current view"""
        self.clear()
        self.append(min_x, self.value)
        self.append(max_x, self.value)


class LineChart(QWidget):
    def __init__(self, parent=None, title: str = ""):
        super().__init__(parent)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        # Create layout
        layout = QVBoxLayout(self)

        # Create chart
        self.chart = QChart()
        self.chart.setTitle(title)

        # Create chart view
        chart_view = QChartView(self.chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setRubberBand(QChartView.RectangleRubberBand)
        chart_view.setDragMode(QChartView.ScrollHandDrag)

        # Add chart view to layout
        layout.addWidget(chart_view)
        self.setLayout(layout)

        # Store horizontal lines for updating
        self.horizontal_lines = []

        # Store main series
        self.main_series = None

        # Create axes
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.axis_y.setRange(0.0, 100.0)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

    def add_series(self, series: QLineSeries):
        """Adds a line series to the chart"""
        self.chart.addSeries(series)
        series.attachAxis(self.axis_x)
        series.attachAxis(self.axis_y)

        if isinstance(series, HorizontalLine):
            self.horizontal_lines.append(series)
        else:
            self.main_series = series

        self.chart.legend().setVisible(True)

    def add_horizontal_line(
        self, value: float, name: str = "Level", color: Qt.GlobalColor = Qt.red
    ):
        """Helper method to add a horizontal line"""
        h_line = HorizontalLine(value, name, color)
        self.add_series(h_line)
        return h_line

    def update_horizontal_lines(self):
        """Updates horizontal lines to span the current view"""
        if self.main_series and self.main_series.count() > 0:
            points = [self.main_series.at(i) for i in range(self.main_series.count())]
            if points:
                min_x = min(point.x() for point in points)
                max_x = max(point.x() for point in points)
                for line in self.horizontal_lines:
                    line.update_bounds(min_x, max_x)
