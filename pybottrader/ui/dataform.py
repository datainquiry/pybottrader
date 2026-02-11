from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QCompleter,
    QDateEdit,
)

# from PyQt6.QtCore import QDate, pyqtSignal
from PyQt6.QtCore import QDate
from typing import Dict, Any, Callable
import datetime


class TradingInputForm(QWidget):
    """Reactive form widget for trading inputs"""

    # Signal for value changes
    # values_changed = pyqtSignal(dict)

    TIMEFRAMES = {
        "1 Minute": "1m",
        "5 Minutes": "5m",
        "15 Minutes": "15m",
        "30 Minutes": "30m",
        "1 Hour": "1h",
        "4 Hours": "4h",
        "Daily": "1d",
        "Weekly": "1w",
        "Monthly": "1M",
    }

    EXCHANGES = [
        "YFinance",
        "Binance",
        "Coinbase",
        "Kraken",
        "Bitfinex",
        "NYSE",
        "NASDAQ",
        "CME",
    ]

    COMMON_SYMBOLS = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "META",
        "TSLA",
        "BTC/USD",
        "ETH/USD",
        "BNB/USD",
        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
    ]

    # def __init__(self, on_change: Callable[[Dict[str, Any]], None] = None, parent=None):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self._on_change = on_change
        self.init_ui()

        # Connect the signal to the callback if provided
        # if on_change:
        #     self.values_changed.connect(on_change)

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        # Exchange selection
        self.exchange_input = QComboBox()
        self.exchange_input.addItems(self.EXCHANGES)
        self.exchange_input.currentTextChanged.connect(self._notify_change)
        form_layout.addRow("Exchange", self.exchange_input)

        # Symbol input with autocomplete
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Enter symbol (e.g., AAPL)")
        completer = QCompleter(self.COMMON_SYMBOLS)
        completer.setCaseSensitivity(False)
        self.symbol_input.setCompleter(completer)
        self.symbol_input.textChanged.connect(self._notify_change)
        form_layout.addRow("Symbol", self.symbol_input)

        # Timeframe selection
        self.timeframe_input = QComboBox()
        self.timeframe_input.addItems(self.TIMEFRAMES.keys())
        self.timeframe_input.setCurrentText("Daily")
        self.timeframe_input.currentTextChanged.connect(self._notify_change)
        form_layout.addRow("Timeframe", self.timeframe_input)

        # Start date input
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        default_start = QDate.currentDate().addYears(-1)
        self.start_date.setDate(default_start)
        self.start_date.setMinimumDate(QDate(1970, 1, 1))
        self.start_date.setMaximumDate(QDate.currentDate())
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.dateChanged.connect(self._notify_change)
        form_layout.addRow("Start Date:", self.start_date)

        # End date input
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setMinimumDate(QDate(1970, 1, 1))
        self.end_date.setMaximumDate(QDate.currentDate())
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        self.end_date.dateChanged.connect(self._notify_change)
        form_layout.addRow("End Date:", self.end_date)

        # Connect date validation
        self.start_date.dateChanged.connect(self.validate_dates)
        self.end_date.dateChanged.connect(self.validate_dates)

    def validate_dates(self):
        """Ensures end date is not before start date"""
        if self.start_date.date() > self.end_date.date():
            self.end_date.setDate(self.start_date.date())

    def _notify_change(self, *args):
        """Emits current values when any input changes"""
        self.values_changed.emit(self.get_values())

    def get_values(self) -> Dict[str, Any]:
        """Returns the current form values"""
        return {
            "exchange": self.exchange_input.currentText(),
            "symbol": self.symbol_input.text().strip().upper(),
            "timeframe": self.TIMEFRAMES[self.timeframe_input.currentText()],
            "start_date": self.start_date.date().toPyDate(),
            "end_date": self.end_date.date().toPyDate(),
        }

    def set_values(self, values: Dict[str, Any]):
        """Sets form values from a dictionary"""
        # Temporarily disconnect the change notification to avoid multiple emissions
        old_callback = self._on_change
        self._on_change = None
        (
            self.values_changed.disconnect()
            if self.values_changed.receivers() > 0
            else None
        )

        if "exchange" in values:
            index = self.exchange_input.findText(values["exchange"])
            if index >= 0:
                self.exchange_input.setCurrentIndex(index)

        if "symbol" in values:
            self.symbol_input.setText(values["symbol"])

        if "timeframe" in values:
            for key, value in self.TIMEFRAMES.items():
                if value == values["timeframe"]:
                    self.timeframe_input.setCurrentText(key)
                    break

        if "start_date" in values:
            if isinstance(values["start_date"], str):
                date = QDate.fromString(values["start_date"], "yyyy-MM-dd")
            else:
                date = QDate(values["start_date"])
            self.start_date.setDate(date)

        if "end_date" in values:
            if isinstance(values["end_date"], str):
                date = QDate.fromString(values["end_date"], "yyyy-MM-dd")
            else:
                date = QDate(values["end_date"])
            self.end_date.setDate(date)

        # Reconnect the change notification
        self._on_change = old_callback
        if old_callback:
            self.values_changed.connect(old_callback)
            self._notify_change()
