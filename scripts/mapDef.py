import const

class mapCell:
    def __init__(self):
        self.occupancyGrid = 0.5
        self.qPheromone = 0.0
        self.rPath = 0
        self.visit = -1

class globalMap:
    def __init__(self, cellMap):
        self.borderLeft = 0
        self.borderRight = 0
        self.borderSup = 0
        self.borderInf = 0
        self.cellMap = cellMap

    def setGlobalMapBorders(self, borderLeft, borderRight, borderSup, borderInf):
        self.borderLeft = borderLeft
        self.globalMap.borderRight = borderRight
        self.globalMap.borderSup = borderSup
        self.globalMap.borderInf = borderInf

    def setGlobalMapOccupancyGrid(self, x, y, prob):
        if ((x >= 0) and (y >= 0) and (x < const.MAP_WIDTH) and (y < const.MAP_HEIGHT)):
            self.cellMap[(y * const.MAP_WIDTH) + x].occupancyGrid = prob
            return 0
        else:
            return -1

    def getGlobalMapOccupancyGrid(globalMap, x, y):
        auxOccupancyGrid = globalMap.cellMap[(y * const.MAP_WIDTH) + x].occupancyGrid
        return auxOccupancyGrid

    def setGlobalMapVisit(self, x, y):
        if ((x >= 0) and (y >= 0) and (x < const.MAP_WIDTH) and (y < const.MAP_HEIGHT)):
            self.cellMap[(y * const.MAP_WIDTH) + x].visit = 1
            return 0
        else:
            return -1


        

