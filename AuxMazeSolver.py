from collections import deque



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
print(mazeDict)
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

print(getRobotOrientation(361))
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
    finalList += [prevCell]
    for i in range(len(wallsAroundCell)):
        if wallsAroundCell[i]: 
            continue 
        elif not wallsAroundCell[i] and potentialNeighbors[i][0] in range(nXCells) and potentialNeighbors[i][1] in range(nYCells):  
            finalList += [potentialNeighbors[i]]
    return finalList

        

#print(getNavigableNeighbors([True, True, False], [(1,2),(2,1),(1,0),(0,1)], (0,1), 2, 2))
#print(getNavigableNeighbors([False, True, False], [(0,2),(1,3),(2,2),(1,1)], (1,1), 4, 4))


def updateMazeNeighbors(mazeDict, currentCell, navNeighbors):
    for (x,y) in mazeDict[currentCell]["neighbors"]: 
        if (x,y) not in navNeighbors: 
            mazeDict[(x,y)]["neighbors"].remove(currentCell)
    mazeDict[currentCell]["neighbors"] = navNeighbors
    return mazeDict
#print(updateMazeNeighbors({(0, 0): {'position': (0, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 1): {'position': (0, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 2): {'position': (0, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 3): {'position': (0, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (0, 4): {'position': (0, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 0): {'position': (1, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 1): {'position': (1, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 2): {'position': (1, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 3): {'position': (1, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (1, 4): {'position': (1, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 0): {'position': (2, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 1): {'position': (2, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 2): {'position': (2, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 3): {'position': (2, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (2, 4): {'position': (2, 4), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 0): {'position': (3, 0), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 1): {'position': (3, 1), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 2): {'position': (3, 2), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 3): {'position': (3, 3), 'neighbors': [], 'visited': False, 'cost': 0}, (3, 4): {'position': (3, 4), 'neighbors': [], 'visited': False, 'cost': 0}}, (2, 2), [(1, 2), (3, 2), (2, 1)]))



def getNextCell(mazeDict, currentCell):
    lowCost = 1000000
    lowCostNeighbor = None
    for neighbor in mazeDict[currentCell]["neighbors"]:
        if mazeDict[neighbor]["visited"] == False and mazeDict[neighbor]["cost"] < lowCost:
            lowCost = mazeDict[neighbor]["cost"]
            lowCostNeighbor = neighbor 
            
    if lowCostNeighbor  == None: 
        for neighbor in mazeDict[currentCell]["neighbors"]:
            if mazeDict[neighbor]["cost"] < lowCost:
                lowCost = mazeDict[neighbor]["cost"]
                lowCostNeighbor = neighbor 


    return lowCostNeighbor

"""
mazeDict = {(0, 0): {'position': (0, 0),'neighbors': [(0, 1)], 'visited': True, 'cost': 0},
            (0, 1): {'position': (0, 1),'neighbors': [(0, 0), (1, 1)], 'visited': True, 'cost': 1},
            (1, 0): {'position': (1, 0), 'neighbors': [(1, 1)], 'visited': False, 'cost': 3},
            (1, 1): {'position': (1, 1), 'neighbors': [(1, 0), (0, 1)], 'visited': False, 'cost': 2}}
currentCell = (0,1)
print(getNextCell(mazeDict, currentCell))

mazeDict = {(0, 0): {'position': (0, 0),'neighbors': [(0, 1)], 'visited': True, 'cost': 0},
            (0, 1): {'position': (0, 1),'neighbors': [(0, 0), (1, 1)], 'visited': False, 'cost': 1},
            (1, 0): {'position': (1, 0), 'neighbors': [(1, 1)], 'visited': False, 'cost': 3},
            (1, 1): {'position': (1, 1), 'neighbors': [(1, 0), (0, 1)], 'visited': True, 'cost': 2}}
currentCell = (1,1)
print(getNextCell(mazeDict, currentCell))
"""


def checkCellArrived(currentCell, destination):
    return currentCell == destination
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
"""
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

"""
This function prints the information from the dictionary as
a grid and can help you troubleshoot your implementation.
"""
def printMazeGrid(mazeDict, nXCells, nYCells, attribute):
    for y in range(nYCells - 1, -1, -1):
        row = '| '
        for x in range(nXCells):
            cell_value = mazeDict[(x, y)][attribute]
            row += '{} | '.format(cell_value)
        print(row[:-1])
