from pymorse import Morse
import const
import mapDef
import math

simMapCell = []
mapObj = mapDef.mapCell()
for i in range(const.MAP_HEIGHT * const.MAP_WIDTH):
    simMapCell.append(mapObj)

#Global map 
simGlobalMap = mapDef.globalMap(simMapCell)

def getSickRangeList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['range_list']

def getSickPointList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['point_list']

def refreshGrid(posX, posY, angLaser, thetaAngle, idRobot): 
    #posX and posY are the coordinates of the robot;
    #thetaAngle is the angle (radians) of the robot relative to the world

    borderLeft = borderRight = borderSup = borderInf = 0
    #Borders of each robots' map
    with Morse() as morse:
        rangeLaser = getSickRangeList
        rangePoint = getSickPointList
        for i in range(const.FIRST_LASER, const.FINAL_LASER + 1):

            if rangeLaser[i] < (const.RANGE_MAX * const.RANGE_LIMIT):
                rateOC = 0.9
            else:
                rateOC = 0.48

            #Defining the points of laser detection
            xL = rangePoint[i][const.X_COORD]
            yL = rangePoint[i][const.Y_COORD]
            zL = rangePoint[i][const.Z_COORD]

            #Adjusting the map's borders
            tempAng = angLaser[i]
            if ((xL == 0) and (yL == 0) and (zL == 0)):
                xL = ((math.cos(angLaser[i] + thetaAngle) * rangeLaser[i]) / const.RESL) + posX # 
                yL = ((math.sin(angLaser[i] + thetaAngle) * rangeLaser[i]) / const.RESL) + posY #
            else:
                xL = xL / const.RESL
                yL = yL / const.RESL

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

            simGlobalMap = mapDef.setGlobalMap(borderLeft, borderRight, borderInf, borderSup)

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
                auxOC = mapDef.getGlobalMapOccupancyGrid(simGlobalMap, xL, yL)
                simGlobalMap = mapDef.setGlobalMapOccupancyGrid(xL, yL, 1 - pow((1 + (rateOC / (1 - rateOC)) * ((1 - const.PRIORI) / const.PRIORI) * (auxOC / ((1 - auxOC) + 0.00001))), -1) + 0.00001)
                simGlobalMap = mapDef.setGlobalMapVisit(xL, yL)

                if (rateOC > 0.5):
                    rateOC = 0.48
                else:
                    rateOC = rateOC * 0.95

                if (xL == posX) and (yL == posY):
                    break

                error2 = 2 * error

                if (error2 > (-1) * deltaY):
                    error = error - deltaY
                    xL = xL + sX

                if (erro2 < deltaX):
                    error = error + deltaX
                    yL = yL + sY

def main():
    
