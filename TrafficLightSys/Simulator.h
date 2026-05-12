#ifndef SIMULATOR_H
#define SIMULATOR_H

#include "Intersection.h"
#include <vector>


// Simulator class manages the grid of intersections and the overall simulation logic. It contains two separate grids: one for fixed control and one for adaptive control
// this allowing us to compare their performance under the same traffic conditions.
class Simulator
{
private:
	// Simulation state variables for tracking time, random seed, and grid dimensions.
    int currentTime;
    int seed;
    int rows;
    int cols;

    // We will use 2D vector for two separate grids with the same layout and input 
    std::vector<std::vector<Intersection>> fixedGrid;
    std::vector<std::vector<Intersection>> adaptiveGrid;

public:
    Simulator(int numRows, int numCols, int seedValue);
    
	// member functions to step simulation forward, run for multiple steps, and access grid and time information.
    void step();
    void run(int steps);

    int getRows() const;
    int getCols() const;
    int getCurrentTime() const;

	// Accessor functions to get references to Intersections in the fixed and adaptive grids.
    // These will be used by the GUI to display the state of each intersection.
    const Intersection& getFixedIntersection(int row, int col) const;
    const Intersection& getAdaptiveIntersection(int row, int col) const;
};

#endif