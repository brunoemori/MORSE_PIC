#Simulation constants

#---------------------------------

#Coordinate constants
X_COORD = 0
Y_COORD = 1
Z_COORD = 2

#Sensor constants
FIRST_LASER = 0
LAST_LASER = 360
RANGE_MAX = 10 #Maximum reach of the robot's sensor
RANGE_LIMIT = 0.6 #Verify!

#Map constants
MAP_WIDTH = 562
MAP_HEIGHT = 562 
RESL = 0.08 #Map resolution
PRIORI = 0.5

'''
MAP_WIDTH = realmap_width / res
MAP_HEIGHT = realmap_height / res
'''

#Divide by 2 the realmap dimensions
HALF_REALMAP_WIDTH = 22.5
HALF_REALMAP_HEIGHT = 22.5

DISP_RATE = 1225
EVAP_RATE = 0.01


'''
For 100x100m and resolution = 0.08
    MAP_WIDTH = 562
    MAP_HEIGHT = 562
'''
