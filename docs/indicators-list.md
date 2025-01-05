# List of Indicators

## Moving Average

```c++
MA(int period, int mem_size = 1)
```

$$\text{MA}_n = \frac{1}{n}\sum_{i =1}^n x_i$$

$$\text{MA}_{t,n} = \frac{1}{n}\sum_{i =t - n + 1}^t x_i$$

The moving average is used to determine the trend direction of a variable. It is
calculated by adding up data points during a specific period divided by the
number of time periods.

## Moving Variance

```c++
MV(int period, int mem_size = 1)
```

$$\text{MV}_n = \frac{1}{n} \sum_{i=1}^n (x_i - \text{MA}n)^2$$

$$\text{MV}_{t,n} = \frac{1}{n} \sum_{i=t - n + 1}^t (x_i - \text{MA}_{t,n})^2$$

## Exponential Moving Average

```c++
EMA(int period, double alpha = 2.0, int mem_size=1)
```

## Return of Investment

```c++
ROI(int mem_size = 1)
```

## Relative Strength Index

```c++
RSI(int period = 14, int mem_size = 1)
```

## Moving Average Convergence/Divergence

```c++
MACD(int short_period, int long_period, int diff_period, int mem_size = 1)
```

## Average True Range


```c++
ATR(int period, int mem_size = 1)
`
