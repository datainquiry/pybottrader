Indicators
==========

Indicators are aggregate measurements of financial data which intend is to
reveal patterns and provide insights for decision making. In PyBotTrader,
indicators are the most basic building block to implement trading algorithms.

There exist many libraries to compute indicators, like `ta-lib`, however
PyBotTrader provides its own implementations because they are designed for
streaming data. Instead of making calculations from scratch at every moment,
indicators in PyBotTrader keep memory of the previous result and just get updated
when new data is captured. This is a more efficient approach for timed data, and
the same time makes easier to use them.

All the available indicators in PyBotTrader share the same interface. Once they
have been initialized, you can call the ``update`` method to include more data. For example,
one of the more basic indicators is the simple moving average, designated as
``MA`` in PyBotTrader. This represents the average of the `n` most recent data
points.

.. code-block::

    from pybottrader.indicators import MA

    ma = MA(period=3)
    ma.update(1)
    ma.update(2)
    ma.update(3)

    print(ma[0])  # Output is 2

    ma.update(4)
    
    print(ma[0])  # Output is 3


In the previous code section, a moving average object is created to represent
the average of the last three data points. To access the value of the moving
average an array notation is used. A zero index correspond to the current
moment: ``ma[0]``.

By default, indicators in PyBotTrader only keep memory of the most recent value. In
the previous example, when a new data point is captured, the indicator value is
recomputed and the previous value is forgoten. However, you are able to modify this
behavior defining how many values to be remembered including the argmument
``mem_size`` when an indicator is created.

.. code-block::

    from pybottrader.indicators import MA

    ma = MA(period=3, mem_size=2)
    ma.update(1)
    ma.update(2)
    ma.update(3)
    ma.update(4)
    ma.update(5)
    
    print(ma[0])   # Output is 4
    print(ma[-1])  # Output is 3
    print(ma[-2])  # Output is NaN

In the previous example, a moving average object its configurated to remind two
values, the current one is ``ma[0]`` and the previous one is ``ma[-1]``. Observe that to access
previous values negative indexes are used. Because the memory size is only for
two values, trying to access ``ma[-2]`` returns a ``NaN`` value. Using negative
indeces can seem strange for sotware developers, but it is a natural way to
represent past events when the current moment is designed with the ``0`` index.
Under this logic, positive indices can be used for future events.
