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
left_drive_2 = Motor(Ports.PORT2,GearSetting.RATIO_6_1,False)
left_motor_group = MotorGroup(left_drive_1,left_drive_2)

right_drive_1 = Motor(Ports.PORT3,GearSetting.RATIO_6_1,True)
right_drive_2 = Motor(Ports.PORT4,GearSetting.RATIO_6_1,False)
right_motor_group = MotorGroup(right_drive_1,right_drive_2)


def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here

def user_control():

    # Brain #
    brain.screen.clear_screen()
    brain.screen.print("driver control")

    # Variables #
    drive_left = 0
    drive_right = 0

    # place driver control in this while loop
    while True:
        
        # Joystick For Tank Control #
        motor_drive_left = controller.axis3.position()
        motor_drive_right = controller.axis2.position()

        # Threshold So Drive Stays Still If Joystick Axis Does Not Return Exactly To 0
        deadband = 15
        if abs(drive_left) < deadband:
            motor_drive_left = 0
        if abs(drive_right) < deadband:
            motor_drive_right = 0    

        ## Motors ##

        # Drivetrain @
        left_motor_group.spin(FORWARD,motor_drive_left, PERCENT)
        right_motor_group.spin(FORWARD,motor_drive_right, PERCENT)

        sleep(10) # Stops loop from running too fast.

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()