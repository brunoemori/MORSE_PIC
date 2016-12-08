from morse.builder import *

robot1 = ATRV()
robot2 = ATRV()

motion1 = MotionVW()
motion2 = MotionVW()

robot1.append(motion1)
robot2.append(motion2)

robot1.translate(x = 0, y = 0)
robot2.translate(x = -3, y = 0)
robot2.rotate(z = 3.1415)

sick1 = Sick()
sick1.properties(laser_range = 10)
sick1.properties(scan_window = 180)
sick1.properties(resolution = 0.5)
sick1.properties(Visible_arc = True)
robot1.append(sick1)

sick2 = Sick()
sick2.properties(laser_range = 10)
sick2.properties(scan_window = 180)
sick2.properties(resolution = 0.5)
sick2.properties(Visible_arc = True)
robot2.append(sick2)

pose1 = Pose()
pose1.translate(z = -0.10)
pose1.add_stream('socket')
robot1.append(pose1)

pose2 = Pose()
pose2.translate(z = -0.10)
pose2.add_stream('socket')
robot2.append(pose2)

mov = Keyboard()
mov.properties(Speed = 5)
robot1.append(mov)

pose1.add_interface('socket')
sick1.add_interface('socket')
motion1.add_interface('socket')

env = Environment('indoors-1/boxes')
env.set_camera_location([0, 0, 60])
env.set_camera_rotation([0, 0, 0])
#env.select_display_camera(camera)
