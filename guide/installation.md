# PyBotTrader Installation Guide

## Standard Installation

For core trading functionality without UI components:

```bash
pip install pybottrader
```

This installs:
- Core trading engine
- Indicators (MA, RSI, MACD, etc.)
- Data streamers (YFinance, Coinbase, CSV)
- Portfolio management
- Strategy framework

## Installation with UI Support

For GUI features including charts and forms:

```bash
pip install pybottrader[ui]
```

This includes everything from the standard installation plus:
- Qt6-based chart components
- Interactive form builders
- Data input widgets
- Trading terminal examples

## UI Components Only

If you already have PyBotTrader installed and want to add UI support:

```bash
pip install pybottrader[ui] --no-deps pybottrader
pip install PyQt6 PyQt6-Charts
```

Or manually:

```bash
pip install PyQt6 PyQt6-Charts
```

## Usage

### Without UI (Core functionality)
```python
import pybottrader
from pybottrader.strategies.simplersi import SimpleRSI
from pybottrader.datastreamers.yfinance import YFHistory

# Core trading functionality available
strategy = SimpleRSI(lower_band=30, upper_band=70)
streamer = YFHistory(symbol="AAPL", timeframe="1d")
```

### With UI (Optional components)
```python
import pybottrader

# Check if UI is available
if pybottrader.has_ui_support():
    from pybottrader.ui import LineChart, FormFactory
    
    # UI components available
    chart = LineChart()
    form = FormFactory(MyStrategy)
else:
    print("UI not available. Install with: pip install pybottrader[ui]")
    
# Or use explicit import with helpful error message
ui = pybottrader.import_ui()
chart = ui.LineChart()
```

## Error Handling

When UI components are not available, attempting to import or use them will result in a helpful error message:

```
UI components are not available. To use PyBotTrader UI features, install with:
    pip install pybottrader[ui]
```

## Examples

### Check UI Support
```python
import pybottrader

if pybottrader.has_ui_support():
    print("UI components available")
else:
    print("UI components not available")
```

### Graceful Fallback
```python
import pybottrader

try:
    ui = pybottrader.import_ui()
    chart = ui.LineChart()
    # Use UI components
except ImportError:
    print("Falling back to non-UI mode")
    # Use alternative functionality
```

## Dependencies

### Core Dependencies
- `attrs` - Class attributes
- `numpy` - Numerical computations
- `pandas` - Data manipulation
- `requests` - HTTP requests
- `yfinance` - Yahoo Finance data
- `coinbase-advanced-py` - Coinbase API
- `pybind11` - C++ bindings
- `twine` - Package publishing

### Optional UI Dependencies
- `PyQt6` - Qt6 widgets framework
- `PyQt6-Charts` - Qt6 charting components

## Development Installation

For development with UI support:

```bash
git clone https://github.com/jailop/pybottrader.git
cd pybottrader
pip install -e ".[ui]"
```

For development without UI:

```bash
pip install -e "."
```

## Testing UI Installation

You can test if UI components are working:

```python
import pybottrader

# Test availability
print("UI available:", pybottrader.has_ui_support())

# Test actual functionality (only works if Qt6 is installed)
if pybottrader.has_ui_support():
    from pybottrader.ui import LineChart
    print("LineChart import successful")
```