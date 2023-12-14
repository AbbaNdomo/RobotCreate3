from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
from collections import deque
import math as m
#import AuxMazeSolver as aux

def createMazeDict(nXCells, nYCells, cellDim):
    mazeDict = {}
    aDict = []
    for i in range(nXCells): 
        for j in range(nYCells): 
            mazeDict[(i,j)] = {}
            mazeDict[(i,j)]["position"] = (cellDim * i , cellDim * j)
            mazeDict[(i,j)]["neighbors"] = []
            mazeDict[(i,j)]["visited"] = False
            mazeDict[(i,j)]["cost"] = 0
    return mazeDict
"""
nXCells, nYCells, cellDim = 2, 2, 10
mazeDict = createMazeDict(nXCells, nYCells, cellDim)
#print(mazeDict)
"""


def addAllNeighbors(mazeDict, nXCells, nYCells):
# left first, front, right and back
    for (x,y) in mazeDict.keys():
            if x-1 in range(nXCells):
                mazeDict[(x,y)]["neighbors"] += [(x-1,y)]
            if y+1 in range(nYCells):
                mazeDict[(x,y)]["neighbors"] += [(x,y+1)]
            if x+1 in range(nXCells):
                mazeDict[(x,y)]["neighbors"] += [(x+1,y)]
            if y-1 in range(nYCells):
                mazeDict[(x,y)]["neighbors"] += [(x,y-1)]
    return mazeDict

#mazeDict = createMazeDict(2,2,10)

#print(addAllNeighbors(mazeDict, 2, 2))

"""
mazeDict = createMazeDict(nXCells, nYCells, cellDim)
mazeDict = addAllNeighbors(mazeDict, nXCells, nYCells)
"""


def getRobotOrientation(heading):
    if abs(heading - 0) < abs(heading  - 360):
        dEast = abs(heading - 0)
    else: 
        dEast = abs(heading  - 360)
    dWest = abs(heading - 180)
    dNorth = abs(heading - 90)
    dSouth = abs(heading - 270)
    aList = [(dEast,"E"),(dWest, "W"),(dNorth, "N"),(dSouth, "S")]
    aList.sort()
    return aList[0][1]

#print(getRobotOrientation(361))
"""
print(getRobotOrientation(361))
print(getRobotOrientation(88.5))
"""

#[leftIndices, frontIndices, rightIndices, backIndices] 
def getPotentialNeighbors(currentCell, orientation):
    (x,y) = currentCell
    finalList = []
    if orientation == "N":
        leftInd = (x-1, y)
        rightInd = (x+1, y)
        frontInd = (x, y+1)
        backInd = (x, y-1)
    elif orientation == "S":
        leftInd = (x+1, y)
        rightInd = (x-1, y)
        frontInd = (x, y-1)
        backInd = (x, y+1)
    elif orientation == "E":
        leftInd = (x, y+1)
        rightInd = (x, y-1)
        frontInd = (x+1, y)
        backInd = (x-1, y)
    else: 
        leftInd = (x, y-1)
        rightInd = (x, y+1)
        frontInd = (x-1, y)
        backInd = (x+1, y)
    finalList += [leftInd, frontInd, rightInd, backInd]
    return finalList 

#print(getPotentialNeighbors((0,0),"E"))
#[(0, 1), (1, 0), (0, -1), (-1, 0)]
#getPotentialNeighbors((2,3),"S") 
#[(3, 3), (2, 2), (1, 3), (2, 4)]


"""
print(getPotentialNeighbors((0,1),"E"))
print(getPotentialNeighbors((2,3),"S"))
"""


def isValidCell(cellIndices, nXCells, nYCells):
    (x,y) = cellIndices
    return x in range(nXCells) and y in range(nYCells)


#print(isValidCell((3,3), 4, 5))
#print(isValidCell((1,2), 2, 2))



def getWallConfiguration(IR0,IR3,IR6,threshold):
    aList = [IR0,IR3,IR6]
    finalList = []
    for value in aList:
        finalList +=  [4095/(value + 1) <= threshold]
    return finalList
    


