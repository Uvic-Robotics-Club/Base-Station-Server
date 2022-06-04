#!/usr/bin/env python3
# this is a note from antons wife to say she loves him <3 
import exceptions
import pygame
import requests
from state import State
import threading
import time
from client import send_command

MAX_VAL = 100
X_AXIS_DEADZONE = 0.14 * MAX_VAL
Y_AXIS_DEADZONE = 0.14 * MAX_VAL
Z_AXIS_DEADZONE = 0.20 * MAX_VAL # Rotation around z axis
SLIDER_OFFSET = 1 * MAX_VAL # Slider in front of joystick

# Minimum interval between reads of joystick axis.
SLEEP_DURATION_SEC = 0.3
PERCENTAGE_VARIANCE = 0.05

state = State()

# Utility method used by joystick and controller.
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

class ArmController():
    def __init__(self, device_index, thread_termination_event):
        self.joystick = pygame.joystick.Joystick(device_index)
        self.joystick.init()
        self.thread_termination_event = thread_termination_event

        # Update arm controller state so feedback in UI shows controller is working
        state.set_attribute('arm_controller_status', 'initialized')
        self.capture_input_and_send_command()

    def capture_input_and_send_command(self):
        while not self.thread_termination_event.is_set():
            pygame.event.get()

            x_axis = self.joystick.get_axis(0)
            y_axis = self.joystick.get_axis(1)
            z_axis = self.joystick.get_axis(4)
            gripper_close = self.joystick.get_axis(2)
            gripper_open = self.joystick.get_axis(5)

            # Adjust x_axis velocity so that if it is less than 0.2, then 
            # it is in the deadzone
            x_axis_velocity = x_axis
            if abs(x_axis_velocity) < 0.2:
                x_axis_velocity = 0

            # Adjust y_axis velocity and set to 0 if values less than 0.2 (deadzone)
            y_axis_velocity = -y_axis
            if abs(y_axis_velocity) < 0.2:
                y_axis_velocity = 0

            # Adjust z_axis velocity and set to 0 if value less than 0.2 (deadzone)
            z_axis_velocity = -z_axis
            if abs(z_axis_velocity) < 0.2:
                z_axis_velocity = 0

            # Calculate gripper value such that LT & RT gripper movements are
            # both taken into account.
            # gripper_velocity 1.0 indicates open, -1.0 indicates close
            gripper_close_velocity = remap(gripper_close, -1.0, 1.0, 0, 1.0)
            gripper_open_velocity = remap(gripper_open, -1.0, 1.0, 0, 1.0)
            gripper_velocity = gripper_open_velocity - gripper_close_velocity

            # Update state attributes so that UI can be updated with most recent joystick input.
            state.set_attribute('arm_controller_x_axis_velocity', x_axis_velocity)
            state.set_attribute('arm_controller_y_axis_velocity', y_axis_velocity)
            state.set_attribute('arm_controller_z_axis_velocity', z_axis_velocity)
            state.set_attribute('arm_controller_gripper_velocity', gripper_velocity)
            state.set_attribute('arm_controller_gripper_rotation_velocity', None)

            # Build command and send
            command = {
                'type': 'ARM',
                'x_axis_velocity': x_axis_velocity,
                'y_axis_velocity': y_axis_velocity,
                'z_axis_velocity': z_axis_velocity,
                'gripper_velocity': gripper_velocity,
                'gripper_rotation_velocity': 0
            }

            try:
                print(command)
                send_command(command)
            except exceptions.NoConnectionException:
                print('No connection, cannot send joystick position...')
                pass
            except requests.exceptions.Timeout:
                print('Timed out on request to send drive train command...')
                pass
            except AssertionError:
                print('Response code is not 200 OK')
                pass

            time.sleep(SLEEP_DURATION_SEC)

        # Update state attributes so that UI can be updated with most recent joystick input.
        state.set_attribute('arm_controller_x_axis_velocity', None)
        state.set_attribute('arm_controller_y_axis_velocity', None)
        state.set_attribute('arm_controller_z_axis_velocity', None)
        state.set_attribute('arm_controller_gripper_velocity', None)
        state.set_attribute('arm_controller_gripper_rotation_velocity', None)


