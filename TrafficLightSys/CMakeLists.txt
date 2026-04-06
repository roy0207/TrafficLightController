# Minimum CMake version required
cmake_minimum_required(VERSION 3.18)

# Project name
project(TrafficLightSys LANGUAGES CXX)

# Use modern C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python development files and interpreter
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

# Find pybind11
# In Codespaces, we'll install pybind11 in the container
find_package(pybind11 CONFIG REQUIRED)

# Build the Python extension module
# IMPORTANT:
# The module name here should match what Python imports.
# Since you chose TrafficLightSys, Python will do:
#     import TrafficLightSys
pybind11_add_module(TrafficLightSys
    bindings.cpp
    Intersection.cpp
    Simulator.cpp
)

# Add include directories if needed
target_include_directories(TrafficLightSys PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)