from pymorse import Morse
import const
import mapDef
import math
import avoidObs

simMapCell = []
for i in range(const.MAP_HEIGHT * const.MAP_WIDTH):
    mapObj = mapDef.MapCell()
    simMapCell.append(mapObj)

angLaser = [(math.pi / 2) * (-1)]

for count in range(1, 361):
    aux = angLaser[count - 1] + 0.00872
    angLaser.append(aux)

#Global map 
simGlobalMap = mapDef.GlobalMap(simMapCell)

def stopRobot(idRobot):
    motion = idRobot.motion
    v_w = {"v": 0, "w": 0}
    motion.publish(v_w)
    print("Robot stopped.")

def getSickRangeList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['range_list']

def getSickPointList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['point_list']

def getPoseYaw(poseStream):
    robotYaw = poseStream.get()
    return robotYaw['yaw']

def getPosePositionX(poseStream):
    robotPositionX = poseStream.get()
    return robotPositionX['x']

def getPosePositionY(poseStream):
    robotPositionX = poseStream.get()
    return robotPositionX['y']

def printOccupancyGridMap(globalMap, mapWidth, mapHeight):
    mapFile = open('occupancy_grid_map', 'w')
    for i in range(mapWidth * mapHeight):
        if ((i + 1) % (mapWidth + 1) == 0):
            mapFile.write("\n")

        mapFile.write("%.2f " % globalMap.cellMap[i].occupancyGrid)
    mapFile.close()

def printVisitMap(globalMap, mapWidth, mapHeight):
    mapFile = open('visit_map', 'w')
    for i in range(mapWidth * mapHeight):
        if ((i + 1) % (mapWidth + 1) == 0):
            mapFile.write("\n")

        mapFile.write("%i " % globalMap.cellMap[i].visit)
    mapFile.close()

def refreshGrid(idRobot, globalMap, angLaser): 
    #posX and posY are the coordinates of the robot;
    #thetaAngle is the angle (radians) of the robot relative to the world

    borderLeft = borderRight = borderSup = borderInf = 0
    #Borders of each robots' map
    rangeLaser = getSickRangeList(idRobot.sick)
    rangePoint = getSickPointList(idRobot.sick)

    thetaAngle = getPoseYaw(idRobot.pose)
    posX = getPosePositionX(idRobot.pose)
    posY = getPosePositionY(idRobot.pose)

    #print("(Not converted) X = %i, Y = %i" % (posX, posY))
        
    #Converting the world's coordinates to map's coordinate
    posX = int((posX + (const.HALF_REALMAP_WIDTH))  / const.RESL)
    posY = int((posY + (const.HALF_REALMAP_HEIGHT)) / const.RESL)

    for i in range(const.FIRST_LASER, const.LAST_LASER + 1):
        if rangeLaser[i] < (const.RANGE_MAX * const.RANGE_LIMIT):
            rateOC = 0.9
        else:
            rateOC = 0.48

        #Defining the points of laser detection
        xL = rangePoint[i][const.X_COORD]
        yL = rangePoint[i][const.Y_COORD]

        yL = yL * (-1)
        #Adjusting the map's borders
        #if ((xL == 0) and (yL == 0) and (zL == 0)):

        xL = ((math.cos(angLaser[i] + thetaAngle) * rangeLaser[i]) / const.RESL) + posX
        yL = ((math.sin(angLaser[i] + thetaAngle) * rangeLaser[i]) / const.RESL) + posY

        #else:
        #    xL = xL / const.RESL
        #    yL = yL / const.RESL

        if (xL < 0): xL = 0
        if (xL > const.MAP_WIDTH): xL = const.MAP_WIDTH
        if (yL < 0): yL = 0
        if (yL > const.MAP_HEIGHT): yL = const.MAP_HEIGHT

        if (borderLeft > xL): borderLeft = xL
        if (borderRight < xL): borderRight = xL
        if (borderSup < yL): borderSup = yL
        if (borderInf > yL): borderInf = yL

        if (borderLeft < 0): xL = borderLeft = 0
        if (borderRight > const.MAP_WIDTH): xL = borderRight = const.MAP_WIDTH
        if (borderSup > const.MAP_HEIGHT): yL = borderSup = const.MAP_HEIGHT
        if (borderInf < 0): yL = borderInf = 0

        globalMap.setGlobalMapBorders(borderLeft, borderRight, borderInf, borderSup) 

        deltaX = abs(xL - posX)
        deltaY = abs(yL - posY)

        #deltaX, deltaY, sX, sY, error, error2 are variables used to travel the map's cells
        #Using Bresenhan's Line Algorithm
        if (xL < posX): sX = 1
        else: sX = -1

        if (yL < posY): sY = 1
        else: sY = -1

        error = deltaX - deltaY

        while True:
            #print("xL = %i, yL = %i" % (int(xL), int(yL)))
            auxOC = globalMap.getGlobalMapOccupancyGrid(int(xL), int(yL))
            globalMap.setGlobalMapOccupancyGrid(int(xL), int(yL), 1 - pow((1 + (rateOC / (1 - rateOC)) * ((1 - const.PRIORI) / const.PRIORI) * (auxOC / ((1 - auxOC) + 0.00001))), -1) + 0.00001)
            globalMap.setGlobalMapVisit(int(xL), int(yL))

            if (rateOC > 0.5):
                rateOC = 0.48
            else:
                rateOC = rateOC * 0.95

            if (abs(xL - posX) <= 2) and (abs(yL - posY) <= 2):
                break

            error2 = 2 * error

            if (error2 > (-1) * deltaY):    
                error = error - deltaY
                xL = xL + sX

            if (error2 < deltaX):
                error = error + deltaX
                yL = yL + sY

def main():
    with Morse() as morse:
        #Returns the list of robots used in the simulation
        listRobots = morse.rpc('simulation', 'list_robots')
        #print(angLaser)

        motion1 = morse.robot1.motion
        sick1 = morse.robot1.sick

        iterations =  decision = 0
        while iterations < 100:
            print("Iteration: %i" % iterations)
            iterations = iterations + 1
            avoidObs.navigate(morse.robot1, sick1, motion1, decision)
            refreshGrid(morse.robot1, simGlobalMap, angLaser)
        
        stopRobot(morse.robot1)
        print("Simulation complete.")
        
        printOccupancyGridMap(simGlobalMap, const.MAP_WIDTH, const.MAP_HEIGHT)
        printVisitMap(simGlobalMap, const.MAP_WIDTH, const.MAP_HEIGHT)

        print("Maps generated for %i iterations." % iterations)

if __name__ == "__main__":
    main()
