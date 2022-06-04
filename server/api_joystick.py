import exceptions
from flask import Blueprint, request
import pygame
from joystick import Joystick
from state import State

# The methods in this blueprint manage the configuration of and capture any
# data of connected joysticks.

bp = Blueprint('api/joystick', __name__, url_prefix='/api/joystick')
joystick = Joystick()
state = State()

@bp.route('/get_connected_joysticks', methods=['GET'])
def get_connected_joysticks():
    '''
    Returns a list of all the joysticks connected to the current machine. This
    includes all controllers and joysticks. Also returns whether joystick is being
    used for arm or drivetrain control.
    '''
    return joystick.get_connected_joysticks()

@bp.route('/start_arm_joystick', methods=['GET'])
def start_arm_joystick():
    '''
    Starts a joystick dedicated to controlling the arm.
    '''
    response = {'status': None}
    args = dict(request.args)

    # Validate that device index and name is provided.
    try:
        assert 'device_index' in args, 'device_index parameter not provided.'
        assert 'name' in args, 'name parameter not provided.'
    except AssertionError as err:
        response['status'] = 'Malformed request'
        response['message'] = str(err)
        return response

    try:
        device_index = int(args['device_index'])
        name = str(args['name'])
        joystick.start_arm_joystick(device_index, name)
    except exceptions.JoystickAssignedException:
        response['status'] = 'failure'
        response['message'] = 'A controller is already assigned to the arm, or this joystick is assigned to the drivetrain.'
        return response
    except exceptions.JoystickNameMismatchException:
        response['status'] = 'failure'
        response['message'] = 'The provided name does not match the device at specified index.'
        return response
    except pygame.error:
        response['status'] = 'failure'
        response['message'] = 'Failed to initialize joystick, most likely the device is no longer connected.'
        return response

    response['status'] = 'success'
    response['message'] = 'Successfully initialized arm controller'
    return response

@bp.route('/stop_arm_joystick', methods=['GET'])
def stop_arm_joystick():
    '''
    Stops currently running joystick controlling the arm.
    '''
    response = {'status': None}

    try:
        joystick.stop_arm_joystick()
    except exceptions.JoystickNotAssignedException:
        response['status'] = 'failure'
        response['message'] = 'No joysticks are assigned to the arm.'
        return response

    response['status'] = 'success'
    response['message'] = 'Stopped arm joystick'
    return response

@bp.route('/start_drivetrain_joystick', methods=['GET'])
def start_drivetrain_joystick():
    '''
    Starts a joystick dedicated to controlling the drivetrain of the
    rover. Returns errors if initialization is not performed correctly.
    '''
    response = {'status': None}
    args = dict(request.args)

    # Validate that device index and name is provided.
    try:
        assert 'device_index' in args, 'device_index paramater not provided.'
        assert 'name' in args, 'name parameter not provided.'
    except AssertionError as err:
        response['status'] = 'Malformed request'
        response['message'] = str(err)
        return response

    try:
        device_index = int(args['device_index'])
        name = str(args['name'])
        joystick.start_drivetrain_joystick(device_index, name)
    except exceptions.JoystickAssignedException:
        response['status'] = 'failure'
        response['message'] = 'A joystick is already assigned to the drivetrain, or this joystick is assigned to the arm.'
        return response
    except exceptions.JoystickNameMismatchException:
        response['status'] = 'failure'
        response['message'] = 'The provided name does not match the device at specified index.'
        return response
    except pygame.error:
        response['status'] = 'failure'
        response['message'] = 'Failed to initialize joystick, most likely the device is no longer connected.'
        return response
    
    response['status'] = 'success'
    response['message'] = 'Successfully initialized joystick for drivetrain'
    return response

@bp.route('/stop_drivetrain_joystick', methods=['GET'])
def stop_drivetrain_joystick():
    '''
    Stops the joystick currently controlling the drivetrain of
    the rover.
    '''
    response = {'status': None}

    try:
        joystick.stop_drivetrain_joystick()
    except exceptions.JoystickNotAssignedException:
        response['status'] = 'failure'
        response['message'] = 'No joysticks are assigned to the drivetrain.'
        return response
    
    response['status'] = 'success'
    response['message'] = 'Stopped drivetrain joystick'
    return response