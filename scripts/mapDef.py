class simCell:
    def __init__(self, occupancyGrid, qPheromone, rPath, visit):
        self.occupancyGrid = occupancyGrid
        self.qPheromone = qPheromone
        self.rPath = rPath
        self.visit = visit

class globalMap:
    def __init__(self, borderLeft, borderRight, borderSup, borderInf, cellMap):
        self.borderLeft = borderLeft
        self.borderRight = borderRight
        self.borderSup = borderSup
        self.borderInf = borderInf
        self.cellMap = cellMap

        

