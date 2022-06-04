'''
Thread-safe implementation of a collection of states that must be stored when the server
is active. The collection is a singleton class, and so there is only one instance of this 
class that can exist at one time.
'''
from singleton import Singleton
from threading import Lock

class State(metaclass=Singleton):
    '''
    This thread-safe class stores data for the base station server during the 
    lifetime of the application. This inherits the Singleton metaclass, and as
    such the same data may be accessed from anywhere inside this application.
    '''
    __lock_set_attr = Lock()
    __data = {}

    def __init__(self):
        '''
        Initializes the singleton instance of this class. Sets default values for
        certain parameters as required such that each parameter's value is known at
        all times during the application's lifecycle.
        '''

        # Initialize data with default parameters
        self.__data = {
            'connection_established': False,
            'connection_remote_addr': None,
            'connection_port': None,
            'connection_id': None,
            'connection_ping_status': None,
            'connection_ping_last_response': None,
            'hotspot_active': False,
            'drivetrain_joystick_status': 'uninitialized',
            'drivetrain_joystick_speed_left': None,
            'drivetrain_joystick_speed_right': None,
            'drivetrain_joystick_direction_left': None,
            'drivetrain_joystick_direction_right': None,
            'arm_controller_status': 'uninitialized',
            'arm_controller_x_axis_velocity': None,
            'arm_controller_y_axis_velocity': None,
            'arm_controller_z_axis_velocity': None,
            'arm_controller_gripper_velocity': None,
            'arm_controller_gripper_rotation_velocity': None,
            'rover_telemetry': {}
        }
    
    def set_attribute(self, attribute_name, value):
        '''
        Sets a value to an attribute name to the application's state. The attribute
        name must be a string. Since this method is non-reentrant, we use locks to 
        ensure only one caller at a time can set attribute value.
        '''
        assert type(attribute_name) == str

        # Acquire lock
        self.__lock_set_attr.acquire()
        self.__data[attribute_name] = value
        # Release lock
        self.__lock_set_attr.release()

    def get_attribute(self, attribute_name):
        '''
        Returns an attribute value of the application's state. Raises KeyError if
        attribute name is not found.
        '''
        assert type(attribute_name) == str
        return self.__data[attribute_name]

    def get_all_attributes(self):
        '''
        Returns all of the attributes of the application state.
        '''
        return self.__data

    def delete_attribute(self, attribute_name):
        '''
        Deletes an attribute value from the application's state. The attribute name
        must be a string. Since this method is non-reentrant, we use lcosk to ensure
        only one caller at a time can delete an attribute. Raises KeyError if attribute
        name is not found.
        '''
        assert type(attribute_name) == str

        # Acquire lock
        self.__lock_set_attr.acquire()
        del self.__data[attribute_name]
        # Release lock
        self.__lock_set_attr.release()
