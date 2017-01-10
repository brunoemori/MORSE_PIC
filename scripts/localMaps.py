from pymorse import Morse
from scripts import mapDef
from scripts import const

def setLocalMaps(morse, simulationList):
    for eachRobot in simulationList:
        currentRobot = getattr(morse, eachRobot)

        localMapCell = []

        for j in range(const.MAP_HEIGHT * const.MAP_WIDTH):
            cell = mapDef.MapCell()
            localMapCell.append(cell)

        localMap = mapDef.GlobalMap(localMapCell)
        setattr(currentRobot, "localMap", localMap)
