from pymorse import Morse
from scripts import const
from scripts import mapDef
from scripts import avoidObs
from scripts import localMaps
from concurrent.futures import ThreadPoolExecutor
import math
import time

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

def getSickRangeList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['range_list']

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
    mapFile = open('occupancy_grid_map.txt', 'w')
    for i in range(mapWidth * mapHeight):
        mapFile.write("%.2f " % globalMap.cellMap[i].occupancyGrid)

        if ((i + 1) % mapWidth == 0):
            mapFile.write("\n")

    mapFile.close()

def printVisitMap(globalMap, mapWidth, mapHeight):
    mapFile = open('visit_map.txt', 'w')
    for i in range(mapWidth * mapHeight):
        mapFile.write("%i " % globalMap.cellMap[i].visit)

        if ((i + 1) % mapWidth == 0):
            mapFile.write("\n")

    mapFile.close()

def printPathMap(globalMap, mapWidth, mapHeight):
    mapFile = open('path_map.txt', 'w')
    for i in range(mapWidth * mapHeight):
        mapFile.write("%i " % globalMap.cellMap[i].rPath)

        if ((i + 1) % mapWidth == 0):
            mapFile.write("\n")

def printPheromoneMap(globalMap, mapWidth, mapHeight):
    mapFile = open('pheromone_map.txt', 'w')
    for i in range(mapWidth * mapHeight):
        mapFile.write("%.5f " % globalMap.cellMap[i].qPheromone)

        if ((i + 1) % mapWidth == 0):
            mapFile.write("\n")

def refreshGrid(idRobot, globalMap, angLaser): 
    #posX and posY are the coordinates of the robot;
    #thetaAngle is the angle (radians) of the robot relative to the world

    borderLeft = borderRight = borderSup = borderInf = 0
    #Borders of each robots' map
    rangeLaser = getSickRangeList(idRobot.sick)

    thetaAngle = getPoseYaw(idRobot.pose)
    posX = getPosePositionX(idRobot.pose)
    posY = getPosePositionY(idRobot.pose)

    #print("(Not converted) X = %i, Y = %i" % (posX, posY))
        
    #Converting the world's position to map's position
    posX = int((posX + (const.HALF_REALMAP_WIDTH))  / const.RESL)
    posY = int((posY + (const.HALF_REALMAP_HEIGHT)) / const.RESL)

    for i in range(const.FIRST_LASER, const.LAST_LASER + 1):
        if rangeLaser[i] < (const.RANGE_MAX * const.RANGE_LIMIT):
            rateOC = 0.9
        else:
            rateOC = 0.48

    #Adjusting the world's coordinates to the global map's coordinates
        xL = ((math.cos(angLaser[i] + thetaAngle) * rangeLaser[i]) / const.RESL) + posX
        yL = ((math.sin(angLaser[i] + thetaAngle) * rangeLaser[i]) / const.RESL) + posY
    
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

        globalMap.setGlobalMapBorders(int(borderLeft), int(borderRight), int(borderInf), int(borderSup))

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
            auxOC = globalMap.getGlobalMapOccupancyGrid(int(xL), int(yL))
            globalMap.setGlobalMapOccupancyGrid(int(xL), int(yL), 1 - pow((1 + (rateOC / (1 - rateOC)) * ((1 - const.PRIORI) / const.PRIORI) * (auxOC / ((1 - auxOC) + 0.00001))), -1) + 0.00001)
            
            if (globalMap.getGlobalMapVisit(int(xL),int(yL)) == -1):    
                globalMap.setGlobalMapPheromone(int(posX), int(posY), int(xL), int(yL))

            idRobot.localMap.setGlobalMapVisit(int(xL), int(yL))

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

def test(robot, globalMap, angLaser):
    i = 0
    while i < 10:
        pass

