class simMap:
    def __init__(self, occupancyGrid, qPheromone, rPath, visit):
        self.occupancyGrid = occupancyGrid
        self.qPheromone = qPheromone
        self.rPath = rPath
        self.visit = visit