#print(getWallConfiguration(300, 200, 39, 100))
#print(getWallConfiguration(23, 800, 10, 100))



def getNavigableNeighbors(wallsAroundCell, potentialNeighbors, prevCell, nXCells, nYCells):
    finalList = []
    if not prevCell == None: 
        finalList += [prevCell]
        #print("This cell {} has been visited: {}".format(CURR_CELL,MAZE_DICT[CURR_CELL]["visited"]))

    for i in range(len(wallsAroundCell)):
        if wallsAroundCell[i]: 
            continue 
        elif not wallsAroundCell[i] and potentialNeighbors[i][0] in range(nXCells) and potentialNeighbors[i][1] in range(nYCells):  
            finalList += [potentialNeighbors[i]]
    return finalList

        

#print(getNavigableNeighbors([True, True, False], [(1,2),(2,1),(1,0),(0,1)], (0,1), 2, 2))
#print(getNavigableNeighbors([False, True, False], [(0,2),(1,3),(2,2),(1,1)], (1,1), 4, 4))


def updateMazeNeighbors(mazeDict, currentCell, navNeighbors):
    """
    FOR CELL IN MAZE DICT:
        IF CURRENT CELL IN MAZE DICT CELL NEIGHBORS:
            IF NOT CELL IS A NAV NEIGHBORS:
                REMOVE CURR CELL FROM MAZZE DICT CELL NEIGHROBS
    """
    
    
    for cell in mazeDict.keys():
        if currentCell in mazeDict[cell]["neighbors"]:
            if  cell not in navNeighbors: 
                mazeDict[cell]["neighbors"].remove(currentCell)
    
    """
    for (x,y) in mazeDict[currentCell]["neighbors"]: 
        if (x,y) not in navNeighbors: 
            mazeDict[(x,y)]["neighbors"].remove(currentCell)
    """
    mazeDict[currentCell]["neighbors"] = navNeighbors
    return mazeDict
#print(updateMazeNeighbors({(0, 0): {'position': (0, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 1): {'position': (0, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 2): {'position': (0, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 3): {'position': (0, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 4): {'position': (0, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 0): {'position': (1, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 1): {'position': (1, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 2): {'position': (1, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 3): {'position': (1, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 4): {'position': (1, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 0): {'position': (2, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 1): {'position': (2, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 2): {'position': (2, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 3): {'position': (2, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 4): {'position': (2, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 0): {'position': (3, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 1): {'position': (3, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 2): {'position': (3, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 3): {'position': (3, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 4): {'position': (3, 4), 'neighbors': [], 'visited': False, 'cost': 0}}, (2, 2), [(1, 2), (3, 2), (2, 1)]))

def updateMazeCost(mazeDict, start, goal):
    for (i,j) in mazeDict.keys():
        mazeDict[(i,j)]["flooded"] = False
    queue = deque([goal])
    mazeDict[goal]['cost'] = 0
    mazeDict[goal]['flooded'] = True
    while queue:
        current = queue.popleft()
        current_cost = mazeDict[current]['cost']
        for neighbor in mazeDict[current]['neighbors']:
            if not mazeDict[neighbor]['flooded']:
                mazeDict[neighbor]['flooded'] = True
                mazeDict[neighbor]['cost'] = current_cost + 1
                queue.append(neighbor)
    return mazeDict

def getNextCell(mazeDict, currentCell):
    lowCost = 1000000
    lowCostNeighbor = None
    allVisited = False
    for neighbor in mazeDict[currentCell]["neighbors"]:
        if mazeDict[neighbor]["visited"] == False and mazeDict[neighbor]["cost"] < lowCost:
            lowCost = mazeDict[neighbor]["cost"]
            lowCostNeighbor = neighbor 
            
    if lowCostNeighbor  == None: 
        #print("THIS IS FOR IF ALL NAVIGABLE CELLS HAVE BEEN VISITED")
        lowCost = 1000000
        for neighbor in mazeDict[currentCell]["neighbors"]:
            if mazeDict[neighbor]["cost"] <= lowCost:
                lowCost = mazeDict[neighbor]["cost"]
                lowCostNeighbor = neighbor 


    return lowCostNeighbor