def robotMapping(robot, globalMap, angLaser):
    iteration = 0
    decision = 0
    while iteration < 100:
        print("Iteration of %s: %i." % (robot.name, iteration))
        iteration = iteration + 1
        sick = robot.sick
        motion = robot.motion
        pose = robot.pose

        decision = avoidObs.navigate(robot, decision)
        refreshGrid(robot, globalMap, angLaser)

        newPosX = getPosePositionX(pose)
        newPosY = getPosePositionY(pose)
        newPosX = int((newPosX + (const.HALF_REALMAP_WIDTH))  / const.RESL)
        newPosY = int((newPosY + (const.HALF_REALMAP_HEIGHT)) / const.RESL)
        simGlobalMap.setGlobalMapRobotPath(newPosX, newPosY)

        robot.localMap.resetGlobalMapVisit()

def main():
    with Morse() as morse:
<<<<<<< HEAD
        iterations = 100
        print("Simulation started...")
=======
        print("Simulation running...")
>>>>>>> fd659f348f4bbf85bb6c4bd45a4aa1891f32359a
        startingTime = time.time()
        #Returns the list of robots used in the simulation
        listRobots = morse.rpc('simulation', 'list_robots')

        localMaps.setLocalMaps(morse, listRobots)

<<<<<<< HEAD
        executor = ThreadPoolExecutor(max_workers=4)
        process1 = executor.submit(robotMapping, morse.robot1, simGlobalMap, angLaser)
        process2 = executor.submit(robotMapping, morse.robot2, simGlobalMap, angLaser)

        executor.shutdown()
=======
        iterations = 0
        decision = 0
        while iterations < 100:
            print("Iteration: %i" % iterations)
            iterations = iterations + 1

            #Iterate for each robot in the simulation
            for robotName in listRobots:
                currentRobot = getattr(morse, robotName) #Returns the robot object by its name on the list
                sick = currentRobot.sick
                motion = currentRobot.motion
                pose = currentRobot.pose
                decision = avoidObs.navigate(currentRobot, decision)

                newPosX = getPosePositionX(pose)
                newPosY = getPosePositionY(pose)
                newPosX = int((newPosX + (const.HALF_REALMAP_WIDTH))  / const.RESL)
                newPosY = int((newPosY + (const.HALF_REALMAP_HEIGHT)) / const.RESL)
                simGlobalMap.setGlobalMapRobotPath(newPosX, newPosY)

                pool = Pool(4)
                mapping_async = pool.apply_async(refreshGrid, [currentRobot, simGlobalMap, angLaser])
                pool.close()
                pool.join()

                #refreshGrid(currentRobot, simGlobalMap, angLaser)
                #stopRobot(currentRobot)
                simGlobalMap.evaporatePheromone()
                #simGlobalMap.resetGlobalMapVisit()
                currentRobot.localMap.resetGlobalMapVisit()
                
>>>>>>> fd659f348f4bbf85bb6c4bd45a4aa1891f32359a

        for robotName in listRobots:
            currentRobot = getattr(morse, robotName)
            stopRobot(currentRobot)

        print("--------------- SIMULATION SUMMARY ---------------")
        print("Simulation complete.")
        print("Robots used in simulation: ", end = "")
        print(listRobots)

        simulationTimeSeconds = time.time() - startingTime
        simulationTimeMinutes = simulationTimeHours = 0
        while (simulationTimeSeconds >= 60):
            simulationTimeSeconds = simulationTimeSeconds - 60
            simulationTimeMinutes = simulationTimeMinutes + 1
        
        while (simulationTimeMinutes >= 60):
            simulationTimeMinutes = simulationTimeMinutes - 60
            simulationTimeHours = simulationTimeHours + 1

        print("Simulation iterations: %i" % iterations)
        print("Simulation time: %i hour(s), %i minute(s) and  %.2f second(s).\n\n" % (simulationTimeHours, simulationTimeMinutes, simulationTimeSeconds))

        printOccupancyGridMap(simGlobalMap, const.MAP_WIDTH, const.MAP_HEIGHT)
        printVisitMap(simGlobalMap, const.MAP_WIDTH, const.MAP_HEIGHT)
        printPathMap(simGlobalMap, const.MAP_WIDTH, const.MAP_HEIGHT)
        printPheromoneMap(simGlobalMap, const.MAP_WIDTH, const.MAP_HEIGHT)

        print("Files generated: occupancy_grid.txt, visit_map.txt, path_map.txt, pheromone_map.txt\n")
        print("--------------- END ---------------")

if __name__ == "__main__":
    main()
