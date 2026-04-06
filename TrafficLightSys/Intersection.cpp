#include "Intersection.h"
#include <iostream>

Intersection::Intersection()
{
	north_queue = 0;
	south_queue = 0;
	east_queue = 0;
	west_queue = 0;

	northWaitTime = 0;
	southWaitTime = 0;
	eastWaitTime = 0;
	westWaitTime = 0;

	currentState = NS_Green;
	currentStateTime = 0;
	minStateTime = 3;
	maxStateTime = 6;
}

Intersection::Intersection(int north, int south, int east, int west,
	lightState initialState, int minTime, int maxTime)
{
	north_queue = north;
	south_queue = south;
	east_queue = east;
	west_queue = west;

	northWaitTime = 0;
	southWaitTime = 0;
	eastWaitTime = 0;
	westWaitTime = 0;

	currentState = initialState;
	currentStateTime = 0;
	minStateTime = minTime;
	maxStateTime = maxTime;
}

void Intersection::addCars(int north, int south, int east, int west)
{
	north_queue += north;
	south_queue += south;
	east_queue += east;
	west_queue += west;
}

void Intersection::moveCars()
{
	if (currentState == NS_Green)
	{
		if (north_queue > 0)
			north_queue--;

		if (south_queue > 0)
			south_queue--;
	}
	else
	{
		if (east_queue > 0)
			east_queue--;

		if (west_queue > 0)
			west_queue--;
	}
}

void Intersection::updateWaitTimes()
{
	if (currentState == NS_Green)
	{
		northWaitTime = 0;
		southWaitTime = 0;

		if (east_queue > 0)
			eastWaitTime++;
		else
			eastWaitTime = 0;

		if (west_queue > 0)
			westWaitTime++;
		else
			westWaitTime = 0;
	}
	else
	{
		eastWaitTime = 0;
		westWaitTime = 0;

		if (north_queue > 0)
			northWaitTime++;
		else
			northWaitTime = 0;

		if (south_queue > 0)
			southWaitTime++;
		else
			southWaitTime = 0;
	}
}

int Intersection::getCurrentStateValue() const 
{
	return static_cast<int>(currentState);
}

int Intersection::getNSCongestion() const
{
	return north_queue + south_queue + northWaitTime + southWaitTime;
}

int Intersection::getEWCongestion() const
{
	return east_queue + west_queue + eastWaitTime + westWaitTime;

}
int Intersection::getNorthQueue() const 
{
	return north_queue;
}

int Intersection::getSouthQueue() const
{
	return south_queue;
}
int Intersection::getEastQueue() const
{
	return east_queue;
}
int Intersection::getWestQueue() const
{
	return west_queue;
}

int Intersection::getNorthWaitTime() const
{
	return northWaitTime;
}
int Intersection::getSouthWaitTime() const
{
	return southWaitTime;
}
int Intersection::getEastWaitTime() const
{
	return eastWaitTime;
}
int Intersection::getWestWaitTime() const
{
	return westWaitTime;
}

Intersection::lightState Intersection::getCurrentState() const
{
	return currentState;
}
int Intersection::getCurrentStateTime() const
{
	return currentStateTime;
}




bool Intersection::shouldSwitch() const
{
	if (currentStateTime < minStateTime)
	{
		return false;
	}

	if (currentStateTime >= maxStateTime)
	{
		return true;
	}

	if (currentState == NS_Green)
	{
		return getEWCongestion() > getNSCongestion();
	}
	else
	{
		return getNSCongestion() > getEWCongestion();
	}
}

void Intersection::update()
{
	moveCars();
	updateWaitTimes();

	currentStateTime++;

	if (shouldSwitch())
	{
		std::cout << "Switching light state at time " << currentStateTime << " seconds" << std::endl;
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

	std::cout << "North Wait Time: " << northWaitTime << std::endl;
	std::cout << "South Wait Time: " << southWaitTime << std::endl;
	std::cout << "East Wait Time: " << eastWaitTime << std::endl;
	std::cout << "West Wait Time: " << westWaitTime << std::endl;

	std::cout << "NS Congestion: " << getNSCongestion() << std::endl;
	std::cout << "EW Congestion: " << getEWCongestion() << std::endl;

	std::cout << "Current Light State: "
		<< (currentState == NS_Green ? "North/South Green" : "East/West Green")
		<< std::endl;

	std::cout << "Current State Time: " << currentStateTime << std::endl;
	std::cout << "-----------------------------" << std::endl;
}