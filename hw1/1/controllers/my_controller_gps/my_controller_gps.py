import numpy as np
import math
import matplotlib.pyplot as plt
from math import cos
from math import sin
from controller import Compass , GPS
from controller import Robot, Motor
TIME_STEP = 64

conv = math.pi / 100

# question 1 functions:

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
    
# question 2 functions:

def inverse_kinematic(x_dot, teta_dot, l, r):
    phi1_dot = ( (2 * x_dot) - (teta_dot * l) ) / (2 * r)
    phi2_dot = ( (2 * x_dot) + (teta_dot * l) ) / (2 * r)
    return [phi1_dot, phi2_dot]




#3
def speed(r):
   axel_length=0.053
   rspeed=6.28
   lspeed=(1-(axel_length/r))*rspeed
   return rspeed,lspeed

def get_bearing_in_degrees(values):
    rad = math.atan2(values[0], values[2])
    bearing = (rad - 1.5708) / math.pi * 180.0
    if bearing < 0.0:
        bearing = bearing + 360.0
    return bearing


robot = Robot()
compass = robot.getDevice("compass")
compass.enable(1)
gps=robot.getDevice("gps")
gps.enable(1)


# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

# set up the motor speeds at 10% of the MAX_SPEED.
###################################################
# questin 1 tests:

# leftMotor.setVelocity(4)
# rightMotor.setVelocity(4)
################################
# leftMotor.setVelocity(4)
# rightMotor.setVelocity(-4)
################################
# leftMotor.setVelocity(0)
# rightMotor.setVelocity(0)
################################
# leftMotor.setVelocity(2)
# rightMotor.setVelocity(4)

############################################
# question 2 tests:

# leftMotor.setVelocity(4)
# rightMotor.setVelocity(4)



# while robot.step(TIME_STEP) != -1:
#    pass

positionx=[]
positiony=[]
angle=[]
t = []
t1 = 0
c = 0
r = 0.5
leftMotor.setVelocity(speed(r)[0])
rightMotor.setVelocity(speed(r)[1])
t1=robot.getTime()+1
while robot.step(TIME_STEP) != -1:
   temp = gps.getValues()
   compass_values = compass.getValues()
   gbid = get_bearing_in_degrees(compass_values)
   angle.append(gbid)
   t.append(t1)
   positionx.append(round(temp[0],3))
   positiony.append(round(temp[2],3))
   t1=robot.getTime()+1
   r = 0.2*pow(t1,2)
   if t1>30:
      break;

plt.plot(t,angle)
plt.show()