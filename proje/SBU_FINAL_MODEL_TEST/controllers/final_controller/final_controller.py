# impo,y,thetrtant points:
# use <robot_position> to get current position of robot in <xa> format.
# use <robot_omega> to get current values for the wheels in <w1,w2,w3> format.
MAX_SPEED=6.28
import numpy as np
from initialization import * 
import math 
import time
wall=list()
turn=True
turn_forward=True
state="forward"
delay=0
goal_postition = np.array([1.3,6.15])
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
    bearing= bearing if bearing>=0 else bearing+360
    print(bearing)
    return bearing
def turn_until_left():
    global turn
    deg=zdegree()
    if ( 0<deg<=0.5):
        update_motor_speed(input_omega=[0,0,0])
        turn=False
    else:
        update_motor_speed(input_omega=[+6.28,+6.28,+6.28])
           
def turn_until_forward():
    global turn_forward
    if ( 300<zdegree()<=300.5 ):
        update_motor_speed(input_omega=[0,0,0])
        turn_forward=False
    else:
        deg=zdegree()
        deg= deg if deg>=0 else deg+360
        if  (deg>=120 and deg<300 ):
            update_motor_speed(input_omega=[-MAX_SPEED,-MAX_SPEED,-MAX_SPEED])
        else:
            update_motor_speed(input_omega=[MAX_SPEED,MAX_SPEED,MAX_SPEED])

def forward():
    update_motor_speed(input_omega=[3*(math.sin(60)*-MAX_SPEED),0,3*(math.sin(60)*MAX_SPEED)])
    update_robot_state()
def left():
    update_motor_speed(input_omega=[(MAX_SPEED*math.sin(30-(zdegree()-300.5))),(-(MAX_SPEED*math.cos(60-(zdegree()-300.5))+MAX_SPEED*math.sin(30-(zdegree()-300.5)))),(MAX_SPEED*math.cos(60-(zdegree()-300.5)))])
    update_robot_state()
def right():
    update_motor_speed(input_omega=[-MAX_SPEED*math.sin(30),(MAX_SPEED*math.cos(60)+MAX_SPEED*math.sin(30)),-MAX_SPEED*math.cos(60)])
    update_robot_state()
def down():    
    update_motor_speed(input_omega=[3*(math.sin(60)*MAX_SPEED),0,3*(math.sin(60)*-MAX_SPEED)])
    update_robot_state()
def cal_slope():
    update_robot_state()
    slope =  (goal_postition[1]-robot_position[1])/(goal_postition[0]-robot_position[0])
    return slope


if __name__ == "__main__":
    
    TIME_STEP = 32
    robot = init_robot(time_step=TIME_STEP)
    init_robot_state(in_pos=[0,0,0],in_omega=[0,0,0])
    mainslope=(goal_postition[1]-robot_position[1])/(goal_postition[0]-robot_position[0])
    print(mainslope)
    
    
    # DEFINE STATES HERE!
    
    while robot.step(TIME_STEP) != -1:
        
        gps_values,compass_val,sonar_value,encoder_value,ir_value = read_sensors_values()

        if (state=="forward"):
            if (turn_forward==True):
                turn_until_forward()
            if(turn_forward==False):
                forward()
                wall.clear()
                if (sonar_value[0]<200 or sonar_value[1]<200 or sonar_value[2]<200 or ir_value[0]<900 or ir_value[1]<900 or ir_value[2]<900 or ir_value[3]<900 or ir_value[4]<900 or ir_value[5]<900 ):
                    state="wall_follow"
                    turn=True
                    leave_point=(robot_position[0],robot_position[1])
                    update_motor_speed(input_omega=[0,0,0])

        elif (state=="wall_follow"):                   
            # if ((sonar_value[0]<200 or ir_value[2]<900 or ir_value[5]<900) and (sonar_value[2]<200 or ir_value[1]<900 or ir_value[4]<900)):
            #     #forward_right_wall
            #     down()
            # elif ((sonar_value[0]<200 or ir_value[2]<900 or ir_value[5]<900) and (sonar_value[1]<200 or ir_value[0]<900 or ir_value[3]<900)):
            #     #forward_left_wall
            #     right()            

            if(sonar_value[0]<200 or ir_value[2]<900 or ir_value[5]<900):
                if(len(wall)==0):
                    #forward_wall
                    wall.append("F")
                    if turn==True:
                        turn_until_left()
                    else:
                        forward()
                elif(wall[len(wall)-1]=="L"):
                    if(ir_value[2]<300 or ir_value[5]<300):
                        down()
            
            elif (sonar_value[2]<200 or ir_value[1]<900 or ir_value[4]<900):
                #right_wall
                if (wall[len(wall)-1]=="F"):
                    wall.append("R")
            elif (sonar_value[1]<200 or ir_value[0]<900 or ir_value[3]<900):
                #left_wall
                if (wall[len(wall)-1]=="F"):
                    if(turn_forward==True):
                        turn_until_forward()
                    else:
                        wall.append("L")
                        down()
                elif (wall[len(wall)-1]=="L"):
                    down()

            if ir_value[0]>900 and ir_value[1]>900 and ir_value[2]>900 and ir_value[3]>900 and ir_value[4]>900 and ir_value[5]>900:
                if (sonar_value[0]>500 and sonar_value[1]>500 and sonar_value[2]>500  ):    
                    state="delay"
                    delay = robot.getTime()
        elif (state=="delay"):
            if (delay+1<robot.getTime()):
                if(wall[len(wall)-1]=="F"):
                    forward()
                    state="wall_follow"
                if(wall[len(wall)-1]=="R"):
                    right()
                    state="wall_follow"
                    if(abs(leave_point[0]-robot_position[0])<0.1):
                        turn_forward=True
                        state="forward"  
                if(wall[len(wall)-1]=="L"):
                    left()
                    state="wall_follow"
                
        update_robot_state()
        #print(zdegree())
        #turn_until_forward()
        #forward() 
        #right()
        #update_motor_speed(input_omega=[math.sin(60)*-6.28,0,math.sin(60)*6.28])
        #update_motor_speed(input_omega=[6.28,6.28,6.28])
        
    pass