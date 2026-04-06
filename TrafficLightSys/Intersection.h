#ifndef INTERSECTION_H
#define INTERSECTION_H

class Intersection
{
public:
	enum lightState { NS_Green, EW_Green }; // which direction has the green light

private:
	lightState currentState; // current state of the traffic light

	// vehicle counts in each direction
	int north_queue;
	int south_queue;
	int east_queue;
	int west_queue;

	// wait timers for each direction
	int northWaitTime;
	int southWaitTime;
	int eastWaitTime;
	int westWaitTime;

	int currentStateTime; // how long current state has been active
	int maxStateTime;     // after this many seconds, switch phase
	int minStateTime;     // minimum time before switching

public:
	Intersection();
	Intersection(int north, int south, int east, int west,
		lightState initialState, int minTime, int maxTime);

	void addCars(int north, int south, int east, int west);

	void update();
	void moveCars();
	void updateWaitTimes();
	void switchState();

	// congestion approximations & getters
	int getNSCongestion() const;
	int getEWCongestion() const;
	int getNorthQueue() const;
	int getSouthQueue() const;
	int getEastQueue() const;
	int getWestQueue() const;

	int getNorthWaitTime() const;
	int getSouthWaitTime() const;
	int getEastWaitTime() const;
	int getWestWaitTime() const;

	lightState getCurrentState() const;
	//getter for currentStateTime so Python can access how 
	// long we've been in the current light phase
	// since we are using an enum, we can return the current 
	// state as an int (0 for NS_Green, 1 for EW_Green)
	int getCurrentStateValue() const;
	int getCurrentStateTime() const;


	bool shouldSwitch() const;

	void printStatus(int currentTime) const;
};

#endif