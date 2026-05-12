#include "Simulator.h"
#include <cstdlib>
#include <iostream>

// Implementation of the Simulator class functions

// The constructor initializes the simulation state, sets up the random seed, and creates two grids of intersections (fixed and adaptive) 
// with the same initial conditions for a fair comparison.
Simulator::Simulator(int numRows, int numCols, int seedValue)
{
    currentTime = 0;
    seed = seedValue;
    rows = numRows;
    cols = numCols;

	// Seed the random number generator
    srand(seed);

    // Resize both grids
    fixedGrid.resize(rows);
    adaptiveGrid.resize(rows);

	// Initialize each intersection in both grids with the same parameters, except for the control mode.
    // The fixed grid uses fixed control, while the adaptive grid uses adaptive control.
    for (int r = 0; r < rows; r++)
    {
        fixedGrid[r].resize(cols);
        adaptiveGrid[r].resize(cols);

        for (int c = 0; c < cols; c++)
        {
            // Fixed-control intersection:
            // switches only after max time, ignores congestion
            fixedGrid[r][c] = Intersection(
                0, 0, 0, 0,
                Intersection::NS_Green,
                3,
                6,
                Intersection::Fixed_Control
            );

            // Adaptive-control intersection:
            // uses congestion and wait times
            adaptiveGrid[r][c] = Intersection(
                0, 0, 0, 0,
                Intersection::NS_Green,
                3,
                6,
                Intersection::Adaptive_Control
            );
        }
    }
}

// The step function advances the simulation by one time unit in our case 5 seconds. It generates random arrivals of cars for
// each direction at each intersection and updates the state of each intersection in both grids.
void Simulator::step()
{
    currentTime++;

    for (int r = 0; r < rows; r++)
    {
        for (int c = 0; c < cols; c++)
        {
            // Generate arrivals
            // These same arrivals are applied to both grids.
            // This makes the comparison fair.
            // we use modulo to limit the number of arrivals for demonstration purposes.
            int northCars = rand() % 3;
            int southCars = rand() % 3;
            int eastCars = rand() % 3;
            int westCars = rand() % 3;

			// Add out car arrivals to both grids
            fixedGrid[r][c].addCars(northCars, southCars, eastCars, westCars);
            adaptiveGrid[r][c].addCars(northCars, southCars, eastCars, westCars);

			// Update both intersections. They will process the same arrivals but may switch differently based on their control mode.
            fixedGrid[r][c].update();
            adaptiveGrid[r][c].update();
        }
    }
}


// This function is now obsolete in the code, we do not need it for GUI but we kept it for debug testing in terminal. 
void Simulator::run(int steps)
{
    for (int t = 0; t < steps; t++)
    {
        step();

        std::cout << "===== Time " << currentTime << " =====" << std::endl;

        std::cout << "\n===== FIXED GRID =====" << std::endl;
        for (int r = 0; r < rows; r++)
        {
            for (int c = 0; c < cols; c++)
            {
                std::cout << "Fixed Intersection [" << r << "][" << c << "]" << std::endl;
                fixedGrid[r][c].printStatus(currentTime);
            }
        }

        std::cout << "\n===== ADAPTIVE GRID =====" << std::endl;
        for (int r = 0; r < rows; r++)
        {
            for (int c = 0; c < cols; c++)
            {
                std::cout << "Adaptive Intersection [" << r << "][" << c << "]" << std::endl;
                adaptiveGrid[r][c].printStatus(currentTime);
            }
        }

        std::cout << std::endl;
    }

}

// Getter functions to access the number of rows, columns, and current simulation time. These are used by the GUI to display information and manage the layout.
int Simulator::getRows() const
{
    return rows;
}

int Simulator::getCols() const
{
    return cols;
}

int Simulator::getCurrentTime() const
{
    return currentTime;
}

const Intersection& Simulator::getFixedIntersection(int row, int col) const
{
    return fixedGrid[row][col];
}

const Intersection& Simulator::getAdaptiveIntersection(int row, int col) const
{
    return adaptiveGrid[row][col];
}