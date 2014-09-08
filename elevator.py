import sys

# TODO these are the worst
def insert_sorted(plan, floor, start, end):
    print "should be inserting",floor,"between",start,end
    if abs(end - start) < 2:
        if plan[start] == floor or plan[end] == floor:
            # we don't need to re-add a floor already in the plan
            print "not adding floor here",floor
            return
        elif floor < plan[start]:
            print "floor less than start"
            if plan[end] >= plan[start]:
                plan.insert(start, floor)
            else:
                if floor < plan[end]:
                    plan.insert(end+1, floor)
                else:
                    plan.insert(end, floor)
        elif floor > plan[end]:
            print "floor more than start"
            if plan[end] >= plan[start]:
                plan.insert(end+1, floor)
            else:
                if floor > plan[start]:
                    plan.insert(start, floor)
                else:
                    plan.insert(end, floor)
        else:
            plan.insert(end, floor)
    else:
        mid = (end + start)/2
        if floor == plan[mid]:
            # we don't need to readd a floor already in the plan
            print "not adding floor",floor
            return
        elif floor > plan[mid]:
            # the floor is greater than the mid point
            if plan[end] > plan[start]:
                # we're sorting up
                insert_sorted(plan, floor, mid, end)
            else:
                # we're sorting down
                insert_sorted(plan, floor, start, mid)
        else:
            # the floor is less than the mid point
            if plan[end] > plan[start]:
                # we're sorting up
                insert_sorted(plan, floor, start, mid)
            else:
                # we're sorting down
                insert_sorted(plan, floor, mid, end)

class Elevator:

    def __init__(self, id):
        self.id = id
        self.position = 0
        # TODO this should be a linked list
        self.plan = []

    def direction(self):
        '''returns 1 if going up, -1 if down, 0 if stationary'''
        if self.plan:
            delta = self.plan[0] - self.position
            return delta/abs(delta)
        else:
            return 0

    def update(self):
        self.position += self.direction()
        if self.plan and self.plan[0] == self.position:
            self.plan.pop(0)

    def cost(self, floor, direction):
        '''returns the approximate number of floors before stopping 
        at the request in the correct direction'''
        # TODO fix this
        return abs(self.position - floor)

    def pickup(self, floor, direction):
        if self.plan:
            distance = floor - self.position
            print "distance ", distance
            if direction == 0 or direction == self.direction():
                print "\tcalled in same direction"
                if distance/abs(distance) == self.direction():
                    print "\t\tfloor is in current direction"
                    insert_sorted(self.plan, floor, 0, self.destination_index())
                else:
                    print "\t\tfloor NOT in current direction"
                    insert_sorted(self.plan, floor, self.destination_index(), self.second_destination_index())
            else:
                print "\tcalled in diff direction"
                if distance/abs(distance) == self.direction():
                    print "\tfloor is in curr dir"
                    insert_sorted(self.plan, floor, self.second_destination_index(), len(self.plan)-1)
                else:
                    print "\tfloor is in diff dir"
                    insert_sorted(self.plan, floor, self.destination_index(), self.second_destination_index())
        else:
            self.plan.append(floor)

    # TODO these should be indices, not values
    def destination_index(self):
        # TODO could keep this info more efficiently
        if self.plan:
            return max(range(len(self.plan)), key=lambda x: self.plan[x]*self.direction())
        else:
            return 0

    def second_destination_index(self):
        if self.plan:
            return max(range(self.destination_index(), len(self.plan)), key=lambda x: -self.plan[x]*self.direction())
        else:
            return 0

    def __str__(self):
        return "ID: %s\tFloor: %s\tPlan: %s" % (self.id, self.position, self.plan)
        

class ElevatorSystem:

    def __init__(self, num_floors, num_elevators):
        self.num_floors = num_floors
        self.elevators = [Elevator(x) for x in range(num_elevators)]
    
    def status(self):
        for e in self.elevators:
            print e

    def update(self):
        for elevator in self.elevators:
            elevator.update()

    def pickup(self, floor, direction=0):
        elevator = min(self.elevators, key=lambda x: x.cost(floor, direction))
        elevator.pickup(floor, direction)

if __name__ == "__main__":
    elevator_system = ElevatorSystem(20, 1)
    request = None
    while request != -1:
        elevator_system.update()
        try:
            request = int(raw_input("Request a floor: "))
        except:
            continue
        elevator_system.pickup(request)
        elevator_system.status()
