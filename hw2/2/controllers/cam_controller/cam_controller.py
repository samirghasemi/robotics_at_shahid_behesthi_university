from controller import Robot,Camera
TIME_STEP = 64
robot = Robot()
max_speed = 6.28

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(1)
right_motor.setVelocity(1)

camera = robot.getDevice('cam')
camera.enable(TIME_STEP)


while robot.step(TIME_STEP) != -1:
    camera.getImage()
    camera.saveImage('image.jpg', 100)
