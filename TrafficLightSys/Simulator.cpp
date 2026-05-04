#include "Simulator.h"
#include <cstdlib>
#include <iostream>

Simulator::Simulator(int numRows, int numCols, int seedValue)
{
    currentTime = 0;
    seed = seedValue;
    rows = numRows;
    cols = numCols;

    srand(seed);

    // Resize both grids
    fixedGrid.resize(rows);
    adaptiveGrid.resize(rows);

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

void Simulator::step()
{
    currentTime++;

    for (int r = 0; r < rows; r++)
    {
        for (int c = 0; c < cols; c++)
        {
            // Generate arrivals ONCE.
            // These same arrivals are applied to both grids.
            // This makes the comparison fair.
            int northCars = rand() % 3;
            int southCars = rand() % 3;
            int eastCars = rand() % 3;
            int westCars = rand() % 3;

            fixedGrid[r][c].addCars(northCars, southCars, eastCars, westCars);
            adaptiveGrid[r][c].addCars(northCars, southCars, eastCars, westCars);

            fixedGrid[r][c].update();
            adaptiveGrid[r][c].update();
        }
    }
}

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