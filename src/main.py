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
left_drive_1 = Motor(Ports.PORT1,GearSetting.RATIO_6_1,False)
left_drive_2 = Motor(Ports.PORT2,GearSetting.RATIO_6_1,True)
left_motor_group = MotorGroup(left_drive_1,left_drive_2)

right_drive_1 = Motor(Ports.PORT3,GearSetting.RATIO_6_1,True)
right_drive_2 = Motor(Ports.PORT4,GearSetting.RATIO_6_1,False)
right_motor_group = MotorGroup(right_drive_1,right_drive_2)

## Drivetrain ##

drivetrain = DriveTrain(left_motor_group,right_motor_group)

drive_toggle = "Tank" # This will set the method of driving between tank and arcade


def toggle():

    global drive_toggle

    if drive_toggle == "Tank":
        drive_toggle = "Arcade"
    else:
        drive_toggle = "Tank"

def update_screen(): 

    ## Updates The Screen With All The Current Info ##

    brain.screen.clear_screen()

    if comp.is_driver_control:
        brain.screen.print("State: Driver Control")
    elif comp.is_autonomous:
        brain.screen.print("State: Autonomous")
    else:
        brain.screen.print("State: None")

    brain.screen.next_row()
    brain.screen.print("Drivetrain Mode:", drive_toggle)

    brain.screen.next_row()
    brain.screen.print("Left Motor Group Velocity:", left_motor_group.velocity)
    brain.screen.next_row()
    brain.screen.print("Right Motor Group Velocity:", right_motor_group.velocity)

def autonomous():

    update_screen()    

    # place automonous code here

def user_control():

    update_screen()

    controller.buttonX.pressed(toggle)

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
            motor_drive = controller.axis2.position()
            motor_turn = controller.axis1.position()

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
            motor_drive_left = controller.axis3.position()
            motor_drive_right = controller.axis2.position()

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



