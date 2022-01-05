# impo,y,thetrtant points:
# use <robot_position> to get current position of robot in <xa> format.
# use <robot_omega> to get current values for the wheels in <w1,w2,w3> format.

state="turn"
import numpy as np
from initialization import * 
import math 

def update_robot_state():
    read_sensors_values()
    global robot_velocity
    global robot_position
    global robot_omega
    # updating the current theta
    robot_position[2] = math.atan2(compass_val[0], compass_val[1])
    # updating the currnet robot position
    robot_position[0] = gps_values[0]
    robot_position[1] = gps_values[1]
def zdegree():
    compass=read_sensors_values()[1]
    rad=math.atan2(compass[0],compass[1])
    bearing = (rad - 1.5708) / 3.14 * 180.0
    return bearing
def turn_until_left():
    if ( 0<zdegree()<=-1.5):
        update_motor_speed(input_omega=[0,0,0])
        return True
    else:
        update_motor_speed(input_omega=[-6.28,-6.28,-6.28])
        return False    
def turn_until_forward():
    if ( -60.5<zdegree()<=-59 ):
        update_motor_speed(input_omega=[0,0,0])
        return True
    else:
        update_motor_speed(input_omega=[-6.28,-6.28,-6.28])
        return False
def forward():
    update_motor_speed(input_omega=[3*(math.sin(60)*-6.28),0,3*(math.sin(60)*6.28)])
    update_robot_state()
def left():
    update_motor_speed(input_omega=[6.28*math.sin(29.3),-(6.28*math.cos(60)+6.28*math.sin(29.3)),6.28*math.cos(60)])
    update_robot_state()
def right():
    update_motor_speed(input_omega=[-6.28*math.sin(29.3),(6.28*math.cos(59)+6.28*math.sin(29.3)),-6.28*math.cos(60)])
    update_robot_state()
def down():    
    update_motor_speed(input_omega=[3*(math.sin(60)*6.28),0,3*(math.sin(60)*-6.28)])
    update_robot_state()

if __name__ == "__main__":
    goal_postition = np.array([0,0])
    TIME_STEP = 32
    robot = init_robot(time_step=TIME_STEP)
    init_robot_state(in_pos=[0,0,0],in_omega=[0,0,0])
    mainslope=(goal_postition[1]-robot_position[1])/(goal_postition[0]-robot_position[0])

    
    
    # DEFINE STATES HERE!
    
    while robot.step(TIME_STEP) != -1:
        
        gps_values,compass_val,sonar_value,encoder_value,ir_value = read_sensors_values()
        #print("sonar",sonar_value)
        #print("ir",ir_value)
        #print(robot_position[2])
        #update_robot_state()
        print(robot_position[2])
        #print( "gps=",gps_values);
        #print( "compass=",compass_val)
        #print( "sonar=",sonar_value)
        #print( "encoder=",encoder_value)
        #print( "ir=",ir_value)
        # DEFINE STATE MACHINE HERE!
        if (state=="turn"):
            r=turn_until_forward()
            if(r==True):
                state="forward"
            update_robot_state()
        elif (state=="forward"):
            forward()
            if (sonar_value[0]<200 or sonar_value[1]<200 or sonar_value[2]<200 or ir_value[0]<900 or ir_value[1]<900 or ir_value[2]<900 or ir_value[3]<900 or ir_value[4]<900 or ir_value[5]<900 ):
                state="wall_follow"
                update_motor_speed(input_omega=[0,0,0])

        elif (state=="wall_follow"):
            if ((sonar_value[0]<400 or ir_value[2]<900 or ir_value[5]<900) and (sonar_value[2]<400 or ir_value[1]<900 or ir_value[4]<900)):
                left()
            if ((sonar_value[0]<200 or ir_value[2]<900 or ir_value[5]<900) and (sonar_value[1]<200 or ir_value[0]<900 or ir_value[3]<900)):
                right()                
            if(sonar_value[0]<400 or ir_value[2]<900 or ir_value[5]<900):
                left()
        
            if ir_value[0]>900 and ir_value[1]>900 and ir_value[2]>900 and ir_value[3]>900 and ir_value[4]>900 and ir_value[5]>900:
                if (sonar_value[0]>200 and sonar_value[1]>200 and sonar_value[2]>200  ):
                    state="forward"
                    update_motor_speed(input_omega=[0,0,0])
        update_robot_state()
        #print(zdegree())
        #turn_until_forward()
        #forward() 
        #right()
        #update_motor_speed(input_omega=[math.sin(60)*-6.28,0,math.sin(60)*6.28])
        #update_motor_speed(input_omega=[6.28,6.28,6.28])
        
    pass