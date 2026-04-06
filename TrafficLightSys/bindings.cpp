// Include pybind11 core functionality
// This allows us to create Python modules from C++ code
//#include <pybind11/pybind11.h>

// Include your C++ backend classes
#include <pybind11/pybind11.h>
#include "Simulator.h"
#include "Intersection.h"

// Create a shorter alias for pybind11 namespace
// So we can write py:: instead of pybind11::
namespace py = pybind11;

/*
    This macro defines a Python module.

    Format:
    PYBIND11_MODULE(module_name, variable_name)

    - module_name → what Python will import
      Example: import traffic_sim

    - variable_name → the module object we add classes/functions to
*/
PYBIND11_MODULE(TrafficLightSys, m)
{
    /*
        ================================
        Exposing the Intersection class
        ================================
    */

    py::class_<Intersection>(m, "Intersection")

        // Bind getter functions so Python can access state
        // Each .def() exposes a C++ method to Python

        .def("getNorthQueue", &Intersection::getNorthQueue)
        .def("getSouthQueue", &Intersection::getSouthQueue)
        .def("getEastQueue", &Intersection::getEastQueue)
        .def("getWestQueue", &Intersection::getWestQueue)

        .def("getNorthWaitTime", &Intersection::getNorthWaitTime)
        .def("getSouthWaitTime", &Intersection::getSouthWaitTime)
        .def("getEastWaitTime", &Intersection::getEastWaitTime)
        .def("getWestWaitTime", &Intersection::getWestWaitTime)

        // Congestion metrics
        .def("getNSCongestion", &Intersection::getNSCongestion)
        .def("getEWCongestion", &Intersection::getEWCongestion)

        // Time spent in current light phase
        .def("getCurrentStateTime", &Intersection::getCurrentStateTime)

        // Current light state (NS_Green or EW_Green)
        //.def("getCurrentState", &Intersection::getCurrentState);
        .def("getCurrentStateValue", &Intersection::getCurrentStateValue);

    /*
        ================================
        Exposing the Simulator class
        ================================
    */

    py::class_<Simulator>(m, "Simulator")

        /*
            Bind constructor

            Python usage:
            sim = Simulator(rows, cols, seed)

            Example:
            sim = Simulator(2, 2, 42)
        */
        .def(py::init<int, int, int>())

        /*
            step()

            Advances simulation by ONE time step.

            This is the most important function for GUI.
            GUI will call this repeatedly.
        */
        .def("step", &Simulator::step)

        /*
            run()

            Runs multiple steps (mainly for CLI/testing).
        */
        .def("run", &Simulator::run)

        /*
            Grid size getters
        */
        .def("getRows", &Simulator::getRows)
        .def("getCols", &Simulator::getCols)

        /*
            Current simulation time
        */
        .def("getCurrentTime", &Simulator::getCurrentTime)

        /*
            getIntersection(row, col)

            Returns a reference to an Intersection object inside the grid.

            IMPORTANT:
            We use reference_internal because:
            - Simulator owns the grid
            - Intersection lives inside Simulator
            - Python should NOT copy it
            - Python must not outlive Simulator

            This ensures safe memory behavior.
        */
        .def("getIntersection", &Simulator::getIntersection,
            py::return_value_policy::reference_internal);
}