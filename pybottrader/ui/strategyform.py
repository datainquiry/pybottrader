"""
Strategy Form widget

This module contains a class that generates a Qt Widget based on the init
parameters of a strategy.
"""

# from typing import Any, Dict, Type, Callable
from typing import Any, Dict, Type
import inspect
from PyQt6.QtWidgets import (
    QWidget,
    #     QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
)

# from PyQt6.QtCore import pyqtSignal
from ..strategies import Strategy


class StrategyWidget(QWidget):
    """Generic widget for Strategy"""

    # values_changed = pyqtSignal(dict)
    target_class: Strategy
    param_widgets: dict

    # def __init__(self, target_class: Type, on_change: Callable[[Dict[str, Any]], None] = None):
    def __init__(self, target_class: Strategy):
        """
        Creates a form to capture parameters for target_class.__init__

        Args:
            target_class: The class whose __init__ parameters we want to capture
            on_change: Function to call when parameters change
        """
        super().__init__()
        self.target_class = target_class
        self.param_widgets = {}

        # Connect the signal to the callback if provided
        # if on_change:
        #     self.values_changed.connect(on_change)

        form_layout = QFormLayout()
        self.setLayout(form_layout)

        param_labels = target_class.labels()
        # signature = inspect.signature(target_class.__init__)
        # parameters = signature.parameters
        parameters = inspect.signature(target_class.__init__).parameters

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

            # Connect widget's value change signal
            self._connect_widget_signal(widget)

            label_text = param_labels.get(name, name.replace("_", " ").title())
            label = QLabel(label_text["label"])
            if name in param_labels:
                help_text = param_labels[name]
                if isinstance(help_text, dict):
                    label.setToolTip(help_text.get("help", ""))
                    label_text = help_text.get("label", label_text)
                    label.setText(label_text)
            form_layout.addRow(label, widget)

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

    def _notify_change(self, *args):
        """Emits current values when any input changes"""
        self.values_changed.emit(self.get_values())

    def get_values(self) -> Dict[str, Any]:
        """Returns the current form values"""
        params = {}
        for name, widget in self.param_widgets.items():
            if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                params[name] = widget.value()
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
