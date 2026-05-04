// Include pybind11 core functionality.
// This allows us to create Python modules from C++ code.
#include <pybind11/pybind11.h>

// Include your C++ backend classes.
#include "Simulator.h"
#include "Intersection.h"

// Short alias for pybind11 namespace.
namespace py = pybind11;

/*
    This creates a Python module named TrafficLightSys.

    Python usage:
        import TrafficLightSys
*/
PYBIND11_MODULE(TrafficLightSys, m)
{
    /*
        ================================
        Exposing the Intersection class
        ================================
    */
    py::class_<Intersection>(m, "Intersection")

        // Queue getters
        .def("getNorthQueue", &Intersection::getNorthQueue)
        .def("getSouthQueue", &Intersection::getSouthQueue)
        .def("getEastQueue", &Intersection::getEastQueue)
        .def("getWestQueue", &Intersection::getWestQueue)

        // Wait-time getters
        .def("getNorthWaitTime", &Intersection::getNorthWaitTime)
        .def("getSouthWaitTime", &Intersection::getSouthWaitTime)
        .def("getEastWaitTime", &Intersection::getEastWaitTime)
        .def("getWestWaitTime", &Intersection::getWestWaitTime)

        // Congestion metrics
        .def("getNSCongestion", &Intersection::getNSCongestion)
        .def("getEWCongestion", &Intersection::getEWCongestion)

        // Light-state and control-mode values as integers
        // Light state:
        //   0 = NS_Green
        //   1 = EW_Green
        .def("getCurrentStateValue", &Intersection::getCurrentStateValue)

        // Control mode:
        //   0 = Fixed_Control
        //   1 = Adaptive_Control
        .def("getControlModeValue", &Intersection::getControlModeValue)

        // Time spent in current light phase
        .def("getCurrentStateTime", &Intersection::getCurrentStateTime);

    /*
        ================================
        Exposing the Simulator class
        ================================
    */
    py::class_<Simulator>(m, "Simulator")

        // Python usage:
        //   sim = TrafficLightSys.Simulator(rows, cols, seed)
        .def(py::init<int, int, int>())

        // Advance the simulation by one time step.
        .def("step", &Simulator::step)

        // Run multiple steps, mainly useful for CLI/debug testing.
        .def("run", &Simulator::run)

        // Grid size getters.
        .def("getRows", &Simulator::getRows)
        .def("getCols", &Simulator::getCols)

        // Current simulation time.
        .def("getCurrentTime", &Simulator::getCurrentTime)

        /*
            Fixed grid accessor.

            Returns a reference to an Intersection inside Simulator's fixedGrid.

            reference_internal means:
            - Python does not own this Intersection
            - the Intersection is tied to the Simulator object's lifetime
        */
        .def("getFixedIntersection", &Simulator::getFixedIntersection,
            py::return_value_policy::reference_internal)

        /*
            Adaptive grid accessor.

            Returns a reference to an Intersection inside Simulator's adaptiveGrid.
        */
        .def("getAdaptiveIntersection", &Simulator::getAdaptiveIntersection,
            py::return_value_policy::reference_internal);
}