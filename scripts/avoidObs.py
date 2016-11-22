from pymorse import Morse
import time

def isCloseRight(sick_stream):
    listRange = sick_stream.get()
    rangeValues = listRange['range_list']
    for i in range(120, 180):
        if rangeValues[i] < 3:
            return True
        else:
            return False

def isCloseLeft(sick_stream):
    listRange = sick_stream.get()
    rangeValues = listRange['range_list']
    for i in range(240, 180, -1):
        if rangeValues[i] < 3:
            return True
        else:
            return False

def isCloseFront(sick_stream):
    listRange = sick_stream.get()
    rangeValues = listRange['range_list']
    for i in range(150, 211):
        if rangeValues[i] < 2:
            return True
        else:
            return False

def getDir(sick_stream):
    listRange = sick_stream.get()
    rangeValues = listRange['range_list']
    distRay = listRange[0]
    dirPos = 0
    for i in rangeValues:
        if distRay < listRange[i]:
            distRay = listRange[i]
            dirPos = i
    return i

def main():
    with Morse() as morse:
        motion = morse.robot1.motion
        robotSick = morse.robot1.sick
        decision = 0 #0 = Right, 1 = Left
        while True:
            sensorRight = isCloseRight(robotSick)
            sensorLeft = isCloseLeft(robotSick)
            sensorFront = isCloseFront(robotSick)
            if sensorFront:
                if sensorRight:
                    v_w = {"v": -1, "w": 0.7}
                elif sensorLeft: 
                    v_w = {"v": -1, "w": -0.7}
                elif decision == 0:
                    v_w = {"v": 1, "w": -0.7}
                    decision = 1
                elif decision == 1:
                    v_w = {"v": 1, "w": 0.7}
                    decision = 0
            elif sensorRight:
                v_w = {"v": 1, "w": 0.7}
            elif sensorLeft:
                v_w = {"v": 1, "w": -0.7}
            else:
                v_w = {"v": 1, "w": 0}
            motion.publish(v_w)

if __name__ == "__main__":
    main()
