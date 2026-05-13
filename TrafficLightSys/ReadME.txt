Team Members: Royam Nayyar, Sherry Salib , Israelia Magen. 

 Project Name:  Traffic Light System Simulation

Description

This project is a traffic light simulation system that compares two different traffic control methods: fixed timing control and adaptive traffic control. The goal of the project is to see whether adaptive signal control can reduce congestion and wait times better than a traditional fixed timer system.

The backend simulation logic was built in C++, while the GUI was created using Python and tkinter. pybind11 is used to connect the Python frontend to the C++ backend.


 Languages & Dependencies

 Main Languages
- C++
- Python

 C++ Libraries
- <vector>
- <iostream>
- <cstdlib>
- <ctime>

Python Libraries
- tkinter
- pybind11

---

 Project Structure

TrafficLightController/
│
├── TrafficLightSys/
│   ├── Intersection.cpp
│   ├── Intersection.h
│   ├── Simulator.cpp
│   ├── Simulator.h
│   ├── bindings.cpp
│   ├── app.py
│   ├── CMakeLists.txt
│   └── build/
│
├── docs/
│   └── ReadMe.txt

 Algorithms Used

1. Fixed Timing Control

The fixed timing system switches traffic lights after a fixed amount of time without checking traffic conditions. This acts as the baseline comparison system.


2. Greedy Adaptive Signal Control

The adaptive system checks congestion levels using queue sizes and wait times. After the minimum green-light time is reached, the system gives priority to the direction with more congestion.

This is considered a greedy algorithm because it makes the best immediate decision based on the current traffic conditions instead of searching for a long-term optimal solution.


3. Grid-Based Simulation Loop

During each simulation step, the simulator traverses every intersection in the grid, generates random traffic, updates both systems, moves cars, updates wait times, and refreshes the simulation.

How The System Works

The project is split into two main parts.

C++ Backend

The C++ backend handles:
- queue management
- congestion calculations
- traffic light switching
- adaptive signal decisions
- simulation updates

Main backend files:
- Intersection.cpp
- Simulator.cpp



Python GUI

The Python GUI is responsible for:
- drawing the intersections
- displaying traffic lights
- showing queue sizes
- showing congestion values
- comparing fixed vs adaptive control side-by-side

Main GUI file:
- app.py



TO Run Project

*********Must use python v.3 with proper dir to pyd file. *******
cd ..(to TrafficLightSys folder)
python app.py


If no GUI display is available, the project automatically switches to terminal mode to demonstrate the backend functionality.

Terminal Example ** TEST

Time: 1

FIXED INTERSECTION
Light: NS Green
Queues -> N:1 S:2 E:0 W:1
Congestion -> NS:3 EW:1

ADAPTIVE INTERSECTION
Light: NS Green
Queues -> N:1 S:2 E:0 W:1
Congestion -> NS:3 EW:1



 GUI Features

The GUI includes: side-by-side fixed vs adaptive comparison
- live queue visualization
- congestion tracking
- real-time updates
- automatic simulation mode
- manual step mode


Complexity Analysis

| Operation | Complexity |

| Add Cars | O(1) |
| Move Cars | O(1) |
| Congestion Calculation | O(1) |
| Adaptive Signal Decision | O(1) |
| Full Simulation Step | O(rows × columns) | O(n) where n is the number of intersections |

 Current Limitations

Some limitations of the current version:
- traffic is randomly generated
- intersections are not connected together yet
- no turning lanes
- no emergency vehicle handling
- cars disappear after leaving an intersection instead of traveling to another one


 GitHub Repository
https://github.com/roy0207/TrafficLightController



