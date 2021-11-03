import numpy as np
import math
import matplotlib.pyplot as plt
from math import cos
from math import sin
from controller import Compass
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

robot = Robot()

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



while robot.step(TIME_STEP) != -1:
   pass
