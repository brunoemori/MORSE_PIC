from scripts import const
#Direction is defined probabilistically by the pheromone ratio on the cell
#So, the robot is more likely to move to the cell which has less pheromone
#But this doesn't means that the robot will ALWAYS take the lesser pheromone ratio cell
#The lesser pheromone quantity, the higher are the chances to to that cell

def getSickRangeList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['range_list']

def navigate(robot, globalMap):
    rangeLaser = getSickRangeList(robot.sick)
    pheromoneArray = []

    for i in range(const.FIRST_LASER * const.LAST_LASER + 1):

        xL = ((math.cos(angLaser[i] + thetaAngle) * rangeLaser[i]) / const.RESL) + posX
        yL = ((math.sin(angLaser[i] + thetaAngle) * rangeLaser[i]) / const.RESL) + posY

        pheromoneCell = globalMap.getGlobalMapPheromone(int(xL), int(yL))

        pheromoneArray.append(pheromoneCell)


        

