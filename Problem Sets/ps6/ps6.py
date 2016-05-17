# Problem Set 6: Simulating robots
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 3:00

import math
import random

import ps6_visualize
import pylab
import time

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        
        #Build a 2-Dimensional Array to store a Bool representing visted
        #Room is defined as two lists with width represented as the first dimenion
        #and height represented as the second dimension.  i.e. [x][y]
        #The room is oriented with the origin in the upper left
        self.room = []
        self.width = width
        self.height = height
        self.numCleaned = 0
        
        for c in xrange(width):
			self.room.append([])
			for r in xrange(height):
				self.room[c].append(False)
	
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        
        #Truncate position floats(i.e. position (1.99, 3.99) is (1,3))
        x = int(pos.getX())
        y = int(pos.getY())
                
        if not self.isTileCleaned(x, y):			
			self.room[x][y] = True
			self.numCleaned += 1
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        
        #Assuming m = x-coord, and n = y-coord
        return self.room[m][n]
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height
        
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """

        return self.numCleaned

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        #Get Random X, and Y
        x = self.width * random.random()
        y = self.height * random.random()
                
        return Position(x, y)                

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        
        return x >=0 and x <= self.width and y >=0 and y <= self.height
        
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.direction = getRandomDirection()
        self.position = room.getRandomPosition()
        
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        #Get position after movement
        newPosition = self.position.getNewPosition(self.getRobotDirection(), self.speed)
        
        #while new position outside room, choose new direction and get a new position
        while not self.room.isPositionInRoom(newPosition):
			self.setRobotDirection(getRandomDirection())
			newPosition = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        
        #Set new Position
        self.setRobotPosition(newPosition)
        
        #Clean square in room
        self.room.cleanTileAtPosition(newPosition)
        
# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    
    total_steps=0
        
    #Run Simulation
    for trial in xrange(num_trials):			
		#Setup Robot Visualization
		#anim = ps6_visualize.RobotVisualization(num_robots, width, height)
			
		#Build simulation
		room = RectangularRoom(width, height)
		robots = []
		trial_steps = 0
		min_tiles_to_clean = room.getNumTiles() * min_coverage
		
		for i in xrange(num_robots):		
			#Add Robot to robot collection
			robots.append(robot_type(room, speed))    
		
		while room.getNumCleanedTiles() < min_tiles_to_clean:
			#Run step
			for robot in robots:
				robot.updatePositionAndClean()
				
			#Draw Frame of Robot Visualization
			#anim.update(room, robots)
							
			trial_steps += 1
			
		#Add trial steps to total steps
		total_steps += trial_steps
	
	#End Visualization
    #anim.done()
		
    return float(total_steps) / num_trials

def getRandomDirection():
	return random.randint(0,359)

# === Problem 4
#
# 1) How long does it take to clean 80% of a 20x20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20x20, 25x16, 40x10, 50x8, 80x5, and 100x4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    
    times = []
    
    #Build list of times
    for i in xrange(1,11):
		times.append(runSimulation(i, 1, 20, 20, .8, 100, StandardRobot))
    
    pylab.plot(xrange(1,11), times)
    pylab.title('Time to clean 80% of a 20x20 room with various numbers of robots')
    pylab.xlabel('Number of Robots')
    pylab.ylabel('Time (steps)')
    pylab.show()

#showPlot1()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    #Rooms represented by list of Tuples (x,y)
    rooms = [(20,20),(25,16),(40,10),(50,8),(80,5),(100,4)]
    roomRatio = []
    times = []
    
    for room in rooms:
		times.append(runSimulation(2, 1, room[0], room[1], .8, 1000, StandardRobot))
		roomRatio.append(float(room[0])/room[1])
		
    pylab.plot(roomRatio, times)
    pylab.title('Time to clean 80% of various 400 area rooms with 2 robots')
    pylab.xlabel('Ratio of Width to Height')
    pylab.ylabel('Time (steps)')
    pylab.show()

#showPlot2()

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        #Choose new direction
        self.setRobotDirection(getRandomDirection())
        
        #Get position after movement
        newPosition = self.position.getNewPosition(self.getRobotDirection(), self.speed)
        
        #while new position outside room, choose new direction and get a new position
        while not self.room.isPositionInRoom(newPosition):
			self.setRobotDirection(getRandomDirection())
			newPosition = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        
        #Set new Position
        self.setRobotPosition(newPosition)
        
        #Clean square in room
        self.room.cleanTileAtPosition(newPosition)

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    time_ratio = []
    
    #Build list of times
    for i in xrange(1,11):
		standard_time = runSimulation(i, 1, 20, 20, .8, 100, StandardRobot)
		random_walk_time = runSimulation(i, 1, 20, 20, .8, 100, RandomWalkRobot)
		time_ratio.append(random_walk_time/standard_time)
    
    pylab.plot(xrange(1,11), time_ratio)
    pylab.title('Ratio of time to clean 80% of a 20x20 room with various numbers of robots')
    pylab.xlabel('Number of Robots')
    pylab.ylabel('Ratio of Standard Robot Time to Random Walk Robot Time')
    pylab.show()

showPlot3()
