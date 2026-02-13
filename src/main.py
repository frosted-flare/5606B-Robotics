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
left_drive_3 = Motor(Ports.PORT3,GearSetting.RATIO_6_1,False)
left_motor_group = MotorGroup(left_drive_1,left_drive_2,left_drive_3)

right_drive_1 = Motor(Ports.PORT4,GearSetting.RATIO_6_1,False)
right_drive_2 = Motor(Ports.PORT5,GearSetting.RATIO_6_1,False)
right_drive_3 = Motor(Ports.PORT6,GearSetting.RATIO_6_1,True)
right_motor_group = MotorGroup(right_drive_1,right_drive_2,right_drive_3)

## Drivetrain ##

drivetrain = DriveTrain(left_motor_group,right_motor_group)
drivetrain.set_stopping(BrakeType.COAST)

drive_toggle = "Tank" # This will set the method of driving between tank and arcade
drive_speed = 1 # This how fast the robot will drive in percentage

## Other Motors #
belt_1 = Motor(Ports.PORT7,GearSetting.RATIO_18_1,True)
outake_1 = Motor(Ports.PORT8,GearSetting.RATIO_18_1,True)

belt_1.set_stopping(HOLD)
outake_1.set_stopping(HOLD)

belt_1_state = 0
outake_1_state = 0

loader_pneumatic = Pneumatics(brain.three_wire_port.a)
goal_pneumatic = Pneumatics(brain.three_wire_port.b)
parking_pneumatic = Pneumatics(brain.three_wire_port.c)

loader_pneumatic_state = False
goal_pneumatic_state = False
parking_pneumatic_state = False

## Timer ##
timer = Timer()

## Status Screen ##

status_list = ["Basic_Info","Left Motors", "Right Motors"]
current_status_screen = 0
status_screen_debounce = 400

last_status_update = timer.time()

def toggle_loader_pnumatic():
    global loader_pneumatic_state
    if loader_pneumatic_state == True:
        loader_pneumatic_state = False
        loader_pneumatic.close()

    else:
        loader_pneumatic_state = True
        loader_pneumatic.open()

def toggle_goal_pnumatic():
    global goal_pneumatic_state
    if goal_pneumatic_state == True:
        goal_pneumatic_state = False
        goal_pneumatic.close()

    else:
        goal_pneumatic_state = True
        goal_pneumatic.open()

def toggle_parking_pnumatic():
    global parking_pneumatic_state
    if parking_pneumatic_state == True:
        parking_pneumatic_state = False
        parking_pneumatic.close()

    else:
        parking_pneumatic_state = True
        parking_pneumatic.open()

def toggle_mode():

    global drive_toggle

    if drive_toggle == "Tank":
        drive_toggle = "Arcade"
    else:
        drive_toggle = "Tank"

    
def change_status_screen(): # Changes the current status screen

    global current_status_screen

    if current_status_screen != len(status_list) - 1:
        current_status_screen += 1
    else:
        current_status_screen = 0

def update_screen(): 

    ## Controller screen ##
    controller.screen.clear_screen()
    controller.screen.set_cursor(1,1)

    controller.screen.print("Mode:", drive_toggle)
    controller.screen.set_cursor(2,1)
    controller.screen.print("Speed:",drive_speed*100)
    controller.screen.set_cursor(3,1)

    ## Updates The Brain Screen With All The Current Info ##

    if current_status_screen == 0:
        
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)

        brain.screen.set_font(FontType.MONO40)
        brain.screen.print("General:")
        brain.screen.set_cursor(4,1)
        brain.screen.set_font(FontType.MONO20)
       
        if comp.is_driver_control:
            brain.screen.print("  State: Driver Control")
        elif comp.is_autonomous:
            brain.screen.print("  State: Autonomous")
        else:
            brain.screen.print("  State: None")
        brain.screen.set_cursor(5,1)


        brain.screen.print("  Drivetrain Mode:", drive_toggle)
        brain.screen.set_cursor(6,1)
        brain.screen.print("  Drivetrain Speed:",drive_speed*100, "Percent")
        brain.screen.set_cursor(8,1)

        brain.screen.print("  Left Motor Group Temperature:", left_motor_group.temperature(TemperatureUnits.CELSIUS), "Degrees")
        brain.screen.set_cursor(9,1)
        brain.screen.print("  Right Motor Group Temperature:", right_motor_group.temperature(TemperatureUnits.CELSIUS), "Degrees")
        brain.screen.set_cursor(10,1)
        

        if brain.sdcard.is_inserted() == True:
            brain.screen.draw_image_from_file('logo_small_size.png',380,0)

    elif current_status_screen == 1:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)

        brain.screen.set_font(FontType.MONO40)
        brain.screen.print("Left Motors:")
        brain.screen.set_cursor(4,1)
        brain.screen.set_font(FontType.MONO20)


        brain.screen.print("  Left Motor Group Velocity:", left_motor_group.velocity(),"RPM")
        brain.screen.set_cursor(5,1)

        if brain.sdcard.is_inserted() == True:
            brain.screen.draw_image_from_file('logo_small_size.png',380,0)


    elif current_status_screen == 2:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)

        brain.screen.set_font(FontType.MONO40)
        brain.screen.print("Right Motors:")
        brain.screen.set_cursor(4,1)
        brain.screen.set_font(FontType.MONO20)


        brain.screen.print("  Right Motor Group Velocity:", right_motor_group.velocity(),"RPM")
        brain.screen.set_cursor(5,1)


        if brain.sdcard.is_inserted() == True:
            brain.screen.draw_image_from_file('logo_small_size.png',380,0)

