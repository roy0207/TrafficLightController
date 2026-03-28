
#include <iostream>
#include "Intersection.h"

int main()
{
	std::cout << "Traffic Light System Simulation" << std::endl;
	std::cout << "-------------------------------" << std::endl;

	// Create an intersection with initial queue lengths and state times
	Intersection intersection(5, 5, 5, 5, Intersection::NS_Green, 10);
	//print initial status
	intersection.printStatus(0);
	// Simulate for 30 seconds
	for (int time = 1; time <= 5; time++)
	{
		// Add random cars to the queues (for demonstration)
		int northCars = rand() % 3; // 0-2 cars
		int southCars = rand() % 3;
		int eastCars = rand() % 3;
		int westCars = rand() % 3;
		intersection.addCars(northCars, southCars, eastCars, westCars);
		intersection.update();
		intersection.printStatus(time);
	}
	

	return 0;
}