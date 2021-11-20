from controller import Robot, Motor , GPS
from matplotlib import pyplot as plt
TIME_STEP = 64

MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()
gps=robot.getDevice("gps")
gps.enable(TIME_STEP)


# get a handler to the motors and set target position to infinity (speed control)
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
#circular
def speed(r):
   axel_length=0.053
   rspeed=6.28
   lspeed=(1-(axel_length/r))*rspeed
   return rspeed,lspeed
#leftMotor.setVelocity(speed(0.2)[0])
#rightMotor.setVelocity(speed(0.2)[1])
positionx=[]
positiony=[]
c=0

t0=robot.getTime()
#circular----------------------------------------------------------------------
# r=0.2
# leftMotor.setVelocity(speed(r)[0])
# rightMotor.setVelocity(speed(r)[1])
# while robot.step(TIME_STEP) != -1:
#    temp=gps.getValues()
#    positionx.append((temp[0],3))
#    positiony.append((temp[2],3))
#    c=c+1
#    t1=robot.getTime()
#    if t1-t0>13:
#       break;
# plt.plot(positionx,positiony)
# plt.show()
#arashmidos---------------------------------------------------------------
r=0.05
while robot.step(TIME_STEP) != -1:
   leftMotor.setVelocity(speed(r)[0])
   rightMotor.setVelocity(speed(r)[1])
   temp=gps.getValues()
   positionx.append(round(temp[0],3))
   positiony.append(round(temp[2],3))
   c=c+1
   t1=robot.getTime()
   r+=0.001*r
   if t1-t0>60:
      break;
plt.plot(positionx,positiony)
plt.show()
#sahmi-----------------------------------------------------
# r=0.05
# d=0.02
# t0=-30
# while robot.step(TIME_STEP) != -1:
#    leftMotor.setVelocity(speed(r)[0])
#    rightMotor.setVelocity(speed(r)[1])
#    temp=gps.getValues()
#    positionx.append(round(temp[0],3))
#    positiony.append(round(temp[2],3))
#    c=c+1
#    t1=robot.getTime()
#    r=d*pow(t1+t0,2)
#    print(r)
#    #if t0+4<t1:
#     #  leftMotor.setVelocity(rspeed)
#       #rightMotor.setVelocity(lspeed)
#      # t0=robot.getTime()

#    #temp=gps.getValues()
#    #position.append(temp)
#    #temp=gps.getValues()
#    #leftMotor.setVelocity(0.0 * MAX_SPEED)
#    #rightMotor.setVelocity(0.0 * MAX_SPEED)
#    if t1-t0>90:
#       break;
# plt.plot(positionx,positiony)
# plt.show()