def checkCellArrived(currentCell, destination):
    return currentCell == destination

# === CREATE ROBOT OBJECT
robot = Create3(Bluetooth("SONNY"))

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_ARRIVED = False

# === BUILD MAZE DICTIONARY
N_X_CELLS = 3
N_Y_CELLS = 3
CELL_DIM = 50
MAZE_DICT = createMazeDict(N_X_CELLS, N_Y_CELLS, CELL_DIM)
MAZE_DICT = addAllNeighbors(MAZE_DICT, N_Y_CELLS, N_Y_CELLS)

# === DEFINING ORIGIN AND DESTINATION
PREV_CELL = None
START = (2,0)
CURR_CELL = START
DESTINATION = (0,2)
MAZE_DICT[CURR_CELL]["visited"] = True

# === PROXIMITY TOLERANCES
WALL_THRESHOLD = 100
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]


# ==========================================================
# FAIL SAFE MECHANISMS
@event(robot.when_touched, [True, True])
async def when_button_touched(robot): 
    global HAS_COLLIDED
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights(Robot.LIGHT_ON, Color(255,0,0))
    HAS_COLLIDED = True

@event(robot.when_bumped, [True, True])
async def when_bumped(robot): 
    global HAS_COLLIDED
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights(Robot.LIGHT_ON, Color(255,0,0))
    HAS_COLLIDED = True

# ==========================================================
# MAZE NAVIGATION AND EXPLORATION

# === NAVIGATE TO CELL
async def navigateToNextCell(robot, nextCell, orientation)      :
    global MAZE_DICT, PREV_CELL, CURR_CELL, CELL_DIM
    orientation = getRobotOrientation((await robot.get_position()).heading)
    potentialNeighborsList = getPotentialNeighbors(CURR_CELL, orientation)

    if nextCell in potentialNeighborsList: 
        i = potentialNeighborsList.index(nextCell)
        if i == 0: 
            await robot.turn_right(-90)
        elif i == 1: 
            pass
        elif i == 2: 
            await robot.turn_right(90)
        elif i == 3: 
            await robot.turn_right(180)
        await robot.move(CELL_DIM)
        MAZE_DICT[CURR_CELL]["visited"] = True
        PREV_CELL = CURR_CELL
        CURR_CELL = nextCell
        

    


#def getWallConfiguration(IR0,IR3,IR6,threshold)

