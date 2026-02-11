# PyBotTrader UI User Guide

This guide covers the user interface components available in PyBotTrader
for building trading applications with Qt6.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [UI Components](#ui-components)
   - [Charts](#charts)
   - [Forms](#forms)
   - [Data Input Forms](#data-input-forms)
4. [Examples](#examples)
5. [Quick Start](#quick-start)

## Overview

PyBotTrader provides a comprehensive set of Qt6-based UI components
specifically designed for trading applications. These components include
interactive charts, form generators for strategy parameters, and data
input forms.

## Installation

Make sure you have Qt6 dependencies installed:

```bash
pip install PyQt6 PyQt6-Charts
```

## UI Components

### Charts

#### LineChart

The `LineChart` component creates interactive line charts for time series data.

```python
from pybottrader.ui.line import LineChart, LineSeries

# Create a line chart
chart = LineChart(title="Price Chart")

# Create and add a line series
series = LineSeries(name="Price")
series.update({"time": 1640995200, "value": 150.0})  # timestamp in seconds
chart.add_series(series)

# Add horizontal lines for levels
chart.add_horizontal_line(30, "Lower Band", color=Qt.GlobalColor.green)
chart.add_horizontal_line(70, "Upper Band", color=Qt.GlobalColor.red)
```

**Features:**

- Interactive pan and zoom
- Rubber band selection
- Multiple series support
- Horizontal reference lines
- Auto-scaling axes

#### CandlestickChart

The `CandlestickChart` component provides OHLC (Open, High, Low, Close)
candlestick charts.

```python
from pybottrader.ui.candlestick import CandlestickChart, CandleStickSeries

# Create candlestick chart
chart = CandlestickChart(title="Price Action")

# Create and add candlestick series
series = CandleStickSeries()
series.update({
    "open": 149.5,
    "high": 152.0,
    "low": 148.0,
    "close": 151.0,
    "time": 1640995200  # timestamp in seconds
})
chart.add_series(series)
```

**Features:**

- Green candles for increasing prices
- Red candles for decreasing prices
- Automatic date formatting on x-axis
- Auto-scaling y-axis

### Forms

#### FormFactory

The `FormFactory` automatically generates form widgets based on a class's `__init__` parameters.

```python
from pybottrader.ui.formfactory import FormFactory
from pybottrader.strategies.simplersi import SimpleRSIStrategy

# Create form from strategy class
form = FormFactory(SimpleRSIStrategy)

# Get current form values
values = form.get_values()
print(values)  # {'period': 14, 'upper_band': 70, 'lower_band': 30}

# Set form values
form.set_values({'period': 20, 'upper_band': 80, 'lower_band': 20})
```

**Supported Input Types:**

- `int` → QSpinBox
- `float` → QDoubleSpinBox  
- `DateStamp` → QDateEdit with calendar popup
- `TickerSymbol` → QLineEdit with symbol autocomplete
- `TimeFrame` → QComboBox with common timeframes
- `str` → QLineEdit

#### StrategyWidget

Specialized form for strategy parameters with signal emission for
real-time updates.

```python
from pybottrader.ui.strategyform import StrategyWidget

# Create strategy form
strategy_form = StrategyWidget(SimpleRSIStrategy)

# Connect to value changes
strategy_form.values_changed.connect(on_strategy_change)
```

#### TraderFormFactory

Combines data streamer and strategy forms into a single widget with an
"Analyze" button.

```python
from pybottrader.ui.formfactory import TraderFormFactory
from pybottrader.strategies.simplersi import SimpleRSIStrategy
from pybottrader.datastreamers.yfinance import YFHistory

# Create combined form
form = TraderFormFactory(SimpleRSIStrategy, YFHistory)

# Connect to changes
form.values_changed.connect(on_form_change)
```

### Data Input Forms

#### TradingInputForm

Pre-built form for common trading data inputs including exchange, symbol, timeframe, and date range.

```python
from pybottrader.ui.dataform import TradingInputForm

# Create data input form
data_form = TradingInputForm()

# Get values
values = data_form.get_values()
# Returns:
# {
#     'exchange': 'YFinance',
#     'symbol': 'AAPL',
#     'timeframe': '1d',
#     'start_date': datetime.date(2023, 1, 1),
#     'end_date': datetime.date(2024, 1, 1)
# }
```

**Available Exchanges:**

- YFinance
- Binance
- Coinbase
- Kraken
- Bitfinex
- NYSE
- NASDAQ
- CME

**Available Timeframes:**

- 1 Minute, 5 Minutes, 15 Minutes, 30 Minutes
- 1 Hour, 4 Hours
- Daily, Weekly, Monthly

**Common Symbols:**

- Stocks: AAPL, MSFT, GOOGL, AMZN, META, TSLA
- Crypto: BTC/USD, ETH/USD, BNB/USD
- Forex: EUR/USD, GBP/USD, USD/JPY

## Examples

### Basic Trading Terminal

Create a complete trading terminal with forms and charts:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from pybottrader.strategies.simplersi import SimpleRSIStrategy
from pybottrader.datastreamers.yfinance import YFHistory
from pybottrader.ui.line import LineChart
from pybottrader.ui.formfactory import TraderFormFactory
from pybottrader.portfolios import DummyPortfolio
from pybottrader.traders import Trader

class TradingTerminal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyBotTrader Terminal")
        self.setMinimumWidth(1200)
        
        # Create main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Create form and chart
        self.form = TraderFormFactory(SimpleRSIStrategy, YFHistory)
        self.form.values_changed.connect(self.update_chart)
        
        self.chart = LineChart(title="RSI Strategy")
        
        # Add to layout
        layout.addWidget(self.form)
        layout.addWidget(self.chart)
    
    def update_chart(self, data):
        """Update chart with new strategy results"""
        params = self.form.get_values()
        
        # Create trader with form parameters
        streamer = YFHistory(**params["data"])
        strategy = SimpleRSIStrategy(**params["strategy"])
        portfolio = DummyPortfolio()
        trader = Trader(strategy, portfolio, streamer)
        
        # Create RSI line series
        rsi_series = LineSeries(name="RSI")
        while trader.next():
            status = trader.status()
            rsi_series.update({
                "time": status.signal.time,
                "value": strategy.rsi[0]
            })
        
        # Add series and bands to chart
        self.chart.add_series(rsi_series)
        self.chart.add_horizontal_line(30, "Lower Band")
        self.chart.add_horizontal_line(70, "Upper Band")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TradingTerminal()
    window.show()
    sys.exit(app.exec())
```

### Candlestick Chart Example
Display OHLC data in a candlestick chart:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pybottrader.ui.candlestick import CandlestickChart, CandleStickSeries
from pybottrader.datastreamers import CSVFileStreamer

class ChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Price Chart")
        self.setGeometry(100, 100, 800, 600)
        
        # Create widget and layout
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Create candlestick chart
        chart = CandlestickChart(title="Stock Price")
        series = CandleStickSeries()
        
        # Load data from CSV
        data_streamer = CSVFileStreamer("data/IBM.csv")
        while True:
            candle = data_streamer.next()
            if candle is None:
                break
            series.update(candle)
        
        chart.add_series(series)
        layout.addWidget(chart)
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChartWindow()
    window.show()
    sys.exit(app.exec())
```

## Quick Start

### 1. Import Required Components
```python
from PyQt6.QtWidgets import QApplication
from pybottrader.ui.formfactory import TraderFormFactory
from pybottrader.ui.line import LineChart
from pybottrader.strategies.simplersi import SimpleRSIStrategy
from pybottrader.datastreamers.yfinance import YFHistory
```

### 2. Create UI Components
```python
# Create form for user input
form = TraderFormFactory(SimpleRSIStrategy, YFHistory)

# Create chart for visualization
chart = LineChart(title="Trading Analysis")
```

### 3. Connect Signals
```python
def on_form_change(values):
    # Handle form data changes
    update_chart(values)

form.values_changed.connect(on_form_change)
```

### 4. Run Application
```python
app = QApplication(sys.argv)
# Add components to main window
window.show()
sys.exit(app.exec())
```

## Tips and Best Practices

### Signal Handling
- Use signals for real-time updates when form values change
- Disconnect signals during programmatic updates to avoid infinite loops
- Always connect signals before setting initial values

### Chart Performance
- For large datasets, consider using data sampling
- Clear and recreate series when updating with completely new data
- Use appropriate time ranges for your analysis timeframe

### Form Validation
- Leverage built-in Qt validators for input constraints
- Use custom validators for trading-specific requirements
- Provide helpful tooltips and placeholder text

### Layout Management
- Use appropriate Qt layouts (QHBoxLayout, QVBoxLayout, QFormLayout)
- Set minimum sizes for charts to ensure usability
- Consider responsive design for different screen sizes

## Customization

### Custom Colors
```python
# Use Qt6 GlobalColor constants
chart.add_horizontal_line(30, "Support", Qt.GlobalColor.green)
chart.add_horizontal_line(70, "Resistance", Qt.GlobalColor.red)
```

### Custom Styling
```python
# Apply Qt stylesheets
chart.setStyleSheet("""
    QChart {
        background-color: #2b2b2b;
        color: #ffffff;
    }
""")
```

### Custom Input Types
Extend FormFactory to support additional parameter types:

```python
def _create_widget_for_type(self, type_hint, default):
    if type_hint == MyCustomType:
        widget = MyCustomWidget()
        # Configure widget
        return widget
    # Call parent method for other types
    return super()._create_widget_for_type(type_hint, default)
```

## Troubleshooting

### Common Issues

**Import Errors:**
- Ensure PyQt6 and PyQt6-Charts are installed
- Check Python path includes the packages

**Chart Not Displaying:**
- Verify data format matches expected structure
- Check timestamps are in seconds (not milliseconds)
- Ensure series is added to chart before adding data

**Form Not Updating:**
- Verify signal connections are properly established
- Check that target class has proper type hints
- Ensure default values are provided for optional parameters

### Debug Mode
Enable Qt debugging:
```python
import os
os.environ['QT_DEBUG_PLUGINS'] = '1'
```

This will provide detailed output when loading Qt components.
