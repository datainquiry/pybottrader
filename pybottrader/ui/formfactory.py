from typing import Any, Dict, Type
import inspect
from PyQt5.QtWidgets import (
    QWidget,
#     QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QDateEdit,
    QCompleter,
    QComboBox,
)
from PyQt5.QtCore import pyqtSignal, Qt, QDate
from ..types import DateStamp, TickerSymbol, TimeFrame

COMMON_SYMBOLS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA',
    'BTC/USD', 'ETH/USD', 'BNB/USD',
    'EUR/USD', 'GBP/USD', 'USD/JPY'
]

TIMEFRAMES = {
    '1 Minute': '1m',
    '5 Minutes': '5m',
    '15 Minutes': '15m',
    '30 Minutes': '30m',
    '1 Hour': '1h',
    '4 Hours': '4h',
    'Daily': '1d',
    'Weekly': '1w',
    'Monthly': '1M'
}
 
class FormFactory(QWidget):
    """Generic widget for Strategy"""

    # values_changed = pyqtSignal(dict)
    target_class: Type
    param_widgets: dict
    values_changed = pyqtSignal(dict)

    def __init__(self, target_class: Type):
        """
        Creates a form to capture parameters for target_class.__init__

        Args:
            target_class: The class whose __init__ parameters we want to capture
        """
        super().__init__()
        self.target_class = target_class
        self.param_widgets = {}
        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)
        parameters = inspect.signature(target_class.__init__).parameters
        self._param_iter(parameters)

    def _param_iter(self, parameters):
        """Parameter iterations to create widgets"""
        param_labels = self.target_class.labels()
        for name, param in parameters.items():
            if name == "self":
                continue
            default = (
                param.default if param.default != inspect.Parameter.empty else None
            )
            annotation = (
                param.annotation
                if param.annotation != inspect.Parameter.empty
                else type(default) if default is not None else str
            )
            widget = self._create_widget_for_type(annotation, default)
            self.param_widgets[name] = widget
            self._connect_widget_signal(widget)
            label_text = param_labels.get(name, {})
            label = name.replace("_", " ").title() if "label" not in label_text else QLabel(label_text["label"])
            # label = QLabel(label_text)
            if name in param_labels:
                help_text = param_labels[name]
                if isinstance(help_text, dict):
                    label.setToolTip(help_text.get("help", ""))
                    label_text = help_text.get("label", label_text)
                    label.setText(label_text)
            self.form_layout.addRow(label, widget)

    def _create_widget_for_type(self, type_hint: Type, default: Any) -> QWidget:
        """Creates appropriate widget based on parameter type"""
        if type_hint == int:
            widget = QSpinBox()
            widget.setRange(-999999, 999999)
            if default is not None:
                widget.setValue(default)
        elif type_hint == float:
            widget = QDoubleSpinBox()
            widget.setRange(-999999.99, 999999.99)
            widget.setDecimals(4)
            if default is not None:
                widget.setValue(default)
        elif type_hint == DateStamp:
            widget = QDateEdit()
            widget.setCalendarPopup(True)
            widget.setDisplayFormat("yyyy-MM-dd")
            widget.setDate(QDate.currentDate())
#             default_start = QDate.currentDate().addYears(-1)
#             self.start_date.setDate(default_start)
#             self.start_date.setMinimumDate(QDate(1970, 1, 1))
#             self.start_date.setMaximumDate(QDate.currentDate())
#             self.start_date.dateChanged.connect(self._notify_change)
#             form_layout.addRow("Start Date:", self.start_date)
        elif type_hint == TickerSymbol:
            widget = QLineEdit()
            widget.setPlaceholderText("Enter symbol (e.g., AAPL)")
            # widget.setInputMask("A" * 255)
            completer = QCompleter(COMMON_SYMBOLS)
            completer.setCaseSensitivity(False)
            widget.setCompleter(completer)
            # self.symbol_input.textChanged.connect(self._notify_change)
            # form_layout.addRow("Symbol", self.symbol_input)
        elif type_hint == TimeFrame:
            widget = QComboBox()
            for key, value in TIMEFRAMES.items():
                widget.addItem(key, value)
            widget.setCurrentText('Daily')
            # widget.currentTextChanged.connect(self._notify_change)
            # form_layout.addRow("Timeframe", self.timeframe_input)
        else:
            widget = QLineEdit()
            if default is not None:
                widget.setText(str(default))
        return widget

    def _connect_widget_signal(self, widget):
        """Connects appropriate change signal based on widget type"""
        if isinstance(widget, QLineEdit):
            widget.textChanged.connect(self._notify_change)
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            widget.valueChanged.connect(self._notify_change)
        elif isinstance(widget, QDateEdit):
            widget.dateChanged.connect(self._notify_change)
        elif isinstance(widget, QComboBox):
            widget.currentTextChanged.connect(self._notify_change)

    def _notify_change(self, *args):
        """Emits current values when any input changes"""
        self.values_changed.emit(self.get_values())

    def get_values(self) -> Dict[str, Any]:
        """Returns the current form values"""
        params = {}
        for name, widget in self.param_widgets.items():
            if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                params[name] = widget.value()
            elif isinstance(widget, QDateEdit):
                params[name] = widget.date().toString("yyyy-MM-dd")
            elif isinstance(widget, QComboBox):
                selected_index = widget.currentIndex()
                params[name] = widget.itemData(selected_index)
            else:
                params[name] = widget.text()
        return params

    def set_values(self, values: Dict[str, Any]):
        """Sets form values from a dictionary"""
        # Temporarily disconnect signals to avoid multiple emissions
        receivers = []
        if self.values_changed.receivers() > 0:
            receivers = list(self.values_changed.receivers())
            for receiver in receivers:
                self.values_changed.disconnect(receiver[1])

        for name, value in values.items():
            if name in self.param_widgets:
                widget = self.param_widgets[name]
                if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                    widget.setValue(value)
                else:
                    widget.setText(str(value))
        # Reconnect signals and emit change
        for receiver in receivers:
            self.values_changed.connect(receiver[1])
        self._notify_change()