# === EXPLORE MAZE
@event(robot.when_play)
async def navigateMaze(robot):
    global HAS_COLLIDED, HAS_ARRIVED
    global PREV_CELL, CURR_CELL, START, DESTINATION, IR_ANGLES
    global MAZE_DICT, N_X_CELLS, N_Y_CELLS, CELL_DIM, WALL_THRESHOLD
    (HAS_ARRIVED, HAS_COLLIDED) = (False, False)
    while HAS_ARRIVED == False and HAS_COLLIDED == False: 
        #(minAngle, minProx) = getMinProxApproachAngle( (await robot.get_ir_proximity()).sensors , IR_ANGLES)
        #print("STARTING")
        aList = []
        irReadingsList = (await robot.get_ir_proximity()).sensors
        #print(irReadingsList)
        for i in range(0,7,3):
            aList += [irReadingsList[i]]
            #print(aList)
        wallBoolList = getWallConfiguration(aList[0], aList[1], aList[2], WALL_THRESHOLD)       
        #print(wallBoolList)
        
        HAS_ARRIVED = checkCellArrived(CURR_CELL, DESTINATION)
        #print(HAS_ARRIVED)
        #print("current cell: {}, destination: {}".format(CURR_CELL, DESTINATION))
        if HAS_ARRIVED == True: 
            break 
        orientation = getRobotOrientation((await robot.get_position()).heading)

        potentialNeighborsList = getPotentialNeighbors(CURR_CELL, orientation)
        #print("This is potential neighbors {}".format(potentialNeighborsList))

        navigableNeighborsList = getNavigableNeighbors(wallBoolList, potentialNeighborsList, PREV_CELL, N_X_CELLS, N_Y_CELLS)   
        #print("This is navigable neighbors {}".format(navigableNeighborsList))
        newMazeDict = updateMazeNeighbors(MAZE_DICT, CURR_CELL, navigableNeighborsList)  
        newMazeDict = updateMazeCost(MAZE_DICT,START, DESTINATION)
        bestCellMove = getNextCell(MAZE_DICT,CURR_CELL)
        if isValidCell(bestCellMove, N_X_CELLS, N_X_CELLS) == True: 
            await navigateToNextCell(robot, bestCellMove, orientation)
        else: 
            #print("NEXT CELL IS NOT WITHIN BOUNDARIES")
            await robot.set_lights(Robot.LIGHT_ON, Color(255,0,0))

    if HAS_COLLIDED == True:
        await robot.set_lights(Robot.LIGHT_ON, Color(255,0,0))
        await robot.set_wheel_speed(0,0)
    elif HAS_ARRIVED == True: 
        await robot.set_lights(Robot.LIGHT_SPIN,Color(0,255,0))
        await robot.set_wheel_speed(0,0)
    #GET IR READINGS

    
    


# start the robot
robot.play()


"""
print(checkCellArrived((4,3), (4,3)))
print(checkCellArrived((6,7), (7,6)))
"""


"""
The following implementation of the Flood Fill algorithm is
tailored for maze navigation. It updates the movement cost for
each maze cell as the robot learns about its environment. As
the robot moves and discovers navigable adjacent cells, it
gains new information, leading to frequent updates in the
maze's data structure. This structure tracks the layout and
traversal costs. With each step and discovery, the algorithm
recalculates the cost to reach the destination, adapting to
newly uncovered paths. This iterative process of moving,
observing, and recalculating continues until the robot reaches
its destination, ensuring an optimal path based on the robot's
current knowledge of the maze.

def updateMazeCost(mazeDict, start, goal):
    for (i,j) in mazeDict.keys():
        mazeDict[(i,j)]["flooded"] = False
    queue = deque([goal])
    mazeDict[goal]['cost'] = 0
    mazeDict[goal]['flooded'] = True
    while queue:
        current = queue.popleft()
        current_cost = mazeDict[current]['cost']
        for neighbor in mazeDict[current]['neighbors']:
            if not mazeDict[neighbor]['flooded']:
                mazeDict[neighbor]['flooded'] = True
                mazeDict[neighbor]['cost'] = current_cost + 1
                queue.append(neighbor)
    return mazeDict


This function prints the information from the dictionary as
a grid and can help you troubleshoot your implementation.

def printMazeGrid(mazeDict, nXCells, nYCells, attribute):
    for y in range(nYCells - 1, -1, -1):
        row = '| '
        for x in range(nXCells):
            cell_value = mazeDict[(x, y)][attribute]
            row += '{} | '.format(cell_value)
        print(row[:-1])

    finalTup = ()
    proximityList = []
    minProx = 10000
    minAngle = 0
    for reading in readings: 
        prox = 4095/(reading+1)
        if prox < minProx: 
            minProx = prox
            minAngle =  angles[readings.index(reading)]
        proximityList += [prox]
    finalTup += (minProx, minAngle)
    return finalTup

    if destination[0] > current_position[0]: 
        a = m.degrees(m.atan2(destination[0] - current_position[0], destination[1]- current_position[1]))
        return m.trunc(a)
    elif destination[0] < current_position[0]: 
        a = m.degrees(m.atan2(destination[0] - current_position[0], destination[1]- current_position[1]))
        return m.trunc(a)
"""