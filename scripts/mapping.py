from pymorse import Morse

def getSickRangeList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['range_list']

def getSickPointList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['point_list']

def remapGrid(posX, posY, thetaAngle, rangeLaser, angLaser, idRobot):
    for i in range(FIRST_LASER, FINAL_LASER):
        if rangeLaser[i] < RANGE_MAX * RANGE_LIMIT:
            rateOC = 0.9
        else:
            rateOC = 0.48

        thisRange = rangeLaser[i]
        thisAngle = angLaser[i]
