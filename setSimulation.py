from pymorse import Morse
from scripts import mapDef
from scripts import const

def main():
    with Morse() as morse:
        listRobots = morse.rpc("simulation", "list_robots")

        morse.robot2.teleport.translate(-3, 0, 0)
        morse.robot2.teleport.rotate(0, 0, 3.1415)

        for eachRobot in listRobots:
            currentRobot = getattr(morse, eachRobot)

            localMapCell = []

            for j in range(const.MAP_HEIGHT * const.MAP_WIDTH):
                cell = mapDef.MapCell()
                localMapCell.append(cell)
            
            localMap = mapDef.GlobalMap(localMapCell)

            setattr(currentRobot, "localMap", localMap)

if __name__ == "__main__":
    main()
