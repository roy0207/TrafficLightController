#ifndef SIMULATOR_H
#define SIMULATOR_H

#include "Intersection.h"
#include <vector>

class Simulator
{
private:
    int currentTime;
    int seed;
    int rows;
    int cols;
    std::vector<std::vector<Intersection>> grid;

public:
    Simulator(int numRows, int numCols, int seedValue);

    void run(int steps);   // CLI / testing
    void step();           // GUI / single tick

    int getRows() const;
    int getCols() const;
    int getCurrentTime() const;

    const Intersection& getIntersection(int row, int col) const;
};

#endif