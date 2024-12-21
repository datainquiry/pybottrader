// bindings.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "indicators.hpp"

namespace py = pybind11;
using namespace indicators;

PYBIND11_MODULE(_indicators, m) {
    m.doc() = "Financial indicators for streaming data implemented in C++";

    py::class_<Indicator<double>>(m, "IndicatorDouble")
        .def(py::init<int>(), py::arg("mem_size") = 1)
        .def("__getitem__", &Indicator<double>::operator[])
        .def("push", &Indicator<double>::push)
        .def("get", &Indicator<double>::get, py::arg("key") = 0);

    py::class_<Indicator<MACDResult>>(m, "IndicatorMACDResult")
        .def(py::init<int>(), py::arg("mem_size") = 1)
        .def("__getitem__", &Indicator<MACDResult>::operator[])
        .def("push", &Indicator<MACDResult>::push)
        .def("get", &Indicator<MACDResult>::get, py::arg("key") = 0);


    py::class_<MA, Indicator<double>>(m, "MA")
        .def(py::init<int, int>(), py::arg("period"), py::arg("mem_size") = 1)
        .def("update", &MA::update);

    py::class_<EMA, Indicator<double>>(m, "EMA")
        .def(py::init<int, double, int>(), 
             py::arg("period"), py::arg("alpha") = 2.0, py::arg("mem_size") = 1)
        .def("update", &EMA::update);

    py::class_<RSI, Indicator<double>>(m, "RSI")
        .def(py::init<int, int>(), py::arg("period") = 14, py::arg("mem_size") = 1)
        .def("update", &RSI::update,
            py::arg("open_price"),
            py::arg("close_price"));

    py::class_<ROI, Indicator<double>>(m, "ROI")
        .def(py::init<int>(), py::arg("mem_size") = 1)
        .def("update", &ROI::update);

    py::class_<MACDResult>(m, "MACDResult")
        .def_readwrite("macd", &MACDResult::macd)
        .def_readwrite("signal", &MACDResult::signal)
        .def_readwrite("hist", &MACDResult::hist);

    py::class_<MACD, Indicator<MACDResult>>(m, "MACD")
        .def(py::init<int, int, int, int>(),
             py::arg("short_period"),
             py::arg("long_period"),
             py::arg("diff_period"),
             py::arg("mem_size") = 1)
        .def("update", &MACD::update);

    py::class_<ATR, Indicator<double>>(m, "ATR")
        .def(py::init<int, int>(),
            py::arg("period"),
            py::arg("mem_size") = 1)
        .def("update", &ATR::update,
            py::arg("low_price"),
            py::arg("high_price"),
            py::arg("close_price"));

    m.def("roi", &calculate_roi, "Calculate return on investment");
}
