class Elevator:
    def __init__(self, id):
        self.id = id
        self.forward_stops = set([])
        self.destination = 0
        self.backward_stops = set([])
        self.second_destination = 0
        self.last_stops = set([])
        self.position = 0
        self.direction = 0

    def pickup(self, floor, direction):
        if not self.forward_stops:
            # adding first stop, set direction etc
            self.forward_stops.add(floor)
            distance = floor - self.position
            self.direction = 0 if distance == 0 else distance/abs(distance)
            return
        if direction in [self.direction, 0]:
            if (floor > self.position and self.direction > 0) or (floor < self.position and self.direction < 0):
                # simple forward stop
                self.forward_stops.add(floor)
            elif direction != 0:
                # we won't be going the right direction until after going back
                self.last_stops.add(floor)
            else:
                # stop at this floor as soon as we reach it, direction doesn't matter
                self.backward_stops.add(floor)
        else:
            # stop at this floor in the right direction, on the way back
            self.backward_stops.add(floor)

    def forward_max(self):
        if self.direction >= 0:
            return max(self.forward_stops)
        else:
            return min(self.forward_stops)

    def backward_max(self):
        if self.direction < 0:
            return max(self.forward_stops)
        else:
            return min(self.forward_stops)

    # TODO include cost for increasing the wait to other floors
    def insert_cost(self, floor, direction):
        '''approximate how long it will take to reach the floor in this direction'''
        if not self.forward_stops:
            # just forward cost
            return abs(self.position - floor)
        if direction in[self.direction, 0]:
            if floor in range(min(self.forward_stops), max(self.forward_stops)):
                # just forward cost
                return abs(floor - self.position)
            elif direction != 0:
                # the cost of going all the way forward, all the way back, and turning around (for direction)
                return abs(self.forward_max() - self.position) + abs(self.forward_max() - self.backward_max()) + abs(floor - self.backward_max())                
            else:
                # all the way forward and partly back
                return abs(self.forward_max() - self.position) + abs(self.forward_max() - floor)
        else:
            # all the way forward and partly back
            return abs(self.forward_max() - self.position) + abs(self.forward_max() - floor)

    def update(self):
        '''advance the elevator in the correct direction, remove stops from plan'''
        self.position += self.direction
        if self.position in self.forward_stops:
            self.forward_stops.remove(self.position)
        if not self.forward_stops:
            self.direction = -self.direction
            self.forward_stops = self.backward_stops
            self.backward_stops = self.last_stops
            self.last_stops = set([])

    def __str__(self):
        return "ID: %s\tFloor: %s\tPlan: f%s b%s l%s" % (self.id, self.position, 
                                                         list(self.forward_stops),
                                                         list(self.backward_stops),
                                                         list(self.last_stops))

class ElevatorSystem:

    def __init__(self, num_elevators):
        self.elevators = [Elevator(x) for x in range(num_elevators)]
    
    def status(self):
        for e in self.elevators:
            print e

    def update(self):
        for elevator in self.elevators:
            elevator.update()

    def pickup(self, floor, direction=0, elevator=None):
        if elevator == None:
            elevator = min(self.elevators, key=lambda x: x.insert_cost(floor, direction))
        else:
            elevator = self.elevators[elevator]
        elevator.pickup(floor, direction)

    def __str__(self):
        return '\n'.join([str(e) for e in self.elevators])

if __name__ == "__main__":
    elevator_system = ElevatorSystem(6)
    request = None
    while request != "EXIT":
        elevator_system.update()
        try:
            request = raw_input("Request a floor: ")
            fields = request.split()
            floor = int(fields[0])
            direction = 0
            elevator = None
            if len(fields) > 1:
                direction = int(fields[1])
            if len(fields) > 2:
                elevator = int(fields[2])
        except:
            print elevator_system
            continue
        elevator_system.pickup(floor, direction, elevator)
        print elevator_system