class DriveTrainJoystick():
    def __init__(self, device_index, thread_termination_event):
        self.joystick = pygame.joystick.Joystick(device_index)
        self.joystick.init()
        self.thread_termination_event = thread_termination_event
        
        # Update drive train joystick state so feedback in UI shows joystick is working
        state.set_attribute('drivetrain_joystick_status', 'initialized')
        self.capture_input_and_send_command()

    def capture_input_and_send_command(self):
        while not self.thread_termination_event.is_set():
            # Retrieve joystick data
            # X and Y axis range [-100.0, 100.0], where negative is reverse.
            pygame.event.get()

            x_axis = self.joystick.get_axis(0) * MAX_VAL
            y_axis = (-self.joystick.get_axis(1)) * MAX_VAL

            # Set initial speed before considering turning
            speedLeft = speedRight = y_axis

            # If x_axis and y_axis are both within the deadzone, assume joystick is centered.
            if abs(x_axis) < X_AXIS_DEADZONE and abs(y_axis) < Y_AXIS_DEADZONE:
                pass
            else:
                # Joystick is not centred
                if x_axis != 0:
                    # Turn rover
                    speedLeft += x_axis
                    speedRight -= x_axis

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
            elif(speed_right > speed_right_setpoint):
                speed_right-=1


            write_direction_left = 0 
            write_direction_right = 0
            write_speed_left = 0
            write_speed_right = 0
        
            # reverse is 0, forward is 1
            if(speed_left>0):
                write_direction_left = 1
            else:
                write_direction_left = 0
            
            if(speed_right>0):
                write_direction_right = 1
            else:
                write_direction_right = 0

            write_speed_left = int(remap(abs(speed_left),0,100,0,255))
            write_speed_right = int(remap(abs(speed_right),0,100,0,255))

            # Update state attributes so that UI can be updated with most recent joystick input.
            state.set_attribute('drivetrain_joystick_speed_left', write_speed_left)
            state.set_attribute('drivetrain_joystick_speed_right', write_speed_right)
            state.set_attribute('drivetrain_joystick_direction_left', write_direction_left)
            state.set_attribute('drivetrain_joystick_direction_right', write_direction_right)

            # Build command and send.
            command = {
                'type': 'DRIVE_TRAIN',
                'left_speed': write_speed_left,
                'right_speed': write_speed_right,
                'left_direction': write_direction_left,
                'right_direction': write_direction_right
            }

            try:
                print(command)
                send_command(command)
            except exceptions.NoConnectionException:
                print('No connection, cannot send joystick position...')
                pass
            except requests.exceptions.Timeout:
                print('Timed out on request to send drive train command...')
                pass
            except AssertionError:
                print('Response code is not 200 OK')
                pass

            time.sleep(SLEEP_DURATION_SEC)

        # Update state attributes so that UI can be updated with most recent joystick input.
        state.set_attribute('drivetrain_joystick_speed_left', None)
        state.set_attribute('drivetrain_joystick_speed_right', None)
        state.set_attribute('drivetrain_joystick_direction_left', None)
        state.set_attribute('drivetrain_joystick_direction_right', None)

