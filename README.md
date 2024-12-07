# PyBotTrader

An experimental Python library to implement trading bots.

## Indicators

### **Components**

#### **Base Class: `Indicator`**
The `Indicator` class provides a generic structure to maintain a circular buffer of recent values, with the following features:
- **Memory Buffer (`mem_data`)**: Stores the last `mem_size` values in a circular fashion.
- **Indexing**: Supports time-series indexing where `0` refers to the most recent value, and negative indices go further back in time.
- **Value Management**:
  - `push(value)`: Adds a new value to the buffer as the latest entry.
  - `__getitem__(key)`: Accesses a value by index, returning `NaN` for out-of-bounds indices.
  - `get(key)`: Retrieves a value similar to `__getitem__`.

---

#### **Derived Classes**

1. **`MA` (Moving Average)**
   - Computes a Simple Moving Average (SMA) over a specified period (`period`).
   - Maintains an internal buffer (`prevs`) to track the last `period` values.
   - **Method**:
     - `update(value)`: Adds a new value, recalculates the SMA, and pushes the result into the buffer.

2. **`EMA` (Exponential Moving Average)**
   - Calculates an EMA with smoothing controlled by `alpha` or a computed factor based on the `periods` parameter.
   - The EMA gives more weight to recent data for responsiveness to changes.
   - **Method**:
     - `update(value)`: Updates the EMA calculation with a new value and stores the result in the buffer.

3. **`ROI` (Return on Investment)**
   - Measures the return on investment (ROI) as a percentage change between two consecutive values.
   - Requires at least one previous value to compute ROI.
   - **Method**:
     - `update(value)`: Computes the ROI from the previous value to the current value and updates the buffer.

---

#### **Helper Function: `roi(initial_value, final_value)`**
- Computes the return on investment using the formula:
  \[
  \text{ROI} = \frac{\text{final value}}{\text{initial value}} - 1.0
  \]
- Returns `NaN` if the initial value is zero or undefined.

---

### **Key Features**
- **Efficient Memory Management**: Uses a ring buffer to limit memory usage while retaining recent values.
- **Flexibility**: Designed for streaming time-series data, allowing on-the-fly updates.
- **Extensibility**: The base class `Indicator` can be extended to implement new indicators.
- **Error Handling**: Provides `NaN` for invalid indices or calculations, ensuring robustness.

---

### **Usage Example**
```python
# Initialize a Moving Average with a buffer size of 10 and a period of 3
ma = MA(period=3, mem_size=10)

# Update with new values
print(ma.update(10))  # Output: NaN (not enough data points yet)
print(ma.update(12))  # Output: NaN
print(ma.update(14))  # Output: 12.0 (average of 10, 12, 14)
print(ma[0])          # Output: 12.0 (most recent value)
```

This modular design is ideal for financial applications, where efficient and dynamic calculations of indicators are essential.
