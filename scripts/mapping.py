from pymorse import Morse
import const
import mapDef
import math

simMapCell = []
for i in range(0, const.MAP_HEIGHT * const.MAP_WIDTH):
    simMapCell[i] = mapCell(0.5, 0.0, 0, -1)

simGlobalMap = globalMap(0, 0, 0, 0, simMapCell)

def getSickRangeList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['range_list']

def getSickPointList(sickStream):
    sickSensor = sickStream.get()
    return sickSensor['point_list']

def refreshGrid(posX, posY, angLaser, thetaAngle, idRobot):
    borderLeft = borderRight = borderSup = borderInf = 0
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
                xL = math.cos(angLase[i] + thetaAngle) * (rangeLaser[i] / const.RESL) + posX
                yL = math.sin(angLase[i] + thetaAngle) * (rangeLaser[i] / const.RESL) + posY

            else:
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

            mapDef.setGlobalMap(simGlobalMap, borderLeft, borderRight, borderInf, borderSup)

def main():