class Joystick():
    '''
    This class manages all the connected joysticks to the machine, including returning
    information about the joysticks, capturing input, and managing profiles
    '''

    def __init__(self):
        pygame.init()
        self.connected_joysticks = {}

        self.arm_joystick_thread = None
        self.arm_joystick_thread_event = None
        self.arm_joystick_assigned_index = None # pygame device index of arm joystick
        self.arm_joystick_assigned_name = None # pygame name of arm joystick

        self.drivetrain_joystick_thread = None
        self.drivetrain_joystick_thread_event = None
        self.drivetrain_joystick_assigned_index = None # pygame device index of drivetrain joystick
        self.drivetrain_joystick_assigned_name = None # pygame name of drivetrain joystick

    def get_connected_joysticks(self):
        '''
        Updates information related to all connected joysticks. Must
        restart the joystick pygame module to detect any changes in connected
        joysticks. Returns a dictionary with the joystick id and the name of the
        joystick.
        '''
        self.connected_joysticks = {}

        num_connected_joysticks = pygame.joystick.get_count()
        for i in range(num_connected_joysticks):
            joystick = pygame.joystick.Joystick(i)

            # Boolean value indicating whether this joystick currently controls the arm
            joystick_controls_arm = (self.arm_joystick_assigned_index == i) and (self.arm_joystick_assigned_name == joystick.get_name())

            # Boolean value indicating whether this joystick currently controls the  drivetrain
            joystick_controls_drivetrain = (self.drivetrain_joystick_assigned_index == i) and (self.drivetrain_joystick_assigned_name == joystick.get_name())

            self.connected_joysticks[i] = {'name': joystick.get_name(), 'controls_arm': joystick_controls_arm, 'controls_drivetrain': joystick_controls_drivetrain}
        return self.connected_joysticks.copy()

    def start_arm_joystick(self, device_index, name):
        '''
        Starts a new thread for the joystick used to control the arm. The thread
        manages the capture and sending of commands to the rover. Before starting 
        thread, ensures that the device is still connected. The method takes the 
        device index and name as input.
        '''
        assert type(device_index) == int
        assert type(name) == str

        # If joystick is already assigned, then do not continue.
        if (self.arm_joystick_assigned_index is not None) or self.drivetrain_joystick_assigned_index == device_index:
            raise exceptions.JoystickAssignedException

        # If joystick has a different name than expected, then do not continue.
        joystick_test_instance = pygame.joystick.Joystick(device_index)
        if joystick_test_instance.get_name() != name:
            raise exceptions.JoystickNameMismatchException

        self.arm_joystick_assigned_index = device_index
        self.arm_joystick_assigned_name = name
        self.arm_joystick_thread_event = threading.Event()
        self.arm_joystick_thread = threading.Thread(target=ArmController, args=(device_index, self.arm_joystick_thread_event))
        self.arm_joystick_thread.start()

    def stop_arm_joystick(self):
        '''
        Stops the thread for the joystick used to control the arm.
        '''

        # If joystick is not assigned, then do not continue.
        if self.arm_joystick_assigned_index is None:
            raise exceptions.JoystickNotAssignedException

        self.arm_joystick_thread_event.set()
        self.arm_joystick_thread.join()
        self.arm_joystick_assigned_index = None
        self.arm_joystick_assigned_name = None
        self.arm_joystick_thread = None

    def start_drivetrain_joystick(self, device_index, name):
        '''
        Starts a new thread for the joystick used to control the drivetrain. The
        thread manages the capture and sendingf of commands to the rover. Before starting
        the thread, ensures that the device is still connected. THe method takes the
        device index and name as input.
        '''
        assert type(device_index) == int
        assert type(name) == str

        # If joystick is already assigned, then do not continue.
        if (self.drivetrain_joystick_assigned_index is not None) or self.arm_joystick_assigned_index == device_index:
            raise exceptions.JoystickAssignedException

        # If joystick has a different name than expected, then do not continue.
        joystick_test_instance = pygame.joystick.Joystick(device_index)
        if joystick_test_instance.get_name() != name:
            raise exceptions.JoystickNameMismatchException

        self.drivetrain_joystick_assigned_index = device_index
        self.drivetrain_joystick_assigned_name = name
        self.drivetrain_joystick_thread_event = threading.Event()
        self.drivetrain_joystick_thread = threading.Thread(target=DriveTrainJoystick, args=(device_index, self.drivetrain_joystick_thread_event))
        self.drivetrain_joystick_thread.start()

    def stop_drivetrain_joystick(self):
        '''
        Stops the thread for the joystick used to control the drivetrain.
        '''

        # If joystick is not assigned, then do not continue.
        print(self.drivetrain_joystick_assigned_index)
        if self.drivetrain_joystick_assigned_index is None:
            raise exceptions.JoystickNotAssignedException

        self.drivetrain_joystick_thread_event.set()
        self.drivetrain_joystick_thread.join()
        self.drivetrain_joystick_assigned_index = None
        self.drivetrain_joystick_assigned_name = None
        self.drivetrain_joystick_thread = None

        state.set_attribute('drivetrain_joystick_status', 'uninitialized')