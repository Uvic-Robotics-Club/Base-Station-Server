from flask import Blueprint, request
from joystick import Joystick
from state import State
import threading

# Initialize joystick thread: Reads input from any joystick 
# and sends as command.
#thread_joystick = threading.Thread(target=Joystick.control_drivetrain)

bp = Blueprint('api/joystick', __name__, url_prefix='/api/joystick')
state = State()

@bp.route('/initialize', methods=['GET'])
def initialize():
    '''
    Starts joystick thread, which captures input from any
    attached joysticks
    '''
    response = {'status': None}

    if state.get_attribute('joystick_initialized'):
        response['status'] = 'failure'
        response['message'] = 'Joystick thread already initialized.'
        return response

    #thread_joystick.start()
    state.set_attribute('joystick_thread_event', threading.Event())
    state.set_attribute('joystick_thread', threading.Thread(target=Joystick.control_drivetrain))
    state.get_attribute('joystick_thread').start()
    state.set_attribute('joystick_initialized', True)
    

    response['status'] = 'success'
    response['message'] = 'Initialized joystick thread.'
    return response

@bp.route('/teardown', methods=['GET'])
def teardown():
    '''
    Stops the joystick thread, so that no further input from
    any connection joysticks are captures.
    '''
    response = {'status': None}

    if not state.get_attribute('joystick_initialized'):
        response['status'] = 'failure'
        response['message'] = 'No initialized joysticks.'
        return response

    # Set the thread event so joystick thread can terminate, then tear down.
    state.get_attribute('joystick_thread_event').set()
    state.get_attribute('joystick_thread').join()
    state.set_attribute('joystick_thread', None)

    # Set that there is no joystick initialized anymore.
    state.set_attribute('joystick_initialized', False)

    response['status'] = 'success'
    response['message'] = 'Teared down joystick thread successfully.'
    return response