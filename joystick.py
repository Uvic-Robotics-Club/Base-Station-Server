# This program will read the x and y axis data from a USB connected joystick and
# convert that data into left/right speed values for the runt rover. 
# This program then processes the left/right speed values and increments or decrements 
# them accordingly. Reads happen at specified intervals, and are then sent as commands
# to the rover.
# this is a note from antons wife to say she loves him <3 
import exceptions
import pygame
import requests
import time
from client import send_command

MAX_VAL = 100
X_AXIS_DEADZONE = 0.14 * MAX_VAL
Y_AXIS_DEADZONE = 0.14 * MAX_VAL
Z_AXIS_DEADZONE = 0.20 * MAX_VAL # Rotation around z axis
SLIDER_OFFSET = 1 * MAX_VAL # Slider in front of joystick

SLEEP_DURATION_SEC = 0.5

class Joystick():

    @staticmethod
    def control_drivetrain():
        pygame.init()

        # Initialize joystick
        try:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
        except pygame.error:
            print('Cannot find joystick. Not running joystick.')
            return

        while pygame.joystick.get_count() > 0:
            # Retrieve joystick data
            # X and Y axis range [-100.0, 100.0], where negative is reverse.
            pygame.event.get()
            x_axis = joystick.get_axis(0) * MAX_VAL
            y_axis = (-joystick.get_axis(1)) * MAX_VAL

            # Rotation around Z axis range [-100.0, 100.0] where negative is left rotation.
            z_axis = joystick.get_axis(3) * MAX_VAL
            # print(x_axis, y_axis, z_axis)

            # Limiter is in range [0, 10.0] where 0 is when slider is all the way
            # back towards negative sign
            limiter = (0 - joystick.get_axis(2)) * MAX_VAL
            limiter = (limiter + SLIDER_OFFSET) / 2 # Maps from [-100.0, 100.0] to [0, 100.0]

            # Set initial speed before considering turning
            speedLeft = speedRight = y_axis

            if abs(x_axis) < X_AXIS_DEADZONE and abs(y_axis) < Y_AXIS_DEADZONE:
                # Joystick is centred
                if abs(z_axis) > Z_AXIS_DEADZONE:
                    # Rotate rover in place
                    speedLeft += z_axis
                    speedRight -= z_axis
            else:
                # Joystick is not centred
                if x_axis != 0:
                    # Turn rover
                    speedLeft += x_axis
                    speedRight -= x_axis

            # Limit values
            speedLeft = -limiter if speedLeft < -limiter else limiter if speedLeft > limiter else speedLeft
            speedRight = -limiter if speedRight < -limiter else limiter if speedRight > limiter else speedRight

            # Arduino expects ints
            speed_left = int(speedLeft)
            speed_right = int(speedRight)

            speed_left_setpoint = 0
            speed_right_setpoint = 0

            if(speed_left < speed_left_setpoint):
                speed_left+=1
            elif(speed_left>speed_left_setpoint):
                speed_left-=1
            
            if(speed_right < speed_right_setpoint):
                speed_right+=1
            elif(speed_right>speed_right_setpoint):
                speed_right-=1


            write_direction_left = 0 
            write_direction_right = 0
            write_speed_left = 0
            write_speed_right = 0
        
            # reverse is 0
            # forward is 1

            if(speed_left>0):
                write_direction_left = 0
            else:
                write_direction_left = 1
            
            if(speed_right>0):
                write_direction_right = 0
            else:
                write_direction_right = 1

            write_speed_left = Joystick.remap(abs(speed_left),0,100,0,255)
            write_speed_right = Joystick.remap(abs(speed_right),0,100,0,255)

            # Build command and send.
            command = {
                'type': 'DRIVE_TRAIN',
                'left_speed': int(write_speed_left),
                'right_speed': int(write_speed_right),
                'left_direction': write_direction_left,
                'right_direction': write_direction_right
            }

            try:
                send_command(command)
            except exceptions.NoConnectionException:
                # print('No connection, cannot send joystick position...')
                pass
            except requests.exceptions.Timeout:
                # print('Timed out on request to send drive train command...')
                pass
            except AssertionError:
                # print('Response code is not 200 OK')
                pass

            time.sleep(SLEEP_DURATION_SEC)

    @staticmethod
    def remap(old_value, old_min, old_max, new_min, new_max):
        '''
        Similar to map() in Arduino. Remaps value from an old range 
        specified by old_min and old_max, to a new range between new_min
        and new_max.
        '''

        old_range = old_max - old_min
        if(old_range == 0):
            new_value = new_min
        else:
            new_range = new_max - new_min
            new_value = (((old_value - old_min) * new_range) / old_range) + new_min
        return new_value