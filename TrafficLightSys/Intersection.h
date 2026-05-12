#ifndef INTERSECTION_H
#define INTERSECTION_H


//Intersection class will privide declartion for functions that handle the state of the light, the queues of cars, and the wait times for each direction.
// It will also contain the logic for switching the light state based on the control mode (fixed or adaptive).
 

class Intersection
{
public:
	// Define enums for light states and control modes for simplicity
	enum lightState { NS_Green, EW_Green };
	enum controlMode { Fixed_Control, Adaptive_Control };

private:
	// State variables
	controlMode mode;
	lightState currentState;

	// Queues for each direction
	int north_queue;
	int south_queue;
	int east_queue;
	int west_queue;

	// Wait times for each direction
	int northWaitTime;
	int southWaitTime;
	int eastWaitTime;
	int westWaitTime;

	// Timing for state changes
	int currentStateTime;
	int maxStateTime;
	int minStateTime;

public:
	//Declaration of functions for the Intersection class
	
	// Default constructor
	Intersection();
	// Parameterized constructor
	Intersection(int north, int south, int east, int west,
		lightState initialState, int minTime, int maxTime, controlMode selectedMode);

	// Function to add cars to the queues
	void addCars(int north, int south, int east, int west);

	// Function to update the state of the intersection (move cars, update wait times, and switch state if needed)
	void update();

	// Function to move cars through the intersection based on the current light state.
	void moveCars();

	// Function to update wait times for cars in the queues. Cars in the direction with a red light will have their wait time increased,
	void updateWaitTimes();

	// Function to switch the light state from NS_Green to EW_Green or vice versa, and reset the state timer.
	void switchState();

	//more getters 
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


	// Getter functions to retrieve the current state and control mode as integers for easier display and comparison.
	lightState getCurrentState() const;

	int getCurrentStateTime() const;

	// Function to determine if the traffic light should switch based on the control mode and congestion levels.
	// This is where our main algorithm for adaptive control is implemented.
	bool shouldSwitch() const;

	//Debugging function for terminal use
	void printStatus(int currentTime) const;
};

#endif 