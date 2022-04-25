'''
This file contains custom exceptions which provide information
to callers if an operation fails.
'''

class NoConnectionException(Exception):
    pass

class JoystickAssignedException(Exception):
    '''
    This exception is to be raised when an attempt is made to assign the 
    arm or the drivetrain controls to a joystick that is already assigned.
    '''

class JoystickNotAssignedException(Exception):
    '''
    This exception is raised when a joystick being stopped is not initialized.
    '''

class JoystickNameMismatchException(Exception):
    '''
    This exception is raised when a joystick being initialized has a different
    name than the original expected joystick.
    '''