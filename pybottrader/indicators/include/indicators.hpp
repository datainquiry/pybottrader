/**
 * Library of indicators
 *
 */

#pragma once
#include <cmath>
#include <memory>
#include <vector>
#include <optional>
#include <stdexcept>

namespace indicators {

template <typename T>
class Indicator {
protected:
  std::vector<T> mem_data;
  int mem_pos;
  int mem_size;

public:
  Indicator(int mem_size = 1)
      : mem_data(mem_size), mem_pos(0), mem_size(mem_size) {}

  virtual ~Indicator() = default;

  T operator[](int key) const {
    if (key > 0 || -key >= mem_size) {
        throw std::out_of_range("Invalid index");
    }
    int real_pos = (mem_pos + mem_size + key) % mem_size;
    return mem_data[real_pos];
  }

  void push(T value) {
    mem_pos = (mem_pos + 1) % mem_size;
    mem_data[mem_pos] = value;
  }

  T get(int key = 0) const { return (*this)[key]; }
};

class MA : public Indicator<double> {
private:
  int period;
  std::vector<double> prevs;
  int length;
  int pos;
  double accum;

public:
  MA(int period, int mem_size = 1)
      : Indicator(mem_size), period(period), prevs(period, 0.0), length(0), pos(0),
        accum(0.0) {}

  double update(double value) {
    if (length < period) {
      length++;
    } else {
      accum -= prevs[pos];
    }
    prevs[pos] = value;
    accum += value;
    pos = (pos + 1) % period;

    if (length < period) {
      push(std::nan(""));
    } else {
      push(accum / period);
    }
    return (*this)[0];
  }
};

class EMA : public Indicator<double> {
private:
  int period;
  double alpha;
  double smooth_factor;
  int length;
  double prev;

public:
  EMA(int period, double alpha = 2.0, int mem_size=1)
      : Indicator(mem_size), period(period), alpha(alpha),
        smooth_factor(alpha / (1.0 + period)), length(0), prev(0.0) {}

  double update(double value) {
    length++;
    if (length < period) {
      prev += value;
    } else if (length == period) {
      prev += value;
      prev /= period;
    } else {
      prev = (value * smooth_factor) + prev * (1.0 - smooth_factor);
    }

    if (length < period) {
      push(std::nan(""));
    } else {
      push(prev);
    }
    return (*this)[0];
  }
};

class RSI : public Indicator<double> {
private:  
    std::unique_ptr<MA> gains;
    std::unique_ptr<MA> losses;

public:
    RSI(int period = 14, int mem_size = 1)
        : Indicator(mem_size), gains(std::make_unique<MA>(period)), losses(std::make_unique<MA>(period)){}
    double update(double open_price, double close_price) {
        double diff = close_price - open_price;
        gains->update(diff >= 0.0 ? diff : 0.0);
        losses->update(diff < 0 ? -diff : 0.0);
        if (std::isnan(losses->get(0))) {
            push(std::nan(""));         
        } else {
            double rsi = 100.0 - 100.0 / (1.0 + gains->get(0) / losses->get(0));
            push(rsi);
        }
        return (*this)[0];
    }
};

inline double calculate_roi(double initial_value, double final_value) {
  if (initial_value == 0 || std::isnan(initial_value)) {
    return std::nan("");
  }
  return final_value / initial_value - 1.0;
}

class ROI : public Indicator<double> {
private:
  double prev;

public:
  ROI(int mem_size = 1) : Indicator(mem_size), prev(std::nan("")) {}

  double update(double value) {
    double curr = calculate_roi(prev, value);
    push(curr);
    prev = value;
    return (*this)[0];
  }
};

struct MACDResult {
  double macd;
  double signal;
  double hist;
};

class MACD : public Indicator<MACDResult> {
private:
  std::unique_ptr<EMA> short_ema;
  std::unique_ptr<EMA> long_ema;
  std::unique_ptr<EMA> diff_ema;
  int start;
  int counter;

public:
  MACD(int short_period, int long_period, int diff_period, int mem_size = 1)
      : Indicator(mem_size), short_ema(std::make_unique<EMA>(short_period)),
        long_ema(std::make_unique<EMA>(long_period)),
        diff_ema(std::make_unique<EMA>(diff_period)),
        start(std::max(long_period, short_period)), counter(0) {}

  MACDResult update(double value) {
    counter++;
    short_ema->update(value);
    long_ema->update(value);

    MACDResult result;
    if (counter >= start) {
      double diff = short_ema->get(0) - long_ema->get(0);
      diff_ema->update(diff);
      result = {diff, diff_ema->get(0), diff - diff_ema->get(0)};
    } else {
      result = {std::nan(""), std::nan(""), std::nan("")};
    }
    push(result);
    return (*this)[0];
  }
};

class ATR : public Indicator<double> {
private:
  MA prevs;

public:
  ATR(int period, int mem_size = 1) : Indicator(mem_size), prevs(period) {}

  double update(double low_price, double high_price, double close_price) {
    double tr = std::max(std::max(high_price - low_price, high_price - close_price),
                    (low_price - close_price));
    prevs.update(tr);
    push(prevs[0]);
    return (*this)[0];
  }
};

} // namespace indicators
