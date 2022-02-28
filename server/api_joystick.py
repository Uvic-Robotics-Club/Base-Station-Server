from flask import Blueprint, request
from joystick import Joystick
from state import State
import threading

# Initialize joystick thread: Reads input from any joystick 
# and sends as command.
thread_joystick = threading.Thread(target=Joystick.control_drivetrain)

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

    thread_joystick.start()
    state.set_attribute('joystick_initialized', True)

    response['status'] = 'success'
    response['message'] = 'Initialized joystick thread.'
    return response