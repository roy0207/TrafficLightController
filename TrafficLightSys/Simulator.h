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

    // Two separate grids with the same layout
    std::vector<std::vector<Intersection>> fixedGrid;
    std::vector<std::vector<Intersection>> adaptiveGrid;

public:
    Simulator(int numRows, int numCols, int seedValue);

    void step();
    void run(int steps);

    int getRows() const;
    int getCols() const;
    int getCurrentTime() const;

    const Intersection& getFixedIntersection(int row, int col) const;
    const Intersection& getAdaptiveIntersection(int row, int col) const;
};

#endif