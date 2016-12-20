from scripts import const
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

    def getGlobalMapVisit(globalMap, x, y):
        auxVisit = globalMap.cellMap[((const.MAP_WIDTH - 1 - y) * const.MAP_WIDTH) + x].visit
        return auxVisit

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
        if ((xL >= 0) and (yL >= 0) and (xL < const.MAP_WIDTH) and (yL < const.MAP_HEIGHT)):
            currentPhQuant = self.cellMap[((const.MAP_WIDTH - 1 - yL) * const.MAP_WIDTH) + xL].qPheromone
            intensityPh1 = math.exp(- (xL - posX) * (xL - posX) / const.DISP_RATE) * math.exp(- (yL - posY) * (yL - posY) / const.DISP_RATE)
            remain = 1 - currentPhQuant

            intensityPh2 = intensityPh1 * remain
            self.cellMap[((const.MAP_WIDTH - 1 - yL) * const.MAP_WIDTH) + xL].qPheromone = currentPhQuant + intensityPh2

    def evaporatePheromone(self):
        for i in range(const.MAP_WIDTH * const.MAP_HEIGHT):
            currentPhQuant = self.cellMap[i].qPheromone
            self.cellMap[i].qPheromone = (1 - const.EVAP_RATE) * currentPhQuant

    def resetGlobaMapVisit(self):
        for i in range(const.MAP_WIDTH * const.MAP_HEIGHT):
            self.cellMap[i].visit = -1

