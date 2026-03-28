#include "Intersection.h"
#include <iostream>



Intersection::Intersection()
{
	north_queue = 0;
	south_queue = 0;
	east_queue = 0;
	west_queue = 0;

	currentState = NS_Green;
	currentStateTime = 0;
	maxStateTime = 5; // Switch every 5 seconds

}

Intersection::Intersection(int north, int south, int east, int west, lightState initialState, int maxTime)
{
	north_queue = north;
	south_queue = south;
	east_queue = east;
	west_queue = west;
	currentState = initialState;
	currentStateTime = 0;
	maxStateTime = maxTime; // Switch after specified maxTime (seconds)
}

void Intersection::addCars(int north, int south, int east, int west)
{
	north_queue += north;
	south_queue += south;
	east_queue += east;
	west_queue += west;

}

void Intersection::update()
{
	if (currentState == NS_Green)
	{
		// allow N/S cars to go
		if (north_queue > 0)
			north_queue--;

		if (south_queue > 0)
			south_queue--;
	}
	else
	{
		// allow E/W cars to go
		if (east_queue > 0)
			east_queue--;

		if (west_queue > 0)
			west_queue--;
	}

	currentStateTime++;

	if (currentStateTime >= maxStateTime)
	{
		switchState();
	}
}

void Intersection::switchState()
{
	if (currentState == NS_Green)
	{
		currentState = EW_Green;
	}
	else
	{
		currentState = NS_Green;
	}

	currentStateTime = 0;
}

void Intersection::printStatus(int currentTime) const 
{
	std::cout << "Time: " << currentTime << " seconds" << std::endl;
	std::cout << "North Queue: " << north_queue << " cars" << std::endl;
	std::cout << "South Queue: " << south_queue << " cars" << std::endl;
	std::cout << "East Queue: " << east_queue << " cars" << std::endl;
	std::cout << "West Queue: " << west_queue << " cars" << std::endl;
	std::cout << "Current Light State: " << (currentState == NS_Green ? "North/South Green" : "East/West Green") << std::endl;


}