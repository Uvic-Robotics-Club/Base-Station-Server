# This blueprint contains routes which are called by the rover. These routes are not intended to be called by any other
# entities such as the UI.
# NOTE: Currently HTTP connection allows any hosts to pretend to be rover. Converting to
# HTTPS and implement a secret key will minimize chances of threat actor exploiting connection.
from flask import Blueprint, request
from random import randrange
from state import State


bp = Blueprint('rover', __name__, url_prefix='/rover')
state = State()

@bp.route('/connect', methods=['GET'])
def connect():
    '''
    Establishes an HTTP connection to the server. The 'connection' is an abstraction on top
    of the HTTP requests, which allows the base station to be aware of the history of HTTP
    requests and who is sending/receiving requests.
    '''
    response = {'status': None}
    remote_addr = request.remote_addr

    # If connection already exists, prevent new connection.
    if state.get_attribute('connection_established'):
        response['status'] = 'failure'
        response['message'] = 'Another connection with ID {} already exists. Disconnect first then reconnect.'.format(state.get_attribute('connection_id'))
        return response

    # Generate new connection ID to indicate new connection.
    new_connection_id = randrange(100000000, 999999999)
    state.set_attribute('connection_id', new_connection_id)
    state.set_attribute('connection_remote_addr', remote_addr)
    state.set_attribute('connection_established', True)

    response['status'] = 'success'
    response['message'] = 'Successfully established connection.'
    response['connection_id'] = new_connection_id
    return response

@bp.route('/send_telemetry', methods=['POST'])
def send_telemetry():
    '''
    This request contains data from the rover which is saved in the state. The data provided must be of JSON format,
    and is stored in the "rover_telemetry" state. Current implementation overwrites all telemetry data from previous 
    request.
    '''
    response = {'status': None}

    if not request.is_json:
        response['status'] = 'failure'
        response['message'] = 'Request\'s MIME type is not application/json.'
        return response

    json_data = request.get_json()
    state.set_attribute('rover_telemetry', json_data)

    response['status'] = 'success'
    response['message'] = 'Successfully received telemetry.'
    return response

@bp.route('/disconnect', methods=['GET'])
def disconnect():
    '''
    Terminates the current connection to the server, if any. Only accepts a disconnect request
    if it originates from the same remote address that established the connection.
    '''
    response = {'status': None}
    remote_addr = request.remote_addr

    if not state.get_attribute('connection_established'):
        response['status'] = 'failure'
        response['message'] = 'No established connection exists.'
        return response

    if state.get_attribute('connection_remote_addr') != remote_addr:
        response['status'] = 'failure'
        response['message'] = 'Cannot terminate connection from another host.'

    # Set state variables to correct values
    state.set_attribute('connection_id', None)
    state.set_attribute('connection_remote_addr', None)
    state.set_attribute('connection_established', False)

    response['status'] = 'success'
    response['message'] = 'Successfully disconnected from base station.'
    return response
