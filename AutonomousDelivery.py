from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

#import AuxAutonomousDelivery as aux
import math as m

# === CREATE ROBOT OBJECT
robot = Create3(Bluetooth("SONNY"))

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_REALIGNED = False
HAS_FOUND_OBSTACLE = False
HAS_ARRIVED = False

# === OTHER NAVIGATION VARIABLES
SENSOR2CHECK = 0
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
DESTINATION = (0, 300)
ARRIVAL_THRESHOLD = 5


# ==========================================================
# FAIL SAFE MECHANISMS
@event(robot.when_touched, [True, True])
async def when_button_touched(robot): 
    global HAS_COLLIDED
    await robot.set_lights(Robot.LIGHT_ON, Color(255,0,0))
    await robot.stop()
    HAS_COLLIDED = True

@event(robot.when_bumped, [True, True])
async def when_bumped(robot): 
    global HAS_COLLIDED
    await robot.set_lights(Robot.LIGHT_ON, Color(255,0,0))
    await robot.stop()
    HAS_COLLIDED = True

# ==========================================================

# === REALIGNMENT BEHAVIOR
async def realignRobot(robot):
    global DESTINATION
    global HAS_REALIGNED
    while not HAS_REALIGNED: 
        #print("getting angle")
        #print(await robot.get_position())
        x  = (await robot.get_position()).x
        y = (await robot.get_position()).y 
        #print(x)
        #print(y)
        angle = getAngleToDestination((x,y), DESTINATION)
        #print("angle gotten")
        await robot.turn_right(getCorrectionAngle((await robot.get_position()).heading) + angle)
        HAS_REALIGNED = True


# === MOVE TO GOAL
async def moveTowardGoal(robot):
    global HAS_FOUND_OBSTACLE, IR_ANGLES, SENSOR2CHECK, HAS_ARRIVED
    pos = await robot.get_position()
    HAS_ARRIVED = checkPositionArrived((pos.x, pos.y), DESTINATION, ARRIVAL_THRESHOLD)
    while HAS_ARRIVED == False and HAS_COLLIDED == False:
        #print("running movetowardgoal") 
        #print("working")
        await robot.set_wheel_speeds(15,15)
        proxList = (await robot.get_ir_proximity()).sensors
        #print(proxList)
        aTup = getMinProxApproachAngle(proxList, IR_ANGLES)
        #print("done")
        #HAS_ARRIVED = checkPositionArrived(await robot.get_position(), DESTINATION, ARRIVAL_THRESHOLD)
        #print(aTup)
        #print(aTup[0])
        pos = await robot.get_position()
        HAS_ARRIVED =  checkPositionArrived((pos.x, pos.y), DESTINATION, ARRIVAL_THRESHOLD)
        #print("HAS ARRIVED IS {}".format(HAS_ARRIVED))
        if aTup[0] < 20: 
            await robot.set_wheel_speeds(0,0) 
            (minProx , minAngle) = getMinProxApproachAngle((await robot.get_ir_proximity()).sensors, IR_ANGLES)
            #print("ok")
            #print((await robot.get_position()).heading)
            if minAngle >0: 

                turnAngle = minAngle - 90
            else: 
                turnAngle = minAngle + 90
            #print("heading found")
            
            #print(turnAngle)

            await robot.turn_right(turnAngle)
            (minProx , minAngle) = getMinProxApproachAngle((await robot.get_ir_proximity()).sensors, IR_ANGLES)
            SENSOR2CHECK = minAngle
            #print("THIS IS SENSOR: {}".format(SENSOR2CHECK))
            HAS_FOUND_OBSTACLE = True
            await followObstacle(robot)
    #print("HAS ARRIVED IS {}".format(HAS_ARRIVED))
    await robot.stop()
            


# === FOLLOW OBSTACLE
async def followObstacle(robot):
    global HAS_FOUND_OBSTACLE, HAS_REALIGNED, SENSOR2CHECK, HAS_ARRIVED
    while HAS_FOUND_OBSTACLE: 
        await robot.set_wheel_speeds(4,4)
        #print("moving")
        irReadingsList = (await robot.get_ir_proximity()).sensors
        #print("here")
        #print("Sensor reading: {}".format(irReadingsList[IR_ANGLES.index(SENSOR2CHECK)]))
        prox = 4095/(irReadingsList[IR_ANGLES.index(SENSOR2CHECK)]+1)
        #print("THIS IS PROX:{} ".format(prox))
        if prox < 20: 
            if IR_ANGLES[IR_ANGLES.index(SENSOR2CHECK)] < 20: 
                await robot.turn_right(3)
            else: 
                await robot.turn_right(-3)
        elif prox > 100: 
            HAS_FOUND_OBSTACLE = False
            HAS_REALIGNED = False
            await robot.set_wheel_speeds(0,0)
            await robot.move(50)
            await realignRobot(robot)
            



# === NAVIGATION TO DELIVERY
@event(robot.when_play)
async def makeDelivery(robot):
    global HAS_ARRIVED, HAS_COLLIDED, HAS_REALIGNED, HAS_FOUND_OBSTACLE
    global DESTINATION, ARRIVAL_THRESHOLD, IR_ANGLES, SENSOR2CHECK
    await robot.reset_navigation()
    while HAS_ARRIVED == False and HAS_COLLIDED == False:
        #print("moving")
        pos = await robot.get_position()
        HAS_ARRIVED =  checkPositionArrived((pos.x, pos.y), DESTINATION, ARRIVAL_THRESHOLD)
        #print("HAS ARRIVED IS {}".format(HAS_ARRIVED))
        await moveTowardGoal(robot)
    else:
        if HAS_ARRIVED: 
            await robot.set_lights(Robot.LIGHT_SPIN,Color(0,255,0))
            #print("HAS ARRIVED IS {}".format(HAS_ARRIVED))
            await robot.set_wheel_speed(0,0)
            await robot.stop()
        else:
            await robot.set_lights(Robot.LIGHT_SPIN,Color(255,0,0))
            #print("HAS ARRIVED IS {}".format(HAS_ARRIVED))
            await robot.set_wheel_speed(0,0)
            await robot.stop()
            


        """
        if HAS_COLLIDED: 
            await robot.set_wheel_speeds(0,0)
            await robot.set_lights(Robot.LIGHT_ON, Color(255,0,0))
        """




# start the robot
robot.play()


def getCorrectionAngle(heading):
    if heading != 90: 
        return m.trunc(heading - 90)


def getAngleToDestination(current_position,destination):
    if destination[0] > current_position[0]: 
        a = m.degrees(m.atan2(destination[0] - current_position[0], destination[1]- current_position[1]))
        return m.trunc(a)
    elif destination[0] < current_position[0]: 
        a = m.degrees(m.atan2(destination[0] - current_position[0], destination[1]- current_position[1]))
        return m.trunc(a)
    

def getMinProxApproachAngle(readings, angles):
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

def checkPositionArrived(current_position, destination, threshold):
    distance = m.sqrt((destination[1]- current_position[1])**2 + (destination[0] - current_position[0])**2)
    return distance <= threshold
