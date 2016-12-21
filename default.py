from morse.builder import *
from scripts import const
from scripts import mapDef

#Defining robots
names = ["robot1", "robot2"]

for i in range(len(names)):
    robot = ATRV(names[i])

    #Defining components
    motion = MotionVW()

    teleport = Teleport()

    sick = Sick()
    sick.properties(laser_range = 10)
    sick.properties(scan_window = 180)
    sick.properties(resolution = 0.5)
    sick.properties(Visible_arc = True)

    pose = Pose()
    pose.translate(z = -0.10)

    robot.append(sick)
    robot.append(motion)
    robot.append(pose)
    robot.append(teleport)

    sick.add_interface('socket')
    motion.add_interface('socket')
    pose.add_interface('socket')
    teleport.add_interface('socket')

'''
    if (names[i] == "robot2"):
        robot.translate(x = -3, y = 0)
        robot.rotate(z = 3.1415)
'''

#Set enviroment
env = Environment('indoors-1/boxes')
env.set_camera_location([0, 0, 60])
env.set_camera_rotation([0, 0, 0])
