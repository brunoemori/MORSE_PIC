import const
#Direction is defined probabilistically by the pheromone ratio on the cell
#So, the robot is more likely to move to the cell which has less pheromone
#But this doesn't means that the robot will ALWAYS take the lesser pheromone ratio cell
#The lesser pheromone quantity, the higher are the chances to to that cella

class RouletteWheel:
    def __init__(dirInRad):
        self.qPheromone = 0
        self.complementPheromone = 0
        self.direction = dirInRad
        self.accPercent = 0

    def setPheromone(qPheromone):
        self.qPheromone = qPheromone
        self.complementPheromone = 1 - qPheromone

    def setAccPercent(accPercert):
        self.accPercent = accPercent

def quickSort(listNum, start, end):
    if (start < end):
        pivot = partition(listNum, start, end)
        quickSort(listNum, start, pivot - 1)
        quickSort(listNum, pivot + 1, end)
    return listNum

def partition(listNum, start, end):
    pivot = listNum[start]
    leftMark = start + 1
    rightMark = end

    flag = False
    while (not flag):
        while ((leftMark <= rightMark) and (listNum[leftMark] <= pivot)):
            leftMark = leftMark + 1
        while ((listNum[rightMark] >= pivot) and (rightMark >= leftMark)):
            rightMark = rightMark - 1
        
        if (rightMark < leftMark):
            flag = True
        else:
            (listNum[leftMark], listNum[rightMark]) = (listNum[rightMark], listNum[leftMark])

    (listNum[start], listNum[rightMark]) = (listNum[rightMark], listNum[start])
    return rightMark

arrayDecision = [RouletteWheel((math.pi / 2) * (-1))]

for count in range(const.LAST_LASER + 1):
    aux = arrayDecision[count] + const.DIST_LASER
    arrayDecision.append(aux)

def getSickRangeList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['range_list']

def navigate(robot, globalMap):
    rangeLaser = getSickRangeList(robot.sick)

    for i in range(const.LAST_LASER + 1):

        xL = ((math.cos(angLaser[i] + thetaAngle) * rangeLaser[i]) / const.RESL) + posX
        yL = ((math.sin(angLaser[i] + thetaAngle) * rangeLaser[i]) / const.RESL) + posY

        pheromoneRatio = globalMap.getGlobalMapPheromone(int(xL), int(yL))
        arrayDecision[i].setPheromone(pheromoneRatio)

