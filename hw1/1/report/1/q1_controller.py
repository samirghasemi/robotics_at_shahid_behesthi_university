"""q1_controller controller."""

import numpy as np
import math
import matplotlib.pyplot as plt
from math import cos
from math import sin
from controller import Compass , GPS
from controller import Robot, Motor
TIME_STEP = 64

#functions---------------------------
def forward_kinematic(phi1_dot ,phi2_dot ,r ,l):
    x_dot = r * ((phi1_dot + phi2_dot) / 2)
    y_dot = 0
    teta_dot =  r * ((phi1_dot - phi2_dot) / l)
    return ((x_dot, y_dot), teta_dot)

def ccw_rotation(linear_v, heading):
    x_dot = linear_v[0]
    y_dot = linear_v[1]
    teta_dot = 0
    r = np.array(
        [cos(heading), -sin(heading), 0],
        [sin(heading), cos(heading), 0],
        [0, 0, 1]
    )
    v = np.array([x_dot], [y_dot], [teta_dot])
    return np.dot(r, v)

def get_degrees(compass_values):
    rad = math.atan2(compass_values[0], compass_values[2])
    degree = (rad - 1.5708) * 180.0 / math.pi 
    if degree < 0.0:
        degree = degree + 360.0
    return degree
#--------------------------------------------
robot = Robot()
compass = robot.getDevice("compass")
compass.enable(1)
gps=robot.getDevice("gps")
gps.enable(1)
#--------------------------------------------
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
#--------------------------------------------
positionx=[]
positiony=[]
angle=[]
t = []
t1 = 0

################################
leftMotor.setVelocity(4)
rightMotor.setVelocity(4)
################################
leftMotor.setVelocity(4)
rightMotor.setVelocity(-4)
################################
leftMotor.setVelocity(0)
rightMotor.setVelocity(5)
################################
leftMotor.setVelocity(2)
rightMotor.setVelocity(4)

t1=robot.getTime()+1

while robot.step(TIME_STEP) != -1:
   
   gps_value = gps.getValues()
   compass_value = compass.getValues()
   gbid = get_degrees(compass_value)
   
   angle.append(gbid)
   t.append(t1)
   positionx.append(round(gps_value[0],3))
   positiony.append(round(gps_value[2],3))
   
   t1=robot.getTime()+1
   if t1>30:
      break;

# plt.plot(positionx,positiony)
plt.plot(t,angle)
plt.show()

# Enter here exit cleanup code.
