from controller import Robot, Motor, GPS
from matplotlib import pyplot as plt
TIME_STEP = 64
robot = Robot()
# conv = math.pi / 100
# comp=robot.getDevice("compass")
# comp.enable(TIME_STEP)
gps = robot.getDevice("gps")
gps.enable(TIME_STEP)
# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

# question 2 function:
def inverse_kinematic(x_dot, teta_dot, d, r):
    phi1_dot = ( (2 * x_dot) - (teta_dot * d) ) / (2 * r) 
    phi2_dot = ( (2 * x_dot) + (teta_dot * d) ) / (2 * r)
    return [phi1_dot, phi2_dot]
pos_x = []
pos_y = []
c = 0
t0 = robot.getTime()
# 1:
# leftMotor.setVelocity(inverse_kinematic(5, 0, 1, 2)[0])
# rightMotor.setVelocity(inverse_kinematic(5, 0, 1, 2)[1])
# 2:
leftMotor.setVelocity(inverse_kinematic(0, 3, 1, 2)[0])
rightMotor.setVelocity(inverse_kinematic(0, 3, 1, 2)[1])

while robot.step(TIME_STEP) != -1:
   temp = gps.getValues()
   pos_x.append(temp[0])
   pos_y.append(temp[2])
   c = c + 1
   t1 = robot.getTime()
   if t1 - t0 > 13:
       break;
plt.plot(pos_x, pos_y)
plt.show()       