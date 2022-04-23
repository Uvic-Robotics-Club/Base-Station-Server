from flask import Blueprint, request
from joystick import Joystick
from state import State
import threading

# Initialize joystick thread: Reads input from any joystick 
# and sends as command.
#thread_joystick = threading.Thread(target=Joystick.control_drivetrain)

bp = Blueprint('api/joystick', __name__, url_prefix='/api/joystick')
joystick_thread = None
joystick_thread_event = None
state = State()

@bp.route('/initialize', methods=['GET'])
def initialize():
    '''
    Starts joystick thread, which captures input from any
    attached joysticks
    '''
    response = {'status': None}

    if state.get_attribute('joystick_status') == 'initialized':
        response['status'] = 'failure'
        response['message'] = 'Joystick thread already initialized.'
        return response

    global joystick_thread
    global joystick_thread_event

    joystick_thread_event = threading.Event()
    joystick_thread = threading.Thread(target=Joystick.control_drivetrain)
    joystick_thread.start()
    #state.set_attribute('joystick_initialized', True)

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

    if not state.get_attribute('joystick_status') == 'initialized':
        response['status'] = 'failure'
        response['message'] = 'No initialized joysticks.'
        return response

    # Set the status so joystick thread can terminate, then tear down.
    state.set_attribute('joystick_status', 'tearing down')
    joystick_thread_event.set()
    joystick_thread.join()

    # Set that there is no joystick initialized anymore.
    state.set_attribute('joystick_status', 'uninitialized')

    response['status'] = 'success'
    response['message'] = 'Teared down joystick thread successfully.'
    return response