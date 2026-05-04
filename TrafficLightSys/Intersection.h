#ifndef INTERSECTION_H
#define INTERSECTION_H

class Intersection
{
public:
	enum lightState { NS_Green, EW_Green };
	enum controlMode { Fixed_Control, Adaptive_Control };

private:
	controlMode mode;
	lightState currentState;

	int north_queue;
	int south_queue;
	int east_queue;
	int west_queue;

	int northWaitTime;
	int southWaitTime;
	int eastWaitTime;
	int westWaitTime;

	int currentStateTime;
	int maxStateTime;
	int minStateTime;

public:
	Intersection();

	Intersection(int north, int south, int east, int west,
		lightState initialState, int minTime, int maxTime, controlMode selectedMode);

	void addCars(int north, int south, int east, int west);

	void update();
	void moveCars();
	void updateWaitTimes();
	void switchState();

	int getCurrentStateValue() const;
	int getControlModeValue() const;

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
	int getCurrentStateTime() const;

	bool shouldSwitch() const;

	void printStatus(int currentTime) const;
};

#endif