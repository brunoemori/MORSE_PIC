from pymorse import Morse

def printPos(pose):
    poseSensor = pose.get()
    print("I'm currently at X = %.0f, Y = %.0f, Z = %.0f" % (poseSensor['x'], poseSensor['y'], poseSensor['z']))

def getYaw(pose):
    poseSensor = pose.get()
    print("Yaw = %.2f" % poseSensor['yaw'])

def main():
    with Morse() as morse:
        printPos(morse.robot1.pose)
        getYaw(morse.robot1.pose)
            
main()
