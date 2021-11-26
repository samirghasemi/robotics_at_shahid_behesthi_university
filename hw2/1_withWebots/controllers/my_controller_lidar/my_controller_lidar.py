# """my_controller_lidar controller."""

# ###################################

###################################



# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot,Lidar
TIME_STEP = 64
# create the Robot instance.
robot = Robot()
max_speed = 6.28

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)
# motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

lidar = robot.getDevice('lidar')
lidar.enable(TIME_STEP)
lidar.enablePointCloud()


# get the time step of the current world.
# leftMotor.setVelocity(4)
# rightMotor.setVelocity(4)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
left_motor.setVelocity(max_speed*0)
right_motor.setVelocity(max_speed*0)
counter = 0
while robot.step(TIME_STEP) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    range_image = lidar.getRangeImage()
    a="{}".format(range_image)
    if 'inf' not in a and counter>50:
        with open('a.txt', 'w') as filehandle:
            for listitem in range_image:
                filehandle.write('%s\n' % listitem)
        filehandle.close()
        break
    counter = counter+1


# Enter here exit cleanup code.


