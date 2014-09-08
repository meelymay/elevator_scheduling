Elevator Scheduling
===================

My ElevatorSystem consists of a list of elevators, each keeping track of their own state.

You can run this project simply with $ python elevator.py

Interface
====
The elevator system interface has three methods: status, step, and pickup.

status() prints the current status of all elevators in the system, including their current floor and planned stops.

step() increments the floor of each elevator in its current direction and updates the planned stops to remove the current floor.

pickup(floor, direction, elevator) includes the functionality for both calling an elevator in a direction from a floor, and requesting a floor from within an elevator. It also allows you to call a specific elevator to a floor in a specific direction.

Algorithm
====

The algorithm used is a considerable improvement over FCFS by scheduling floors to the elevators with the cheapest "cost." This cost is defined as the current number of floors the elevator will pass before stopping at the requested floor in the correct direction. This cost function does not take into account the number of floors that will have to be stopped at before the desired floor (which is likely the primary contributor to wait time). In addition, the cost at the time of scheduling will not necessarily be the exact wait time as additional floors could be scheduled that add to the distance needed to travel, but it's a reasonable heuristic.

Concurrency
====

It is worth noting that this interface does not support concurrent updates. There are several places where race conditions could occur, for example, if a request is made during an update, the direction of the elevator could change to be the opposite. It is also probably possible to overwrite a floor request when starting from an empty forward stop list. To make this system thread safe we could make the updates and pickup scheduling atomic.
