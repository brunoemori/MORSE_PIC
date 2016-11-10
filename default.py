from morse.builder import *

robot1 = ATRV()
motion = MotionVW()
robot1.append(motion)

robot1.translate(x = 22.32, y = -21.24)
robot1.rotate(z = 90)

sick = Sick()
sick.properties(laser_range = 10)
sick.properties(scan_window = 180)
sick.properties(resolution = 0.5)
sick.properties(Visible_arc = True)
robot1.append(sick)

pose = Pose()
pose.translate(z = -0.10)
pose.add_stream('socket')
robot1.append(pose)

mov = Keyboard()
mov.properties(Speed = 5)
robot1.append(mov)

camera = VideoCamera()
camera.translate(z = 1)
camera.rotate(z = 3.1415)
robot1.append(camera)

motion.add_interface('socket')
pose.add_interface('socket')
sick.add_interface('socket')

env = Environment('indoors-1/boxes')
env.set_camera_location([0, 0, 60])
env.set_camera_rotation([0, 0, 0])
env.select_display_camera(camera)
