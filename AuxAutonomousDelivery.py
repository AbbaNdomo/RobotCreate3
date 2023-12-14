
import math as m

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
