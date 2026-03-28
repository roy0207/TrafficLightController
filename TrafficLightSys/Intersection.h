#ifndef INTERSECTION_H
#define INTERSECTION_H



class Intersection 
{
public:
	enum lightState { NS_Green, EW_Green }; // which direction has the green light
	lightState currentState; // current state of the traffic light
private:
	//vehicle counts in each direction
	int north_queue; 
	int south_queue; 
	int east_queue;  
	int west_queue;  

	//wait timers for each direction
	int northWaitTime;
	int southWaitTime;
	int eastWaitTime;
	int westWaitTime;



	int currentStateTime; // how long current state has been active
	int maxStateTime; // after this many seconds, switch phase
	int minStateTime; // minimum time for a state before it can switch (to prevent too rapid switching)

	

public:


	Intersection();
	//parameterized constructor to set initial queue lengths and state times
	Intersection(int north, int south, int east, int west, lightState initialState, int maxTime);

	void addCars(int north, int south, int east, int west);
	void update();
	void switchState();

	//congestion aproximations
	int getNSCongestion(); // congestion level for north-south direction
	int getEWCongestion(); // congestion level for east-west direction

	//bool switch_State(); // determine if we should switch state based on congestion and timers

	void printStatus(int currentTime) const;






};
#endif