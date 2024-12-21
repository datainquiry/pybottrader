cmake_minimum_required(VERSION 3.15)
project(indicators)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(NOT TARGET pybind11::module)
    find_package(pybind11 REQUIRED)
endif()

# Platform specific flags
if(MSVC)
    # Windows-specific flags
    add_compile_options(/W4 /EHsc)
else()
    # Linux/macOS flags
    add_compile_options(-Wall -Wextra)
endif()

# Create module
pybind11_add_module(_indicators 
    src/bindings.cpp
)

# Include directories
target_include_directories(_indicators
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Platform-specific link options
if(APPLE)
    target_link_options(_indicators PRIVATE -undefined dynamic_lookup)
endif()

install(TARGETS _indicators
        LIBRARY DESTINATION pybottrader/indicators
)