def move_belt(value):
    global belt_1_state
    global belt_1

    if (belt_1_state < 1 and value == 1) or (belt_1_state > -1 and value == -1): 
        belt_1_state += value
    belt_1.set_velocity(200)
    if belt_1_state == 1:
        belt_1.spin(FORWARD)
    elif belt_1_state == -1:
        belt_1.spin(REVERSE)
    else:
        belt_1.stop()

def move_outake(value):
    global outake_1_state
    global outake_1

    if (outake_1_state < 1 and value == 1) or (outake_1_state > -1 and value == -1): 
        outake_1_state += value
    outake_1.set_velocity(100)
    if outake_1_state == 1:
        outake_1.spin(FORWARD)
    elif outake_1_state == -1:
        outake_1.spin(REVERSE)
    else:
        outake_1.stop()

def autonomous():

    update_screen()  
    move_belt(1)  
    drivetrain.drive_for(FORWARD,1200,MM,30,PERCENT)
    drivetrain.turn_for(LEFT,80,DEGREES,10,PERCENT)
    toggle_loader_pnumatic()
    drivetrain.drive_for(FORWARD,50,MM,20,PERCENT)
    drivetrain.drive_for(FORWARD,550,MM,25,PERCENT)
    drivetrain.drive_for(REVERSE,75,MM,20,PERCENT)
    drivetrain.drive_for(FORWARD,150,MM,40,PERCENT)
    drivetrain.drive_for(REVERSE,75,MM,20,PERCENT)
    drivetrain.drive_for(FORWARD,150,MM,40,PERCENT)
    drivetrain.drive_for(REVERSE,75,MM,20,PERCENT)
    drivetrain.drive_for(FORWARD,150,MM,40,PERCENT)
    drivetrain.drive_for(REVERSE,100,MM,20,PERCENT)
    drivetrain.turn_for(right_drive_1,10,DEGREES,10,PERCENT)
    drivetrain.drive_for(REVERSE,1100,MM,40,PERCENT)
    move_outake(1)



def user_control():
    global last_status_update

    global belt_1_state
    global outake_1_state

    update_screen()

    brain.screen.pressed(change_status_screen)

    controller.buttonX.pressed(toggle_mode)

    controller.buttonL1.pressed(move_belt,(1,))
    controller.buttonL2.pressed(move_belt,(-1,))

    controller.buttonR1.pressed(move_outake,(1,))
    controller.buttonR2.pressed(move_outake,(-1,))

    controller.buttonLeft.pressed(toggle_loader_pnumatic)
    controller.buttonRight.pressed(toggle_goal_pnumatic)
    controller.buttonUp.pressed(toggle_parking_pnumatic)

    # place driver control in this while loop
    while True:
        
        ## Screen ##
                
        if timer.time() - status_screen_debounce > last_status_update:
            last_status_update = timer.time()
            update_screen()


        ## Check For Drive Type ##

        if drive_toggle == "Arcade": # Arcade

            ## Variables ##
            
            motor_drive = 0
            motor_turn = 0

    

            # Threshold So Drive Stays Still If Joystick Axis Does Not Return Exactly To 0
            deadband = 15
            if abs(motor_drive) < deadband:
                motor_drive = 0
            if abs(motor_turn) < deadband:
                motor_turn = 0    

            ## Drivetrain ##

            left_motor_group.set_velocity((controller.axis2.position() + controller.axis1.position())* drive_speed, PERCENT)
            right_motor_group.set_velocity((controller.axis2.position() - controller.axis1.position())* drive_speed, PERCENT)
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


