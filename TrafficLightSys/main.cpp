#include <iostream>
#include "Simulator.h"

int main()
{
    std::cout << "Traffic Light System Simulation" << std::endl;
    std::cout << "-------------------------------" << std::endl;

    Simulator sim(2, 2, 42);
    sim.run(5);

    return 0;
}