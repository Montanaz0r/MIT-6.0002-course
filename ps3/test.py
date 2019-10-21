# uncompyle6 version 3.5.0
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.7.3 (default, Mar 27 2019, 17:13:21) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: ps3_solutions.py
# Compiled at: 2016-11-10 04:38:40
# Size of source mod 2**32: 19384 bytes
import math, random, ps3_visualize, pylab
from ps3_verify_movement27 import test_robot_movement


class Position(object):
    r"""'\n    A Position represents a location in a two-dimensional room, where\n    coordinates are given by floats (x, y).\n    '"""

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
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):
        return 'Position: ' + str(math.floor(self.x)) + ', ' + str(math.floor(self.y))


class RectangularRoom(object):
    r"""'\n    A RectangularRoom represents a rectangular region containing clean or dirty\n    tiles.\n\n    A room has a width and a height and contains (width * height) tiles. Each tile\n    has some fixed amount of dirt. The tile is considered clean only when the amount\n    of dirt on this tile is 0.\n    '"""

    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        width = int(width)
        height = int(height)
        if width <= 0:
            print('width <= 0')
        if height <= 0:
            print('height <= 0')
        if dirt_amount < 0:
            print('dirt_amount < 0')
        self.tiles = {}
        self.width = width
        self.height = height
        if width > 0 and height > 0 and dirt_amount >= 0:
            for w_idx in range(width):
                for h_idx in range(height):
                    self.tiles[(w_idx, h_idx)] = dirt_amount

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
        self.tiles[(int(pos.get_x()), int(pos.get_y()))] -= capacity
        if self.tiles[(int(pos.get_x()), int(pos.get_y()))] < 0:
            self.tiles[(int(pos.get_x()), int(pos.get_y()))] = 0

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
        if self.tiles[(m, n)] == 0:
            return True
        return False

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        return len([dirt_amount for dirt_amount in self.tiles.values() if dirt_amount == 0])

    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        if (
                int(math.floor(pos.get_x())), int(math.floor(pos.get_y()))) in self.tiles:
            return True
        return False

    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        return self.tiles[(m, n)]

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        raise NotImplementedError

    def is_position_valid(self, pos):
        """
        pos: a Position object.

        returns: True if pos is in the room and (in the case of FurnishedRoom)
                 if position is unfurnished, False otherwise.
        """
        raise NotImplementedError

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        raise NotImplementedError


class Robot(object):
    r"""'\n    Represents a robot cleaning a particular room.\n\n    At all times, the robot has a particular position and direction in the room.\n    The robot also has a fixed speed and a fixed cleaning capacity.\n\n    Subclasses of Robot should provide movement strategies by implementing\n    update_position_and_clean, which simulates a single time-step.\n    '"""

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
        if speed <= 0:
            print('speed <= 0')
        if capacity <= 0:
            print('capacity <= 0')
        self.room = room
        self.speed = speed
        self.capacity = capacity
        self.pos = room.get_random_position()
        self.direction = 360 * random.random()

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

        Move the robot to a new position and mark the tile it is on as having
        been cleaned by capacity amount.
        """
        raise NotImplementedError


class EmptyRoom(RectangularRoom):
    r"""'\n    An EmptyRoom represents a RectangularRoom with no furniture.\n    '"""

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
        return Position(self.width * random.random(), self.height * random.random())


class FurnishedRoom(RectangularRoom):
    r"""'\n    A FurnishedRoom represents a RectangularRoom with a rectangular piece of \n    furniture. The robot should not be able to land on these furniture tiles.\n    '"""

    def __init__(self, width, height, dirt_amount):
        """
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        RectangularRoom.__init__(self, width, height, dirt_amount)
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
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i, j))

    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        if (
                m, n) in self.furniture_tiles:
            return True
        return False

    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        return self.is_tile_furnished(int(pos.get_x()), int(pos.get_y()))

    def is_position_valid(self, pos):
        """
        pos: a Position object.

        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        return self.is_position_in_room(pos) and not self.is_position_furnished(pos)

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        return len(self.tiles.keys()) - len(self.furniture_tiles)

    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        pos = Position(self.width * random.random(), self.height * random.random())
        while 1:
            if not self.is_position_valid(pos):
                pos = Position(self.width * random.random(), self.height * random.random())

        return pos


class StandardRobot(Robot):
    r"""'\n    A StandardRobot is a Robot with the standard movement strategy.\n\n    At each time-step, a StandardRobot attempts to move in its current\n    direction; when it would hit a wall or furtniture, it *instead*\n    chooses a new direction randomly.\n    '"""

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and clean the dirt on the tile
        by its given capacity.
        """
        new_pos = self.pos.get_new_position(self.direction, self.speed)
        if self.room.is_position_valid(new_pos):
            self.pos = new_pos
            self.room.clean_tile_at_position(self.pos, self.capacity)
        else:
            self.set_robot_direction(360 * random.random())


class FaultyRobot(Robot):
    r"""'\n    A FaultyRobot is a robot that will not the tile it moves to and\n    pick a new, random direction for itself with probability p rather\n    than simply cleaning the tile it moves to.\n    '"""
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
        A FaultyRobot get faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p

    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the tile and change its direction randomly.
        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        if self.gets_faulty():
            self.set_robot_direction(360 * random.random())
        else:
            new_pos = self.pos.get_new_position(self.direction, self.speed)
            if self.room.is_position_valid(new_pos):
                self.pos = new_pos
                self.room.clean_tile_at_position(self.pos, self.capacity)
            else:
                self.set_robot_direction(360 * random.random())


def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials, robot_type):
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
    total_time_steps = 0
    for _ in range(num_trials):
        room = EmptyRoom(width, height, dirt_amount)
        robots = []
        for _ in range(num_robots):
            robots.append(robot_type(room, speed, capacity))

        while float(room.get_num_cleaned_tiles()) / room.get_num_tiles() < min_coverage:
            for robot in robots:
                robot.update_position_and_clean()

            total_time_steps += 1

    return float(total_time_steps) / num_trials


def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print('Plotting', num_robots, 'robots...')
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
        height = 300 / width
        print('Plotting cleaning time for a room of width:', width, 'by height:', height)
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