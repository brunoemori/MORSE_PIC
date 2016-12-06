import const
import math

class MapCell:
    def __init__(self):
        self.occupancyGrid = 0.5
        self.qPheromone = 0.0
        self.rPath = 0
        self.visit = -1

class GlobalMap:
    def __init__(self, cellMap):
        self.borderLeft = 0
        self.borderRight = 0
        self.borderSup = 0
        self.borderInf = 0
        self.cellMap = cellMap

    def setGlobalMapBorders(self, borderLeft, borderRight, borderSup, borderInf):
        self.borderLeft = borderLeft
        self.borderRight = borderRight
        self.borderSup = borderSup
        self.borderInf = borderInf

    def getGlobalMapOccupancyGrid(globalMap, x, y):
        auxOccupancyGrid = globalMap.cellMap[((const.MAP_WIDTH - 1 - y) * const.MAP_WIDTH) + x].occupancyGrid
        return auxOccupancyGrid

    def setGlobalMapOccupancyGrid(self, x, y, prob):
        if ((x >= 0) and (y >= 0) and (x < const.MAP_WIDTH) and (y < const.MAP_HEIGHT)):
            self.cellMap[((const.MAP_WIDTH - 1 - y) * const.MAP_WIDTH) + x].occupancyGrid = prob


    def setGlobalMapVisit(self, x, y):
        if ((x >= 0) and (y >= 0) and (x < const.MAP_WIDTH) and (y < const.MAP_HEIGHT)):
            self.cellMap[((const.MAP_WIDTH - 1 - y) * const.MAP_WIDTH) + x].visit = 1

    def setGlobalMapRobotPath(self, x, y):
        if ((x >= 0) and (y >= 0) and (x < const.MAP_WIDTH) and (y < const.MAP_HEIGHT)):
            self.cellMap[((const.MAP_WIDTH - 1 - y) * const.MAP_WIDTH) + x].rPath = 1

    def setGlobalMapPheromone(self, posX, posY, xL, yL):
        if ((x >= 0) and (y >= 0) and (x < const.MAP_WIDTH) and (y < const.MAP_HEIGHT)):
            currentPhQuant = self.cellMap[((const.MAP_WIDTH - 1 - y) * const.MAP_WIDTH) + x].qPheromone
            intensityPh1 = exp(- (xL - posX) * (xL - posX) / const.DISP_RATE) * exp(- (y - posY) / DISP_RATE)
            remain = 1 - currentPhQuant

            intensityPh2 = intensityPh1 * remain
            self.cellMap[((const.MAP_WIDTH - 1 - y) * const.MAP_WIDTH) + x].qPheromone = currentQuant + intensityPh2

    def evaporatePheromon(self):
        for x in range(self.borderLeft, self.borderRight):
            for y in range(self.borderInf, self.borderSup):
                currentPhQuant = self.cellMap[((const.MAP_WIDTH - 1 - y) * const.MAP_WIDTH) + x].qPheromone
                self.cellMap[((const.MAP_WIDTH - 1 - y) * const.MAP_WIDTH) + x].qPheromone = (1 - const.EVAP_RATE) * currentPhQuant

