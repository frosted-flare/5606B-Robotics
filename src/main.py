# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Simon Ward                                                   #
# 	Created:      6/7/2025, 6:03:07 PM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports #
from vex import *

## Important Variables ##
brain = Brain()
controller = Controller()



# Drive Motors #
left_drive_1 = Motor(Ports.PORT1,GearSetting.RATIO_6_1,True)
left_drive_2 = Motor(Ports.PORT2,GearSetting.RATIO_6_1,True)
left_motor_group = MotorGroup(left_drive_1,left_drive_2)

right_drive_1 = Motor(Ports.PORT3,GearSetting.RATIO_6_1,False)
right_drive_2 = Motor(Ports.PORT4,GearSetting.RATIO_6_1,False)
right_motor_group = MotorGroup(right_drive_1,right_drive_2)

## Drivetrain ##

drivetrain = DriveTrain(left_motor_group,right_motor_group)

drive_toggle = "Tank" # This will set the method of driving between tank and arcade
drive_speed = 1 # This how fast the robot will drive in percentage

def toggle_mode():

    global drive_toggle

    if drive_toggle == "Tank":
        drive_toggle = "Arcade"
    else:
        drive_toggle = "Tank"

def toggle_speed():
    global drive_speed
    if drive_speed == 1:
        drive_speed = 0.5
    else:
        drive_speed = 1
    
def update_screen(): 

    ## Updates The Screen With All The Current Info ##

    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    if comp.is_driver_control:
        brain.screen.print("State: Driver Control")
    elif comp.is_autonomous:
        brain.screen.print("State: Autonomous")
    else:
        brain.screen.print("State: None")

    brain.screen.set_cursor(2,1)
    brain.screen.print("Drivetrain Mode:", drive_toggle)
    brain.screen.set_cursor(3,1)
    brain.screen.print("Drivetrain Speed:",drive_speed*100, "Percent")


    brain.screen.set_cursor(4,1)
    brain.screen.print("Left Motor Group Velocity:", left_motor_group.velocity(),"RPM")
    brain.screen.set_cursor(5,1)
    brain.screen.print("Right Motor Group Velocity:", right_motor_group.velocity(),"RPM")

    brain.screen.set_cursor(6,1)
    brain.screen.print("Left Motor Group Temperature:", left_motor_group.temperature(), "Degrees")
    brain.screen.set_cursor(7,1)
    brain.screen.print("Right Motor Group Temperature:", right_motor_group.temperature(), "Degrees")



def autonomous():

    update_screen()    

    # place automonous code here

def user_control():

    update_screen()

    controller.buttonX.pressed(toggle_mode)
    controller.buttonR2.pressed(toggle_speed)

    # place driver control in this while loop
    while True:
        
        ## Screen ##
                
        update_screen()


        ## Check For Drive Type ##

        if drive_toggle == "Arcade": # Arcade

            ## Variables ##
            
            motor_drive = 0
            motor_turn = 0

            # Joystick For Arcade Control #
            motor_drive = controller.axis2.position() * drive_speed
            motor_turn = controller.axis1.position() * drive_speed

            # Threshold So Drive Stays Still If Joystick Axis Does Not Return Exactly To 0
            deadband = 15
            if abs(motor_drive) < deadband:
                motor_drive = 0
            if abs(motor_turn) < deadband:
                motor_turn = 0    

            ## Drivetrain ##

            left_motor_group.set_velocity((controller.axis2.position() + controller.axis1.position()), PERCENT)
            right_motor_group.set_velocity((controller.axis2.position() - controller.axis1.position()), PERCENT)
            left_motor_group.spin(FORWARD)
            right_motor_group.spin(FORWARD)

        elif drive_toggle == "Tank": # Tank

            ## Variables ##
            
            motor_drive_left = 0
            motor_drive_right = 0

            # Joystick For Tank Control #
            motor_drive_left = controller.axis3.position() * drive_speed
            motor_drive_right = controller.axis2.position() * drive_speed

            # Threshold So Drive Stays Still If Joystick Axis Does Not Return Exactly To 0
            deadband = 15
            if abs(motor_drive_left) < deadband:
                motor_drive_left = 0
            if abs(motor_drive_right) < deadband:
                motor_drive_right = 0    

            ## Motors ##

            left_motor_group.spin(FORWARD,motor_drive_left, PERCENT)
            right_motor_group.spin(FORWARD,motor_drive_right, PERCENT)


        sleep(10) # Stops loop from running too fast.

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()



