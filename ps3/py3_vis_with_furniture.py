"""
        Returns: an integer; the total number of tiles in the room
        """
import math
import random

import ps3_visualize
import pylab


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """

    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """

    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        if not type(width) == int or width <= 0:
            raise ValueError
        else:
            self.width = width
        if not type(height) == int or height <= 0:
            raise ValueError
        else:
            self.height = height
        if not type(dirt_amount) == int or dirt_amount < 0:
            raise ValueError
        else:
            self.dirt_amount = dirt_amount

        self.tiles = {}
        for x in range(width):
            for y in range(height):
                self.tiles[(x, y)] = self.dirt_amount

    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        if pos.get_x() > self.width:
            raise ValueError
        if pos.get_y() > self.height:
            raise ValueError
        pos_tile = math.floor(pos.get_x()), math.floor(pos.get_y())
        if self.tiles[pos_tile] < capacity:
            self.tiles[pos_tile] = 0
        else:
            self.tiles[pos_tile] = self.tiles[pos_tile] - capacity

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        try:
            if self.tiles[(m, n)] == 0:
                return True
            else:
                return False
        except KeyError:
            print('Tile you specified is not in the room!')

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        num_of_cleaned_tiles = 0
        for key in self.tiles.keys():
            if self.tiles[key] == 0:
                num_of_cleaned_tiles += 1
        return num_of_cleaned_tiles

    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        if pos.get_x() >= self.width or pos.get_y() >= self.height:
            return False
        elif pos.get_x() < 0 or pos.get_y() < 0:
            return False
        else:
            return True

    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        amount_od_dirt = self.tiles[(m, n)]
        return amount_od_dirt

    def get_num_tiles(self):
        # do not change -- implement in subclasses.
        raise NotImplementedError

    def is_position_valid(self, pos):
        """
        pos: a Position object.

        returns: True if pos is in the room and (in the case of FurnishedRoom)
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """

    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the
        specified room. The robot initially has a random direction and a random
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot
                  in a single time-step
        """
        self.room = room
        if speed <= 0:
            raise ValueError
        else:
            self.speed = speed
        if capacity < 0:
            raise ValueError
        else:
            self.capacity = capacity
        self.pos = Position(random.uniform(0, room.width), random.uniform(0, room.height))
        self.direction = random.uniform(0, 360)

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        return self.pos

    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.pos = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid,
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError


# === Problem 2
class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return len(self.tiles.keys())

    def is_position_valid(self, pos):
        """
        pos: a Position object.

        Returns: True if pos is in the room, False otherwise.
        """
        return self.is_position_in_room(pos)

    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        return Position(random.uniform(0, self.width), random.uniform(0, self.height))


class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of
    furniture. The robot should not be able to land on these furniture tiles.
    """

    def __init__(self, width, height, dirt_amount):
        """
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.

        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []

    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored
        as (x, y) tuples in the list furniture_tiles

        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the
        entire room. Position is selected by randomly selecting the location of the
        bottom left corner of the piece of furniture so that the entire piece of
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i, j))

    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        if (m, n) in self.furniture_tiles:
            return True
        else:
            return False

    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        pos_tile = math.floor(pos.get_x()), math.floor(pos.get_y())
        if pos_tile in self.furniture_tiles:
            return True
        else:
            return False

    def is_position_valid(self, pos):
        """
        pos: a Position object.

        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        if self.is_position_in_room(pos) and not self.is_position_furnished(pos):
            return True
        else:
            return False

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        return len(self.tiles.keys()) - len(self.furniture_tiles)

    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        while True:
            position = Position(random.uniform(0, self.width), random.uniform(0, self.height))
            if self.is_position_valid(position):
                break
        return position


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid,
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity.
        """
        current_pos = self.get_robot_position()
        new_pos = current_pos.get_new_position(self.get_robot_direction(), self.speed)
        if self.room.is_position_valid(new_pos):
            self.set_robot_position(new_pos)
            self.room.clean_tile_at_position(self.pos, self.capacity)
        else:
            self.set_robot_direction(random.uniform(0, 360))


# Uncomment this line to see your implementation of StandardRobot in action!
# test_robot_movement(StandardRobot, EmptyRoom)
# test_robot_movement(StandardRobot, FurnishedRoom)

# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob

    def gets_faulty(self):
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p

    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        current_pos = self.get_robot_position()
        new_pos = current_pos.get_new_position(self.get_robot_direction(), self.speed)
        if self.room.is_position_valid(new_pos) and not self.gets_faulty():
            self.set_robot_position(new_pos)
            self.room.clean_tile_at_position(self.pos, self.capacity)
        else:
            self.set_robot_direction(random.uniform(0, 360))


# test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                   robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                FaultyRobot)
    """
    avrg_num_of_steps = []
    for index in range(num_trials):
        room = FurnishedRoom(width, height, dirt_amount)
        room.add_furniture_to_room()
        amt_of_tiles = room.get_num_tiles()
        cleaned_tiles = room.get_num_cleaned_tiles()
        anim = ps3_visualize.RobotVisualization(num_robots, width, height, True, delay=0.3)
        my_robots = []
        for i in range(1, num_robots + 1):
            my_robots.append(robot_type(room, speed, capacity))
        num_of_steps = 0
        while True:
            if cleaned_tiles / amt_of_tiles >= min_coverage:
                break
            else:
                for robot in my_robots:
                    robot.update_position_and_clean()
                    cleaned_tiles = room.get_num_cleaned_tiles()
                anim.update(room, my_robots)
                num_of_steps += 1
        avrg_num_of_steps.append(num_of_steps)
    anim.done()
    return sum(avrg_num_of_steps) / len(avrg_num_of_steps)


# for num_of_trials in (10, 20, 50, 100, 200):
#     print(f'Trials: {num_of_trials}')
#     print('avg time steps StandardRobot: ')
#     standard_robot = run_simulation(1, 1.0, 1, 20, 20, 3, 1.0, num_of_trials, StandardRobot)
#     print(standard_robot)
#     print('avg time steps FaultyRobot: ')
#     faulty_robot = run_simulation(1, 1.0, 1, 20, 20, 3, 1.0, num_of_trials, FaultyRobot)
#     print(faulty_robot)
#     print(f'Faulty robot performed: {(faulty_robot - standard_robot) / standard_robot} worse than Standard one.')
#     print('---------------------------**********************--------------------------')


run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 1, StandardRobot)


# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#
#
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions
#       10x30, 20x15, 25x12, and 50x6?
#
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = int(300 / width)
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

# show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
# show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
