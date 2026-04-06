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

    grid.resize(rows, std::vector<Intersection>(cols));
}

void Simulator::step()
{
    currentTime++;

    for (int r = 0; r < rows; r++)
    {
        for (int c = 0; c < cols; c++)
        {
            int northCars = rand() % 3;
            int southCars = rand() % 3;
            int eastCars = rand() % 3;
            int westCars = rand() % 3;

            grid[r][c].addCars(northCars, southCars, eastCars, westCars);
            grid[r][c].update();
        }
    }
}

void Simulator::run(int steps)
{
    for (int t = 0; t < steps; t++)
    {
        step();

        std::cout << "===== Time " << currentTime << " =====" << std::endl;

        for (int r = 0; r < rows; r++)
        {
            for (int c = 0; c < cols; c++)
            {
                std::cout << "Intersection [" << r << "][" << c << "]" << std::endl;
                grid[r][c].printStatus(currentTime);
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

const Intersection& Simulator::getIntersection(int row, int col) const
{
    return grid[row][col];
}