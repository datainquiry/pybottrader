# Indicators

Indicators are aggregate measurements of financial data which intend is to
reveal patterns and provide insights for decision making. In PyBotTrader,
indicators are the most basic building block to implement trading algorithms.

There exist many libraries to compute indicators, like `ta-lib`, however
PyBotTrader provides its own implementations designed for streaming data.
Instead of making calculations from scratch at every moment, indicators in
PyBotTrader keep memory of the previous results and get just updated when new
data arrives. This is a more efficient approach for timed data.

All the available indicators in PyBotTrader share the same interface. Once they
have been initialized, you can call the ``update`` method to compute new data.
For example, one of the more basic indicators is the simple moving average,
designated as ``MA`` in PyBotTrader. This represents the average of the `n` most
recent data points.

```python
from pybottrader.indicators import MA

ma = MA(period=3)
ma.update(1)
ma.update(2)
ma.update(3)

print(ma[0])  # Output is 2

ma.update(4)

print(ma[0])  # Output is 3
```

In the previous code examples, a moving average instance is created to represent
the average of the last three data points. To access the value of the moving
average, array notation is used. A zero index correspond to the current moment:
`ma[0]`.

By default, indicators in PyBotTrader only keep memory of the most recent value.
In the previous example, when a new data point is captured, the indicator value
is recomputed and the previous value is forgoten. However, you are able to
modify this behavior by defining how many values to be remembered assinging a
value to the argmument `mem_size` when an indicator is created.

```python
from pybottrader.indicators import MA

ma = MA(period=3, mem_size=2)
ma.update(1)
ma.update(2)
ma.update(3)
ma.update(4)
ma.update(5)

print(ma[0])   # Output is 4
print(ma[-1])  # Output is 3
print(ma[-2])  # Error, invalid index
```

In the previous example, a moving average object its configurated to remind two
values, the current one is ``ma[0]`` and the previous one is ``ma[-1]``. Observe
that to access previous values, negative indeces are used. Because the memory
size is only for two values, trying to access ``ma[-2]`` produces an exception.

Using negative indeces can seem strange for sotware developers, but it is a
natural way to represent past events when the current moment is designed with
the ``0`` index.  Morever, under this logic, positive indices can be used to
represent future events.

Indicators in PyBotTrader are implemented in C++ instead of Python. In that way,
your running code can take advantage of the speed and memory locality in your
system.

At this moment, a limited number of indicators is implemented. In future
versions, more indicators will be included.


